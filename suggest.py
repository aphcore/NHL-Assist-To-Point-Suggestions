import pandas
from dabble import get_props_by_game
import os
import re

FILE_NAME = "dabble.json"
TOP_N = 3

# NHL API team abbreviation: team name
TEAM_ABBR_MAP = {
    "ANA": "Anaheim Ducks",
    "BOS": "Boston Bruins",
    "BUF": "Buffalo Sabres",
    "CGY": "Calgary Flames",
    "CAR": "Carolina Hurricanes",
    "CHI": "Chicago Blackhawks",
    "COL": "Colorado Avalanche",
    "CBJ": "Columbus Blue Jackets",
    "DAL": "Dallas Stars",
    "DET": "Detroit Red Wings",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MTL": "Montreal Canadiens",
    "NJD": "New Jersey Devils",
    "NSH": "Nashville Predators",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins",
    "SEA": "Seattle Kraken",
    "SJS": "San Jose Sharks",
    "STL": "St. Louis Blues",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "UTA": "Utah Mammoth",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets",
    "WSH": "Washington Capitals"
}

# suggest TOP_N players to bet on from correlation data
def suggest_combos_from_cwd():
    # suggest player combos for all CSVs (they must be in the same folder!)
    
    # build dabble props file path from cwd
    cwd = os.getcwd()
    dabble_json = os.path.join(cwd, FILE_NAME)
    
    # load dabble props 
    games = get_props_by_game()
    print(f"Detected games in JSON: {list(games.keys())}")

    # find all CSVs in current folder
    csv_files = [f for f in os.listdir(cwd) if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in current directory")
        return

    for corr_csv in csv_files:
        # extract team abbreviation from CSV filename
        match = re.match(r"([A-Z]+)_.*\.csv", corr_csv)
        if match:
            team_abbr = match.group(1)
        else:
            print(f"Warning: Cannot detect team abbreviation from filename: {corr_csv}")
            continue
        # map abbreviation to full team name 
        if team_abbr not in TEAM_ABBR_MAP:
            print(f"Skipping {team_abbr}: abbreviation not recognized")
            continue

        team_name = TEAM_ABBR_MAP[team_abbr]

        # load correlation CSV
        corr_df = pandas.read_csv(corr_csv, index_col=0)

        # collect all players in JSON that match this team
        prop_players = []
        for matchup, props in games.items():
            if team_name in matchup:
                prop_players.extend([p[0] for p in props])

        # filter players with props and in CSV
        available_players = [p for p in prop_players if p in corr_df.index]
        if not available_players:
            print(f"\nNo props for players on {team_name} ({team_abbr})")
            continue

        # get TOP_N correlations
        top_pairs = []
        for player in available_players:
            row = corr_df.loc[player].drop(player, errors="ignore").sort_values(ascending=False)
            for teammate, prob in row.head(TOP_N).items():
                if prob > 0:
                    top_pairs.append((player, teammate, prob))

        top_pairs = sorted(top_pairs, key=lambda x: x[2], reverse=True)

        print(f"\n=== Suggested player combos for {team_name} ({team_abbr}) ===")
        if top_pairs:
            for a, b, prob in top_pairs:
                print(f"{a} → {b}: {prob:.2f}")
        else:
            print("No significant correlations found")


if __name__ == "__main__":
    suggest_combos_from_cwd()