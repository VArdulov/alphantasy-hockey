from fantasy.scraping.utils import (
    get_summary_soups,
    game_info_from_soup,
    stats_from_soup,
    GameReport
)
# from typing import List, Union
from logging import warning
from datetime import datetime
max_number_of_games_in_a_season = 31 * 82
current_year = datetime.now().year


def scrape_game( seasons=current_year, game_ids="all", verbose=False):
    if isinstance(game_ids, int):
        game_ids = [game_ids]
    elif game_ids == "all":
        game_ids = list(range(1, max_number_of_games_in_a_season+1))

    if isinstance(seasons, int):
        seasons = [seasons]
    elif seasons == "all":
        seasons = list(range(2008, current_year))
    game_reports = dict()
    for season in seasons:
        worked = True
        i = 0
        game_reports[season] = dict()
        while worked and i < len(game_ids):
            gid = game_ids[i]
            game_report = _get_game_report(season, gid)
            if game_report is not None:
                game_reports[season][gid] = game_report
                i += 1
                if verbose > 9:
                    if i % 10 == 0:
                        print(f"processed {i} games")
            else:
                worked = False
        if verbose:
            print(f"Processed {len(game_reports[season])} games for {season} season")

    return game_reports


def _get_game_report(season, game_id, verbose="warn"):
    summary_soups = get_summary_soups(season, game_id, verbose=verbose)
    if (summary_soups.game_summary is not None) and (summary_soups.event_summary is not None):
        game_info = game_info_from_soup(game_id, summary_soups)
        stats_dict = stats_from_soup(game_info, summary_soups)
        return GameReport(game_info, stats_dict)

    if verbose == "warn":
        warning(f"Unable to process {season} - id: {game_id:04d}, returning None")

    return None
