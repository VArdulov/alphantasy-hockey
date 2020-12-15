import requests
import logging

from fantasy.scraping.config import (
    base_url,
    season_subfolder_format,
    event_summary_uri,
    game_summary_uri
)

from os import path
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pandas import to_datetime, read_html
from pandas.errors import ParserError
from logging import info, warning



@dataclass
class DataSoup:
    event_summary: BeautifulSoup
    game_summary: BeautifulSoup


def get_summary_soups(season, game_id, verbose=False):

    url = path.join(base_url, season_subfolder_format(season), event_summary_uri(game_id))
    if verbose:
        info(f"GET {url}")
    r = requests.get(url)

    if verbose:
        info("Success!" if r.status_code == 200 else "Failed!!!")

    event_summary_soup = None
    if r.status_code == 200:
        event_summary_soup = BeautifulSoup(r.content, "lxml")
    else:
        logging.warning("Response failed for Event Summary returning None")

    url = path.join(base_url, season_subfolder_format(season), game_summary_uri(game_id))
    if verbose:
        info(f"GET {url}")
    r = requests.get(url)

    if verbose:
        info("Success!" if r.status_code == 200 else "Failed!!!")

    game_summary_soup = None
    if r.status_code == 200:
        game_summary_soup = BeautifulSoup(r.content, "lxml")
    else:
        logging.warning("Response failed for Game Summary returning None")

    return DataSoup(event_summary_soup, game_summary_soup)


@dataclass
class GameInfo:
    date: str
    visitor: str
    home: str
    game_id: int
    status: str


def game_info_from_soup(game_id, data_soup):
    event_summary_soup = data_soup.event_summary
    game_info_soup = event_summary_soup.find(id="GameInfo")
    game_info_df = read_html(game_info_soup.prettify(), flavor="bs4")[0]
    date_found = False
    i = 1
    date_str = ""
    while not date_found:
        candidate_str = game_info_df.loc[i, 0]
        try:
            date_str = to_datetime(candidate_str).isoformat().split('T')[0]
            date_found = True
        except ParserError:
            warning(f"{candidate_str} in {game_id} is not a date trying next one")
            i += 1
        except ValueError:
            warning(f"{candidate_str} in {game_id} is not a date trying next one")
            i += 1

    status_str = game_info_df.loc[game_info_df.shape[0]-1, 0].lower()

    visitor_team_name_table = event_summary_soup.find(id="Visitor")
    visitor_teamname_df = read_html(visitor_team_name_table.prettify(), flavor="bs4")[0]
    visitor_teamname = []
    for w in visitor_teamname_df.loc[3, 0].split(" "):
        if w.upper() == w:
            visitor_teamname.append(w)
        else:
            visitor_teamname = " ".join(visitor_teamname)
            break

    home_team_name_table = event_summary_soup.find(id="Home")
    home_teamname_df = read_html(home_team_name_table.prettify(), flavor="bs4")[0]
    home_teamname = []
    for w in home_teamname_df.loc[3, 0].split(" "):
        if w.upper() == w:
            home_teamname.append(w)
        else:
            home_teamname = " ".join(home_teamname)
            break

    return GameInfo(
        date_str,
        visitor_teamname,
        home_teamname,
        game_id,
        status_str
        )

@dataclass
class GameReport:
    game_info: GameInfo
    player_stats: dict


def stats_from_soup(game_info, datasoup):
    event_summary_soup = datasoup.event_summary
    dfs_of_table = read_html(
        event_summary_soup.find_all(
            "td",
            class_='lborder + rborder + bborder + visitorsectionheading'
        )[0].parent.parent.prettify(), flavor="bs4")[0]

    visitor_team_starting_point = 2
    break_point, end_point = dfs_of_table.loc[dfs_of_table[0] == "TEAM TOTALS"].index
    home_team_starting_point = break_point + 5
    visitor_team_stats_df = dfs_of_table.loc[list(range(visitor_team_starting_point, break_point))]
    home_team_stats_df = dfs_of_table.loc[list(range(home_team_starting_point, end_point))]

    skater_columns = [
        "number",
        "position",
        "name",
        "G",
        "A",
        "P",
        "+/-",
        "PN",
        "PIM",
        "TOT",
        "SHF",
        "AVG TOI/SH",
        "PP",
        "SH",
        "EV",
        "S",
        "A/B",
        "MS",
        "HT",
        "GV",
        "TK",
        "BS",
        "FW",
        "FL",
        "F%"
    ]

    visitor_team_stats_df.columns = skater_columns
    home_team_stats_df.columns = skater_columns

    visitor_team_stats_df["team"] = game_info.visitor
    home_team_stats_df["team"] = game_info.home

    goalies_df = read_html(
        datasoup.game_summary.find_all(
            "td",
            class_="lborder + rborder + bborder + visitorsectionheading"
        )[0].parent.parent.prettify(), flavor="bs4")[0]

    goalie_info_columns = [0, 1, 2]
    goalie_toi_columns = goalies_df.columns[goalies_df.loc[0] == "TOI"]
    goalie_goals_shots_columns = goalies_df.columns[
        (goalies_df.loc[0] == "GOALS-SHOTS AGAINST") |
        (goalies_df.loc[0] == "BUTS-LANCERS  GOALS-SHOTS AGAINST")
    ]
    goalie_tot_goals_shots_column = goalie_goals_shots_columns[goalies_df.loc[1, goalie_goals_shots_columns] == "TOT"]
    goalie_column_idxs = goalie_info_columns + goalie_toi_columns.to_list() + goalie_tot_goals_shots_column.to_list()
    goalie_columns = ["number", "position", "name", "EV", "PP", "SH", "TOT", "GSA-TOT"]

    away_team_starting_point = 2
    break_point, end_point = goalies_df.loc[goalies_df[0] == "TEAM TOTALS"].index
    home_team_starting_point = break_point + 4

    away_goalie_df = goalies_df.loc[list(range(away_team_starting_point, break_point)), goalie_column_idxs]
    try:
        away_goalie_df.columns = goalie_columns
    except ValueError:
        print(goalies_df.loc[0])
        print(game_info.game_id)
        raise ValueError
    home_goalie_df = goalies_df.loc[list(range(home_team_starting_point, end_point)), goalie_column_idxs]
    home_goalie_df.columns = goalie_columns

    away_goalie_df["GA"] = 0
    away_goalie_df["SA"] = 0

    home_goalie_df["GA"] = 0
    home_goalie_df["SA"] = 0

    for i in away_goalie_df.loc[~away_goalie_df["GSA-TOT"].isna()].index:
        gsa_tot = away_goalie_df.loc[i, "GSA-TOT"]
        away_goalie_df.loc[i, ["GA", "SA"]] = gsa_tot.split("-")

    goalie_columns = ["EV", "PP", "SH", "TOT", "GA", "SA"]
    for i, goalie in away_goalie_df.iterrows():
        visitor_goalie_idx = visitor_team_stats_df.loc[visitor_team_stats_df["number"] == goalie["number"]].index
        visitor_team_stats_df.loc[visitor_goalie_idx, goalie_columns] = goalie[goalie_columns].to_list()

    for i in home_goalie_df.loc[~home_goalie_df["GSA-TOT"].isna()].index:
        gsa_tot = home_goalie_df.loc[i, "GSA-TOT"]
        home_goalie_df.loc[i, ["GA", "SA"]] = gsa_tot.split("-")

    home_team_stats_df["GA"] = 0
    home_team_stats_df["SA"] = 0

    for i, goalie in home_goalie_df.iterrows():
        home_goalie_idx = home_team_stats_df.loc[home_team_stats_df["number"] == goalie["number"]].index
        home_team_stats_df.loc[home_goalie_idx, goalie_columns] = goalie[goalie_columns].to_list()

    final_df = visitor_team_stats_df.append(home_team_stats_df, ignore_index=True).fillna(0)
    return final_df.to_dict(orient="list")