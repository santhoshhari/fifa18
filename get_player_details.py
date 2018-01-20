import sys
import requests
import random
import time
from bs4 import BeautifulSoup
import pandas as pd

f_name = sys.argv[1]
player_list = pd.DataFrame.from_csv(f_name, header=1)
col_names = ['PreferredFoot', 'InternationalReputation', 'WeakFoot', 'SkillMoves', 'WorkRate', 'BodyType', 'RealFace',
             'ReleaseClause']
data = pd.DataFrame(columns=col_names)


def get_player_detail(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    attr_list = dict()
    web = [elem[1].text for elem in enumerate(soup.findAll('script')) if 'pointPAC' in elem[1].text][0]
    attr_list['general_pace'] = web[web.find('pointPAC') + 11:web.find('pointPAC') + 13]
    attr_list['general_shot'] = web[web.find('pointSHO') + 11:web.find('pointSHO') + 13]
    attr_list['general_pass'] = web[web.find('pointPAS') + 11:web.find('pointPAS') + 13]
    attr_list['general_dribble'] = web[web.find('pointDRI') + 11:web.find('pointDRI') + 13]
    attr_list['general_defend'] = web[web.find('pointDEF') + 11:web.find('pointDEF') + 13]
    attr_list['general_physical'] = web[web.find('pointPHY') + 11:web.find('pointPHY') + 13]
    attr = soup.findAll('div', attrs={'class': 'column col-3 mb-20'})
    for elem in enumerate(attr):
        cat = elem[1].find('h5').text.lower()
        if cat == 'traits':
            traits = [e[1].text.lower() for e in enumerate(elem[1].findAll('li'))]
        else:
            for e in enumerate(elem[1].findAll('li')):
                attr_list[cat+'_'+e[1].text.strip().split(' ', 1)[1].lower().replace(" ", "_")] = \
                    e[1].text.strip().split(' ', 1)[0]

    high_attr = soup.findAll('div', attrs={'class': 'teams'})
    for e in enumerate(high_attr[0].findAll('ul', attrs={'class': 'pl'})[0].findAll('li')[:5]):
        attr_list[e[1].text.strip().split('\n')[0].lower().replace(" ", "_")] = \
            e[1].text.strip().split('\n')[1].lower()


    return None


try:
    for player_url in player_list['URL']:
        data = data.append(get_player_detail(player_url), ignore_index=True)
except:
    data.to_csv('player_details.txt', encoding='utf-8', index=False)

data.to_csv('player_details.txt', encoding='utf-8', index=False)
