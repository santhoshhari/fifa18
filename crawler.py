import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

col_names = ['ID', 'Name', 'FullName', 'Age', 'Nationality', 'Club', 'Image', 'Position', 'Overall', 'Potential',
           'Value', 'Wage', 'URL']
data = pd.DataFrame(columns=col_names)


def get_player_url(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    player_image_list = soup.findAll('img', attrs={'class': 'player-check'})
    player_image = [pim['data-src'] for pim in player_image_list]
    player_id = [pim['id'] for pim in player_image_list]
    player_details = soup.findAll('div', attrs={'class': 'col-name'})
    player_profile = [pld for i, pld in enumerate(player_details) if i % 2 == 0]
    club_details = [pld for i, pld in enumerate(player_details) if i % 2 == 1]
    player_country = [pld.findAll('a')[0]['title'] for pld in player_profile]
    player_club = [pld.findAll('a')[0].text.strip() for pld in club_details]
    player_name = [pld.findAll('a')[1].text.strip() for pld in player_profile]
    player_fname = [pld.findAll('a')[1]['title'] for pld in player_profile]
    player_url = [url + pld.findAll('a')[1]['href'] for pld in player_profile]
    player_position_list = [pld.findAll('a')[2:] for pld in player_profile]
    player_position = []
    for pplist in player_position_list:
        player_position.append([elem.text.strip() for elem in pplist])


    player_overall_list = soup.findAll('div', attrs={'class': 'col-digit col-oa'})
    player_overall = [oa.find('span').text.strip() for oa in player_overall_list]
    player_poten_list = soup.findAll('div', attrs={'class': 'col-digit col-pt'})
    player_poten = [pt.find('span').text.strip() for pt in player_poten_list]
    player_age = [pa.text.strip() for pa in soup.findAll('div', attrs={'class': 'col-digit col-ae'})]
    player_value = [val.text.strip() for val in soup.findAll('div', attrs={'class': 'col-digit col-vl'})]
    player_wage = [wg.text.strip() for wg in soup.findAll('div', attrs={'class': 'col-digit col-wg'})]

    data_list = [player_id, player_name, player_fname, player_age, player_country, player_club,
                                    player_image, player_position, player_overall, player_poten, player_value,
                                    player_wage, player_url]

    player_df = pd.DataFrame(list(zip(*data_list)), columns=col_names)

    return player_df


url = 'https://sofifa.com/players'
temp_df = get_player_url(url)
count = 0

while temp_df.shape[0] != 0:
    time.sleep(2)
    data = data.append(temp_df, ignore_index=True)
    count += 80
    temp_df = get_player_url(url + '?offset=' + str(count))

data.to_csv('player_data.txt', encoding='utf-8')
