import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

url = 'https://www.vlr.gg/rankings/north-america'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

team_div = soup.find('div', class_='mod-scroll')
team_items = team_div.find_all('div', class_='rank-item')

data = []
stats = []
for i, team in enumerate(team_items[:1]):
    team_rank = team.find('div', class_='rank-item-rank-num').get_text(strip=True)
    team_name_elem = team.find('div', class_='ge-text')

    for span in team_name_elem.find_all('span'):
        span.extract()

    for country in team_name_elem.find_all(class_='rank-item-team-country'):
        country.extract()

    team_name = team_name_elem.get_text(strip=True)
    team_href = team.find('a', class_='rank-item-team')
    href = 'https://www.vlr.gg' + team_href.get('href')
    team_response = requests.get(href)
    team_soup = BeautifulSoup(team_response.content, 'html.parser')
    
    team_igl = ''
    managers = []
    coaches = []
    players = []
    team_roster = team_soup.find_all('div', class_='team-roster-item')

    for player in team_roster:
        alias = player.find('div', class_='team-roster-item-name-alias')
        if alias is not None:
            player_name = alias.text.strip()
        else:
            player_name = player.text.strip()

        role = player.find('div', class_='team-roster-item-name-role')
        
        if role is not None:
            role_text = role.text.strip()
            if 'coach' in role_text.lower():
                coaches.append(player_name)
                continue
            elif 'manager' in role_text.lower():
                managers.append(player_name)
                continue

        if player.find('i', class_='fa-star') is not None:
            team_igl = player_name
        else:
            players.append(player_name)

        player_href = player.find('a').get('href')
        player_url = 'https://www.vlr.gg' + player_href
        player_url60 = player_url + '/?timespan=60d'
        # print(player_url60)

        player_response = requests.get(player_url60)
        player_soup = BeautifulSoup(player_response.content, 'html.parser')
        table = player_soup.find('table')
        # print(table)
        
        player_stats = []
        rows = table.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            cells = row.find_all('td')
            agent = cells[0].find('img')['alt']
            usage = cells[1].text.strip()
            rounds_played = cells[2].text.strip()
            rating = cells[3].text.strip()
            avg_combat_score = cells[4].text.strip()
            kd_ratio = cells[5].text.strip()
            avg_damage_per_round = cells[6].text.strip()
            kast = cells[7].text.strip()
            kpr = cells[8].text.strip()
            apr = cells[9].text.strip()
            fkpr = cells[10].text.strip()
            fdpr = cells[11].text.strip()
            kills = cells[12].text.strip()
            deaths = cells[13].text.strip()
            assists = cells[14].text.strip()
            first_bloods = cells[15].text.strip()
            first_deaths = cells[16].text.strip()

            # Create a dictionary to store the extracted data
            row_data = {
                'Alias': player_name,
                'Agent': agent,
                'Usage': usage,
                'Rounds Played': rounds_played,
                'Rating': rating,
                'Average Combat Score': avg_combat_score,
                'Kills:Death': kd_ratio,
                'Average Damage per Round': avg_damage_per_round,
                'Kill, Assist, Survive, Trade %': kast,
                'Kills Per Round': kpr,
                'Assists Per Round': apr,
                'First Kills Per Round': fkpr,
                'First Deaths Per Round': fdpr,
                'Kills': kills,
                'Deaths': deaths,
                'Assists': assists,
                'First Bloods': first_bloods,
                'First Deaths': first_deaths
            }

            # Add the row data to the list
            player_stats.append(row_data)

        # Print the extracted data
        for row_data in player_stats:
            print(row_data)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

#     data.append([team_rank, team_name, team_igl, players, managers, coaches, href])
    

# df = pd.DataFrame(data, columns=['Rank', 'Team', 'Team Leader', 'Players', 'Manager', 'Coach(es)','Link'])

# print(df)