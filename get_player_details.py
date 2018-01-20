import sys
import requests
import random
import time
from bs4 import BeautifulSoup
import pandas as pd

if len(sys.argv) == 1:
    f_name = 'player_data.txt'
else:
    f_name = sys.argv[1]

target_file_name = 'player_details.txt'

player_list = pd.DataFrame.from_csv(f_name)
# target = pd.DataFrame.from_csv(target_file_name)

col_names = ['attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 'attacking_short_passing',
             'attacking_volleys', 'defending_marking', 'defending_sliding_tackle', 'defending_standing_tackle',
             'general_defend', 'general_dribble', 'general_pace', 'general_pass', 'general_physical', 'general_shot',
             'goalkeeping_gk_diving', 'goalkeeping_gk_handling', 'goalkeeping_gk_kicking', 'goalkeeping_gk_positioning',
             'goalkeeping_gk_reflexes', 'id', 'international_reputation', 'mentality_aggression', 'mentality_composure',
             'mentality_interceptions', 'mentality_penalties', 'mentality_positioning', 'mentality_vision',
             'movement_acceleration', 'movement_agility', 'movement_balance', 'movement_reactions',
             'movement_sprint_speed', 'position_cam', 'position_cb', 'position_cdm', 'position_cf', 'position_cm',
             'position_lam', 'position_lb', 'position_lcb', 'position_lcm', 'position_ldm', 'position_lf',
             'position_lm', 'position_ls', 'position_lw', 'position_lwb', 'position_ram', 'position_rb', 'position_rcb',
             'position_rcm', 'position_rdm', 'position_rf', 'position_rm', 'position_rs', 'position_rw', 'position_rwb',
             'position_st', 'power_jumping', 'power_long_shots', 'power_shot_power', 'power_stamina', 'power_strength',
             'preferred_foot', 'qualities', 'skill_ball_control', 'skill_curve', 'skill_dribbling',
             'skill_fk_accuracy', 'skill_long_passing', 'skill_moves', 'traits', 'weak_foot', 'work_rate']

data = pd.DataFrame(columns=col_names)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_player_detail(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    attr_dict = dict()
    attr_dict['id'] = url[url.find('/player/') + 8:]
    web = [elem[1].text for elem in enumerate(soup.findAll('script')) if 'pointPAC' in elem[1].text][0]
    attr_dict['general_pace'] = web[web.find('pointPAC') + 11:web.find('pointPAC') + 13]
    attr_dict['general_shot'] = web[web.find('pointSHO') + 11:web.find('pointSHO') + 13]
    attr_dict['general_pass'] = web[web.find('pointPAS') + 11:web.find('pointPAS') + 13]
    attr_dict['general_dribble'] = web[web.find('pointDRI') + 11:web.find('pointDRI') + 13]
    attr_dict['general_defend'] = web[web.find('pointDEF') + 11:web.find('pointDEF') + 13]
    attr_dict['general_physical'] = web[web.find('pointPHY') + 11:web.find('pointPHY') + 13]
    attr = soup.findAll('div', attrs={'class': 'column col-3 mb-20'})
    for elem in enumerate(attr):
        try:
            cat = elem[1].find('h5').text.lower()
            if cat == 'traits':
                attr_dict['traits'] = [e[1].text.lower() for e in enumerate(elem[1].findAll('li'))]
            else:
                for e in enumerate(elem[1].findAll('li')):
                    attr_dict[cat + '_' + e[1].text.strip().split(' ', 1)[1].lower().replace(" ", "_")] = \
                        e[1].text.strip().split(' ', 1)[0]
        except:
            attr_dict['traits'] = 'na'

    high_attr = soup.findAll('div', attrs={'class': 'teams'})
    for e in enumerate(high_attr[0].findAll('ul', attrs={'class': 'pl'})[0].findAll('li')[:5]):
        attr_dict[e[1].text.strip().split('\n')[0].lower().replace(" ", "_").strip()] = \
            e[1].text.strip().split('\n')[1].lower()

    attr_dict['qualities'] = soup.findAll('div', attrs={'class': ''})[1].text.strip().lower().split(u"\xa0#")

    try:
        for row in soup.find("table", attrs={'class': 'table-hover'}).find('tbody').findAll('tr'):
            col = row.findAll('td')
            pos = col[0].text.strip().replace('\n', ' ')
            val = col[1].text.strip()
            for p in pos.lower().split(' '):
                attr_dict['position_' + p] = val
    except:
        attr_dict.update(
            dict(position_cam='-1', position_cb='-1', position_cdm='-1', position_cf='-1', position_cm='-1',
                 position_lam='-1', position_lb='-1', position_lcb='-1', position_lcm='-1', position_ldm='-1',
                 position_lf='-1', position_lm='-1', position_ls='-1', position_lw='-1', position_lwb='-1',
                 position_ram='-1', position_rb='-1', position_rcb='-1', position_rcm='-1', position_rdm='-1',
                 position_rf='-1', position_rm='-1', position_rs='-1', position_rw='-1', position_rwb='-1',
                 position_st='-1'))

    return attr_dict


# pl_id = list(player_list['URL'].apply(lambda x: x[x.find('/player/') + 8:]))
# data = target.copy()

try:
    for player_url in player_list['URL']:
        #if player_url[player_url.find('/player/') + 8:] not in pl_id:
        time.sleep(random.randrange(1, 50) / 100.0)
        data = data.append(get_player_detail(player_url), ignore_index=True)
except Exception, e:
    print 'Error: ' + str(e)
    data.to_csv(target_file_name, encoding='utf-8', index=False)

if len(data) == len(player_list):
    data.to_csv(target_file_name, encoding='utf-8', index=False)
