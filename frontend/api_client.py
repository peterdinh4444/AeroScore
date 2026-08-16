import requests
from settings import *
 

def submit_score(player_name, player_score):
    try: 
        response = requests.post(
            f"{BASE_API_URL}/api/score",
            json = {"player_name": player_name, "player_score": player_score},
            timeout=60
            )

        response.raise_for_status()
        return response.status_code in (200,201)
    except requests.exceptions.RequestException as e:
        print(f"Failed to submit score: {e}")
        return False


def get_leaderboard():
    try:
        response = requests.get(f"{BASE_API_URL}/api/leaderboard", timeout=2)
        if response.status_code == 200: return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch leaderboard: {e}")
        return []

