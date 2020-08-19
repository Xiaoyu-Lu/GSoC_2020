#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 22:09:24 2020

@author: loewi
"""
import re
import json
import collections
import sys

def check_gentle(gentle_file):
    """
    Some gentle could be empty

    """
    # nested replace() 
    with open(gentle_file, encoding='utf-8') as f:
        tmp = f.read().replace('\t','').replace('\n','').replace(',}','}').replace(',]',']').replace('"','\"')
        data = json.loads(tmp)
        
    return data

def read_gentle(gentle_file):
    """
    Eextract the transcript and aligned words from gentle json file 

    Parameters
    ----------
    gentle_file : json
        {
            "transcript": ...,
            "words": [{...},{...},...]
        }
    Returns
    -------
    transcript : string
        DESCRIPTION.
    words : list of dictionary
        DESCRIPTION.

    """
    # nested replace() 
    with open(gentle_file, encoding='utf-8') as f:
        tmp = f.read().replace('\t','').replace('\n','').replace(',}','}').replace(',]',']').replace('"','\"')
        data = json.loads(tmp)

    transcript = data["transcript"]
    words = data["words"]
    
    return transcript, words


def create_start_index_dict(words):
    """
    Convert list of dict into a dictionary (key=startOffset, value=index in the list)

    Parameters
    ----------
    words : list of dict
    [ {
          "alignedWord": "the",
          "case": "success",
          "end": 28.739999,
          "endOffset": 38,
          "phones": [
            {
              "duration": 0.01,
              "phone": "dh_B"
            },
            {
              "duration": 0.01,
              "phone": "ah_E"
            }
          ],
          "start": 28.719999,
          "startOffset": 35,
          "word": "The"
        },
        {
          "case": "not-found-in-audio",
          "endOffset": 52,
          "startOffset": 46,
          "word": "regime"
        },
        ...
        ]

    Returns
    -------
    start_dict : dictionary
        {35:1, 46:2, ...}

    """
    start_dict = collections.defaultdict()
    for i, word_info in enumerate(words):
        start_dict[word_info["startOffset"]] = i
    return start_dict
    

def extract_txt_from_line(line):
    """
    Extract raw txt from a line 
    ALMOST THE SAME AS THE SCRIPT (Barbara Butz, Karoline Plum, Patricia Windler, (Hannah Westerhagen))
    WHICH IS USED IN THE FORCE ALIGNMENT (gentle)
    
    Parameters
    ----------
    line : string
        e.g. "20180415100001.233|20180415100002.701|CC1|>>> UNIDENTIFIED MALE: Precise,"
        
    Returns
    -------
    string
        e.g. "Precise,"

    """  
    text = ""
    match = re.findall(".*CC1\|(.*)", line)
    if len(match) > 0:
        text = match[0]
        if not text.isupper():
            # delete [06:55:05] 
            text = re.sub("\[.*\]", "", text)
            
            if text.startswith(">"):
                index = text.rfind(":")
                text = text[index + 1:]

            text = text.replace(">>>", "")
            return " ".join(text.split())

    return ""


def extract_txt_from_lines(lines):
    """
    Extract raw txt from list of lines 

    Parameters
    ----------
    lines : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    texts = []
    for line in lines:
        if "|CC1|" in line:
            texts.append(extract_txt_from_line(line))
    
    return " ".join([t for t in texts if t])


def process_person_line(line):
    """
    Read and process the line contains the speaker
    e.g. 20120911190001.900|20120911190133.626|NER_01|Person=Martin Savidge|Role=CNN ANCHOR

    Parameters
    ----------
    line : string
        DESCRIPTION.

    Returns
    -------
    (starttime, endtime): tuple
        DESCRIPTION.
    person : string
        DESCRIPTION.
    role : string
        DESCRIPTION.

    """

    tokens = line.split("|")
    starttime, endtime = tokens[0], tokens[1]
    person_tmp = re.sub("\[.*\]", "", tokens[3])
    person_tmp = re.sub("_", " ", person_tmp)
    person = person_tmp[7:].strip().replace(' ','_')

    if "UNIDENTIFIED" in person:
        person = "UNKNOWN"
    if "Role=" in line:
        role = tokens[4][5:]
    else:
        role = "UNKNOWN"
    return (starttime, endtime), person, role


def read_tpt(tpt_file):
    """
    read the tpt file and return list of lines

    Parameters
    ----------
    tpt_file : string
        path of the file.

    Returns
    -------
    lines : list of strings
        DESCRIPTION.

    """
    with open(tpt_file,'r', encoding="utf-8", errors="ignore") as f:
      
      file_name = tpt_file.split("/")[-1][:-4]
      print("{} tpt processing ...".format(file_name))
    
      lines = f.read().splitlines()
      
    return lines 


def get_speakers(gentle_file, tpt_file):
    """
    1. extract the script of each speaker
    2. get the first letter index of each script in the transcript
    3. convert the index into the position of the words list from gentle

    Parameters
    ----------
    gentle_file : json
        DESCRIPTION.
    tpt_file : txt
        DESCRIPTION.

    Returns
    -------
    two lists should have the same length
        one contains the speakers name, 
        another contains the index of the first word

    """

    transcript, words = read_gentle(gentle_file)

    start_dict = create_start_index_dict(words)
    
    def extract_index(text_idx):
        if text_idx not in start_dict:
            return -1
        return start_dict[text_idx]
    
    lines = read_tpt(tpt_file)
    person_index_list = []
    person_list = []
    for i, line in enumerate(lines):

         if 'NER_01|Person=' in line:
            _, person, _ = process_person_line(line)
            person_index_list.append(i)
            person_list.append(person)
        
    n, idx = 0, 0
    starter_list = []   # INDEX OF THE FIRST LETTER OF THE SPEAKER
    
    for i in range(1, len(person_index_list)):
    
        start, end = person_index_list[i-1], person_index_list[i]
        # print(person_list[i-1])
        extracted_text = extract_txt_from_lines(lines[start+1:end])
        # print(extracted_text, idx)
        text_idx = transcript.find(extracted_text, idx)
        start_idx = extract_index(text_idx)
        starter_list.append(start_idx)
        
        n = len(extracted_text)
        # JUST IN CASE THE TEXT DOES NOT MATCH THE TRANSCRIPT
        if text_idx >= 0:
            idx = text_idx + n
        else:
            text_idx = idx + n
        
    # THE LAST SPEAKER
    i = len(person_index_list)-1
    start = person_index_list[i]
    extracted_text = extract_txt_from_lines(lines[start+1:])
    text_idx = transcript.find(extracted_text, idx)
    
    start_idx = extract_index(text_idx)
    starter_list.append(start_idx)
    
    return person_list, starter_list



def extract_time(gentle_file, tpt_file):
    """
    Return each speaker and the time intervals

    Parameters
    ----------
    gentle_file : json
        DESCRIPTION.
    tpt_file : txt
        DESCRIPTION.

    Returns
    -------
    speaker_dict: dictionary
            {  
             'Aj_Pederson': [[3427.65, 3437.43]],
             'Alex_Whitten': [[3437.43, 3448.679999], [3473.09, 3475.73]],
             'Samantha_Arnold': [[3448.679999, 3457.199999]]
             ...
             })

    """
    
    _, words = read_gentle(gentle_file)
    
    def extract_start(index):
        word_info = words[index]
        if word_info["case"] == "not-found-in-audio":
            return -1
        return word_info["start"]

    def extract_end(index):
        word_info = words[index]
        if word_info["case"] == "not-found-in-audio":
            return -1
        return word_info["end"]
    
    snippets = []
    person_list, starter_list = get_speakers(gentle_file, tpt_file)
    
    for i in range(1, len(starter_list)):
        start = extract_start(starter_list[i-1])
        end = extract_start(starter_list[i])
        snippets.append([start, end])
    # the last one
    start = extract_start(starter_list[-1])
    end = extract_end(-1) 
    snippets.append([start, end])
    
    speaker_dict = collections.defaultdict(list)
    for speaker, time_interval in zip(person_list, snippets):
        if -1 in time_interval: continue
        speaker_dict[speaker].append(time_interval)
        
    new_speaker_dict = collections.defaultdict()
    for speaker, time in speaker_dict.items():
        new_speaker_dict[speaker] = {'time': time}
        
    return new_speaker_dict


    
def build_yearly(gentle_files):
    """
    Make dictionary for each file

    Assume each gentle file has a corresponding tpt file.
    Parameters
    ----------
    gentle_paths : string
        DESCRIPTION.

    Returns
    -------
     {"2018-01-16_0100_US_CNN_Anderson_Cooper_360": {
        "Ana_Navarro": {
            "time": [
                [
                    "20180116012229.417",
                    "20180116012406.081"
                ],
                ...
                }
            ...
    """
    
    file_dict = collections.defaultdict()
    for gentle_file in gentle_files:
        tpt_file = gentle_file[:-18]+".tpt"
        file_name = gentle_file.split("/")[-1][:-18]
        print("PROCESSING...")
        print(file_name)
        if check_gentle(gentle_file):
            print("GENTLE file is not empty...")
            speaker_dict = extract_time(gentle_file, tpt_file)  
            file_dict[file_name] = speaker_dict
        
    return file_dict
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("not valid ")
    else:
        gentlepath = args[1]
        output = args[2]
        with open(, 'r') as f:
            gentle_paths = f.read().splitlines()
        all_dict = build_yearly(gentle_paths)
        # with open('./output/corpus_2018.json', 'w') as fp:
        with open(output, 'w') as fp:
            json.dump(all_dict, fp, sort_keys=True, indent=4, ensure_ascii=False)
    
    
    
    
    

