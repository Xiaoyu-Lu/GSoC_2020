#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:19:39 2020

this script can build the speakers' database 
e,g, {speaker1: {birthday:yy-mm-dd, gender: female}, 
      speaker2: {..} ,
      ...
      }

@author: loewi
"""
import sys
import json
import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import quote
from urllib.request import urlopen  

DB_PATH = "./output/archive/speaker_db.json"
if os.path.exist(DB_PATH):
    with open(DB_PATH, 'r') as f:
        SPEAKER_DB = json.load(f)

def get_name_set(json_file):
    year = json_file.split('.')[0][-4:]
    name_set = set()
    with open(json_file,'r') as f:
        tmp_dict = json.load(f) 
        for file, name_dict in tmp_dict.items():
            name_set.update(name_dict.keys())
    
    return year, name_set

def search_dbpedia(name):
    """
    Extract the speaker's gender and birthday from dbpedia

    Parameters
    ----------
    name : string
        DESCRIPTION.


    Returns
    -------
    res_gender: string
        DESCRIPTION.
    res_birth: string
        DESCRIPTION.

    """
    res_gender, res_birth = '', '' 
    
    try: 
        temp_string = "http://dbpedia.org/page/" + name
    
        html = requests.get(temp_string).text
        
        html_soup = BeautifulSoup(html,'html.parser')
        res_gender = html_soup.find("span", property="foaf:gender")
        res_birth = html_soup.find("span", property="dbo:birthDate")

        if not res_gender:
            res_gender = backup_search(name, gender=True, bdate=False)
        else:
            res_gender = res_gender.text
        if not res_birth:
            res_birth = backup_search(name)
        else:
            res_birth = res_birth.text
        
    except:
        pass
        
    return  res_gender if res_gender else "None" , res_birth if res_birth else "None"

def backup_search(name, gender=False, bdate=True):
    """
    If cannot find gender/bdate on dbpedia, search on live.dpedia.

    Parameters
    ----------
    name : string
        DESCRIPTION.
    gender : string, optional
        DESCRIPTION. The default is False.
    bdate : string, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    string
        DESCRIPTION.

    """
    try: 
        tmp = "http://live.dbpedia.org/data/"+quote(name)+".json"
        url = urlopen(tmp)
        data = json.load(url)

        # print(data)
        for name, info in data.items():
            if gender:
                if 'http://xmlns.com/foaf/0.1/gender' in info.keys():
                    gender = info['http://xmlns.com/foaf/0.1/gender'][0]['value']
                    return gender
            if bdate:
                if 'http://live.dbpedia.org/ontology/birthDate' in info.keys():
                    date = info['http://live.dbpedia.org/ontology/birthDate'][0]['value']
                    return date
    except:
        return "None"

            
def _add(speaker_dict, key, key_a, val_a, key_b, val_b): 
    if key in speaker_dict:
        if key_a not in speaker_dict[key] or key_b not in  speaker_dict[key]:
            speaker_dict[key].update({key_a: val_a, key_b: val_b})
    else:
        speaker_dict.update({key:{key_a: val_a, key_b: val_b}})
    return speaker_dict

          
def build_person_db(year, name_set):
    """
    search DBpedia to get birthdate and gender of the speakers
    skip the name which is appeared in SPEAKER_DB  
    """
    speaker_dict = {}
    
    with open(f'./output/speaker_db_{year}.json', 'w') as fp:
        count = 0
        for name in name_set:
            if os.path.exist(DB_PATH) and not name in SPEAKER_DB:
                # print(name)
                gender, bdate = search_dbpedia(name)
                # print(gender, bdate)
                speaker_dict = _add(speaker_dict, name, 'birth_date', bdate,  'gender', gender)
            count +=1
            print(count)

        json.dump(speaker_dict, fp, sort_keys=True, indent=4, ensure_ascii=False)

        # merge the new one to the old one
        # SPEAKER_DB.update(speaker_dict) 
        # with open(DB_PATH, 'r') as f:
        #     json.dump(SPEAKER_DB, f, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == "__main__":

    # yr = '2018'
    # json_file = f'./corpus_{yr}.json'
    # print(json_file)
    # year, name_set = get_name_set(json_file)
    # build_person_db(yr, name_set)
    args = sys.argv
    if len(args) != 2:
        raise Exception("not valid ")
    else:
        json_file = args[1]
        print(f'{json_file} processing...')
        year, name_set = get_name_set(json_file)
        build_person_db(yr, name_set)




    