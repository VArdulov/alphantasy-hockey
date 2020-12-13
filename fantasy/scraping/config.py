base_url = "http://www.nhl.com/scores/htmlreports/"
season_subfolder_format = lambda year: f"{year}{year+1}"
event_summary_uri = lambda game_id: f"ES02{game_id:04d}.HTM"
game_summary_uri = lambda game_id: f"GS02{game_id:04d}.HTM"
