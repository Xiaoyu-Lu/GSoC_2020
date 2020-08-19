#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:59:36 2020

@author: loewi

use speaker's info db and make a cleaned vesion of the corpus_year.json

"""
import json
import datetime
import sys

ROOT_DIR = './output/archive'
SPEAKER_DB = f'{ROOT_DIR}/speaker_db.json'

def validate(date_text):
    """
    Return True if the date is valid, otherwise, return False.

    Parameters
    ----------
    date_text : string
        '2011-08-09'

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """

    try:
        if date_text[-3:] == "0-0":
            date_text = date_text.replace("0-0", "1-1")
        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False          
                    
                    
def convert_date(string):
    """
    Change the format of the string date into datetime date.
    
    Parameters
    ----------
    string : str 
        e.g.'2011-08-09'
        
    Returns
    -------
    datetime.date(2011, 8, 9)

    """
        
    yy, mm, dd = map(int, string.split("-"))

    return datetime.date(yy, mm, dd)


def calculate_age(end_date, birth_date):
    """
    Calculate the age.

    Parameters
    ----------
    end_date : str
        e.g. '2011-08-09'
    birth_date : str.
        e.g. '1982-01-01'

    Returns
    -------
    age e.g. 29

    """
    time_diff = convert_date(end_date) - convert_date(birth_date)
    return int(time_diff.days/365.2425)


def _add(person_dict, key, key_a, val_a, key_b, val_b, key_c, val_c): 
    """dictionary helper function"""
    if key in person_dict:
        if key_a not in person_dict[key] or key_b not in  person_dict[key] or key_c not in person_dict[key]:
            person_dict[key].update({key_a: val_a, key_b: val_b, key_c: val_c})
    else:
        person_dict.update({key:{key_a: val_a, key_b: val_b, key_c: val_c}})
    return person_dict


def corpusBuilder(path):
    """
    Clear out the speaker whose birthday is unknown from the corpus.

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    file_dict : dictionary
        DESCRIPTION.

    """
    file_dict = {}
    with open(path) as f:
        with open(SPEAKER_DB, 'r') as db_f:
            data = json.load(f)
            speaker_db = json.load(db_f)
            for file_name, speakers in data.items():

                end_date = file_name[:10]

                if not validate(end_date): continue
            
                speaker_info = {}
                for speaker, info_dict in speakers.items():

                    bdate = speaker_db[speaker]["birth_date"]
                    if (not speaker.isupper()) and speaker in speaker_db and validate(bdate):
                        # print(speaker, end_date, bdate)
                        age = calculate_age(end_date, bdate)
                        if age <= 100:
                            speaker_info = _add(speaker_info, speaker, 'age', age, 'time', info_dict["time"], 'gender', speaker_db[speaker]["gender"])
    
                if speaker_info:
                    file_dict[file_name] = speaker_info
                
    return file_dict

if __name__ == "__main__":
    # yrs = ["2018"]
    #     for yr in yrs:
    #         with open('./lean_corpus_'+yr+'.json', 'w') as fp:
    #             path = './corpus_'+yr+'.json'
    #             file_dict = corpusBuilder(path)
    #             json.dump(file_dict, fp, sort_keys=True, indent=4, ensure_ascii=False)

    args = sys.argv
    if len(args) != 3:
        raise Exception("not valid ")
    else:
        json_path = args[1]
        output = args[2]
        with open(output, 'w') as fp:
            file_dict = corpusBuilder(json_path)
            json.dump(file_dict, fp, sort_keys=True, indent=4, ensure_ascii=False)

