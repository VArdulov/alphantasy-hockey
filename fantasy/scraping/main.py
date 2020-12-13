from argparse import ArgumentParser
from fantasy.scraping.scraper import current_year, scrape_game

parser = ArgumentParser()
parser.add_argument("--output", "-o", type=str, help="Which directory to save the final json dictionary to")
parser.add_argument(
    "--season",
    type=int,
    default=(current_year - 1),
    help=f"Which season (starting year) should the data collect data from"
)
parser.add_argument("--game-id", type=int, default="all", nargs="+", help="Which games to process, default = all")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.output:
        print(f"output = {args.output}")
    print(f"season: {args.season}")

