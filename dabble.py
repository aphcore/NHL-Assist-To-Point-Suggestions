import json
from collections import defaultdict

FILE_NAME = "dabble.json"
TARGET_MARKETS = {"Player Goals", "Player Assists", "Player Points"}

def get_props_by_game():
    # group all props by matchup
    with open(FILE_NAME, "r") as f:
        raw_data = json.load(f)

    games = defaultdict(list)

    for entry in raw_data:
        json_list = entry.get("result", {}).get("data", {}).get("json", [])
        for p in json_list:
            market = p.get("market", "")
            if market not in TARGET_MARKETS:
                continue

            home = p.get("homeTeam", "Unknown Home").strip()
            away = p.get("awayTeam", "Unknown Away").strip()
            player = p.get("participant", "Unknown Player").strip()
            selection = p.get("selection", "").strip()

            if not player:
                continue

            matchup_key = f"{home} @ {away}"
            games[matchup_key].append((player, market, selection))

    return games

# print props grouped by game
def print_props(games):
    for matchup, props in games.items():
        print(f"\n=== {matchup} ===")
        for player, market, selection in props:
            print(f"{player} – {market} ({selection})")

# don't wanna rerun dabble stuff when we import it in suggest.py

if __name__ == "__main__":
    games = get_props_by_game()
    print_props(games)
