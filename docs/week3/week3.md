### Dataset Building

- Separated the data by year

  ```
  .
  ├── tpt_paths_2006.txt
  ├── tpt_paths_2007.txt
  ├── tpt_paths_2008.txt
  ├── tpt_paths_2009.txt
  ├── tpt_paths_2010.txt
  ├── tpt_paths_2011.txt
  ├── tpt_paths_2012.txt
  ├── tpt_paths_2013.txt
  ├── tpt_paths_2014.txt
  ├── tpt_paths_2015.txt
  ├── tpt_paths_2016.txt
  ├── tpt_paths_2017.txt
  └── tpt_paths_2018.txt
  ```

  38164 paths were stored.

- Converted each tpt file into a JSON file

  ```
  {file_name: {speaker_name:{role:xx, time:[(start,end), (start,end)]}}}
  
  
  {
      "2006-09-29_0100_US_CNN_Larry_King_Live": {
          "Ashton_Kutcher": {
              "role": "ACTOR",
              "time": [
                  [
                      "20060929010022.000",
                      "20060929010038.667"
                  ],
                  [
                      "20060929010058.000",
                      "20060929010100.000"
                  ],
                  ...
                  },
          "Ryan_Seacrest": {
              "role": "CNN HOST",
              "time": [
                  [
                      "20060929010038.667",
                      "20060929010058.000"
                  ],
                  [
                      "20060929010100.000",
                      "20060929010113.429"
                  ],
                  ...
                  
                  
  ```

  - Created speakers's database by scraping dbpedia
  
  - Built the corpus
  ```
      "2006-09-29_2000_US_CNN_Situation_Room": {
        "Donald_Rumsfeld": {
            "age": 35,
            "gender": "female",
            "time": [
                [
                    "20060929200535.000",
                    "20060929200542.429"
                ]
            ]
        },
        "Howard_Dean": {
            "age": 45,
            "gender": "male",
            "time": [
                [
                    "20060929200631.000",
                    "20060929200644.333"
                ]
            ]
        },
        "Kathleen_Koch": {
            "age": 51,
            "gender": "male",
            "time": [
                .....
```
- Getting familiar with python toolkit for face detection, tracking, and clustering in videos
