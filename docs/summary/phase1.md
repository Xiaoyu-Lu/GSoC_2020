Before we can predict people's age group in a video, we have to build a dataset that can feed into the machine learning model.

### Phase 1: Building Dataset

#### Step 1: Knowing what to do

The tv news videos are all stored in the tv directory. The year ranges from 2005 to 2020. 

The first thing we have to do is to determine which video we will use. After checking all the documents on the HPC, we decided to use those videos which has a corresponding tpt file.

> tpt: Online transcript (downloaded and mechanically aligned)

*Peek into the tpt file:*

```
...
20180415100018.417|20180415100024.957|NER_01|Person=Nikki Haley|Role=U.S. AMBASSADOR TO THE UNITED NATIONS
20180415100018.417|20180415100019.752|CC1|>> NIKKI HALEY, U.S. AMBASSADOR TO THE UNITED NATIONS: If the Syrian regime uses 
20180415100019.818|20180415100023.255|CC1|this poisonous gas again, 
...
```

It has the "Person=Nikki Haley", and the text "If the Syrian regime uses this poisonous gas again, ... ". 

We can have the age of the person, as long as we got his/her birthday. So, having all the tpt files and extracting all the names from them is the next step.

#### Step 2: Finding useful paths

We went through all the files in the tv directory, and wrote their paths into a txt file. Because some tpt files are not in the english language, we added a condition to find all english tpt files. 

*Peek into the header of a tpt file:*

```
TOP|20130101140001|2013-01-01_1400_US_CNN_Newsroom
...
LAN|ENG
...
```

Now, we have all the legit paths, which can lead us to the tpt files. Next, we dig into the tpt file and get the information we need from it. 

#### Step 3: Extracting information from the tpt file

Checking the tpt file as shown above, what we need are speaker and the time interval. The line in a format of `start time | end time | primary tag | other contents`contains all the information we need: 

```
20180415100018.417|20180415100024.957|NER_01|Person=Nikki Haley|Role=U.S. AMBASSADOR TO THE UNITED NATIONS
```

Then we processed each file and stored them into a json file.

*Peek into a json file:*

```
{
    "2018-01-16_0100_US_CNN_Anderson_Cooper_360": {
        "Ana_Navarro": {
            "role": "CNN POLITICAL COMMENTATOR",
            "time": [
                [
                    "20180116012229.417",
                    "20180116012406.081"
                ],
                ...
            ]
        },
        "Anderson_Cooper": {
            "role": "CNN ANCHOR",
            "time": [
                [
                    "20180116013300.817",
                    "20180116013305.855"
                ],
               ...
```

For convenience, we dealt with the files year by year. Interestingly, 2005, 2010, 2014, 2019 and 2020 don't have the transcripts: 

*Tree*:

```bash
.
├── corpus_2006.json
├── corpus_2007.json
├── corpus_2008.json
├── corpus_2009.json
├── corpus_2011.json
├── corpus_2012.json
├── corpus_2013.json
├── corpus_2015.json
├── corpus_2016.json
├── corpus_2017.json
└── corpus_2018.json
```

Then, we know who the speakers are, so we can create the database that stores all the information of the speakers for future use. 

#### Step 4: Building a database for speakers

DBpedia is very friendly for web scraping. 

> *DBpedia* (from "DB" for "database") is a project aiming to extract structured content from the information created in the *Wikipedia* project. 

So we collected all speaker's name from the json file and looked upon the DBpedia. If nothing was found, return the string "None".

- **Problem encountered:**

  The speaker's name is not well-formatted in the tpt file:

  ```
  20180415100520.486|20180415100722.609|NER_01|Person=[06:05:12] Nick Paton Walsh|Role=CNN SENIOR INTERNATIONAL CORRESPONDENT
  ```

  We have to clean the part after `Person=` to get `Nick_Paton_Walsh`.

Normaly, we use the url  ` "http://dbpedia.org/page/"+ speaker_name  ` to get the information. 

e.g. `http://dbpedia.org/page/Anderson_Cooper` 

We use `Beautifulsoup` to get the birthDate from `xhtml`:

```
<li><span class="literal"><span property="dbo:birthDate" xmlns:dbo="http://dbpedia.org/ontology/">1967-06-03</span><small> (xsd:date)</small></span></li>
```

Later, we found out that `dbpedia.org` updated 6-18 months behind the update of Wikipedia. So manually, we can get the birthdays of some speakers online, but  not by web scraping using DBpedia.org. 

There is another way which is more dynamic of retrieving data from Wikipedia -- `DBpedia Live`. 

At this point, we found out that DBpedia provides several formats, for example the json format:

```
...
"http://live.dbpedia.org/ontology/birthDate" : 
	[ 
		{ "type" : "literal", "value" : "1967-06-03" , 
			"datatype" : "http://www.w3.org/2001/XMLSchema#date" 
			} 
	] ,
	...
```

So we have a two-step searching mechanism: if the result of searching returns "None" in ``dbpedia.org``, it turns to use `DBpedia Live`. 

- **Problem encountered:** 

  When dumping the json file for corpus building in step 3, we set the parameter of  `ensure_ascii` to *False*. 

  > If *ensure_ascii* is true (the default), all non-ASCII characters in the output are escaped with `\uXXXX` sequences, and the result is a [`str`](https://docs.python.org/2/library/functions.html#str)instance consisting of ASCII characters only. If *ensure_ascii* is false, some chunks written to *fp* may be [`unicode`](https://docs.python.org/2/library/functions.html#unicode) instances. This usually happens because the input contains unicode strings or the *encoding* parameter is used. 

  So if we need to open `http://live.dbpedia.org/data/Pablo_Guzmán_(reporter).json` , it will trigger the error, due to the non-ASCII character `á ` . 

  ```
  UnicodeEncodeError: 'ascii' codec can't encode character '\xe1' in position 20: ordinal not in range(128)
  ```

  To make it safe as URL component, we can use `quote()`. 

  e.g. `"http://live.dbpedia.org/data/"+quote(name)+".json"`

Given the large amount, it took a while to go through all the names in the database. 

*Peek into the speakers' database:*

```
{
    "Andrew_Luck": {
        "birth_date": "1989-9-12",
        "gender": "male"
    },
    "Andrew_Marchand": {
        "birth_date": "None",
        "gender": "male"
    },
    ...
}
```

Next, we can integrate the speaker database with the corpus created in step 3. 

#### Step 5: Creating a lean corpus

We can calculate the speaker's age by the speaker's name and birthday. 

- **Problem encountered:** 

  We use `datetime` package to calculate the age: to get the differences between two dates *(start date is the birth date, end date is the broadcast time*) and then divide it by 365.2425. 

  However,  not all dates have the format "yyyy-mm-dd", e.g. ''2011afdi1''. We have to check if the date is valid first, then use it for calculating the age. 

  Besides, for the birth date that only contains year, such as "2011-0-0", we convert it into "2011-1-1".

*At first, I did not want to include the gender, but my mentor Karan said it has no harm. So I included the gender of speakers into the corpus.*

*Peek into the lean corpus:*

```
{
    "2018-01-16_0100_US_CNN_Anderson_Cooper_360": {
        "Ana_Navarro": {
            "age": 46,
            "gender": "female",
            "time": [
                [
                    1977.66,
                    2027.059999
                ]
            ]
        },
        "Anderson_Cooper": {
            "age": 50,
            "gender": "male",
            "time": [
                [
                    12.9,
                    21.03
                ],
                ...
```

#### Step 6: Extracting video snippets

Now, we have everything we need to extract the video snippets:  the input path (video path), the output path (snippet path), the start time and the end time. 

- **Problem encountered:** 

  Out of habits, we randomly extracted five snippets. The results are disappointing, because the start time and the end time are not reliable! 

  I turned to ask for help, because the  work is really time-consuming, I really don't want to waste time on this. Luckily, one of my mentors, Peter, told me that his students have done the aligment using gentle for the data in 2018. 

  So I decided to use the gentle output to **redo Step 3**. 

  *Peek into the gentle output:*

       {
        "transcript": "\u266a Size overwhelming and e... "
        "words": [
          {
            "alignedWord": "and",
            "case": "success",
            "end": 28.34,
            "endOffset": 23,
            "phones": [
      				...
            ],
            "start": 28.15,
            "startOffset": 20,
            "word": "and"
          }, 
          ...
          {
            "case": "not-found-in-audio",
            "endOffset": 52,
            "startOffset": 46,
            "word": "regime"
           }, ...
  We can locate the word by `startOffset` and `endOffset` in the transcript. The transcript is extracted from the tpt file, so we can map it back to the tpt file. 

  *Peek into the tpt file:*

  ```
  ...
  20180415101153.580|20180415101157.184|NER_01|Person=Christi Paul|Role=CNN ANCHOR
  20180415101153.580|20180415101155.048|CC1|>> PAUL: Sure. So, Juliette, if you are not going to get involved in a civil war and you are not going to displace this 
  20180415101155.115|20180415101156.550|CC1|leader, what are the 
  20180415101156.617|20180415101157.117|CC1|options? 
  20180415101157.184|20180415101255.743|NER_01|Person=Juliette Kayyem|Role=CNN NATIONAL SECURITY ANALYST
  20180415101157.184|20180415101158.352|CC1|>> KAYYEM: So, there's two focuses that we will see 
  20180415101158.418|20180415101158.952|CC1|in the future. 
  ...
  ```

  The transcript contains the text "*Sure. So, Juliette, if you are not going to get involved in a civil war and you are not going to displace this leader, what are the options?*" We locate this text in the transcript, from 11000 to 11139. Hence, get the corresponding `start`(701.83) and `end` time(710.38). 

  - **Problem encountered:**

    Not all words are aligned, some of them are "not-found-in-audio". In this case, we omit this time interval if one of the time (start and end) is not found. 

  After the doing the step 3 again, we have a new corpus:

  ```
  └── corpus_2018_new.json
  ```

Then, we use this newly created corpus to trim the videos. We name the output file in a format of ` '{file_name}_{start_time}-{end_time}_{person}.mp4'`. And the output will be written/appended in a csv file for future reference.

- **Problem encountered:**

  After running the script for an hour, the outputs look like the same, except the start and end time in the file name. Then, we rechecked the corpus. This kind of output appeared because someone spoke more than the others , e.g. the anchors. So we have to delete some of the time intervals from dataset. 

  ```
  [('Anderson_Cooper', 9613),
   ('Chris_Cuomo', 6523),
   ('Jake_Tapper', 5370),
   ('Wolf_Blitzer', 4614),
   ('John_King', 4390),
   ('Donald_Trump', 2825),
   ('Christi_Paul', 2626),
   ('Jim_Sciutto', 1623),
   ...
  ```

  [img]

  First, for the whole dataset, the time tuple whose duration is smaller than 3 seconds is removed, whose duration is greater than 30 seconds is cut to 30.  

  Next round, we only deal with the most appeared speakers whose time tuples' count is greater than 25 times. The time tuple whose duration is smaller than 5 seconds is removed, whose duration is greater than 20 seconds is cut to 20. 

  ```
  [('Anderson_Cooper', 7687),
   ('Jake_Tapper', 4341),
   ('Chris_Cuomo', 4297),
   ('Wolf_Blitzer', 4054),
   ('John_King', 3889),
   ('Donald_Trump', 2407),
   ('Christi_Paul', 2269),
   ('Jim_Sciutto', 1387),
   ...
  ```

  For the rest of times, we can normalize the count of time intervals for the speakers in each files.

  ​	e.g.  James appeared in 5 files. The number of time intervals of each file is stored in an array, nums=[10, 30, 1, 150, 9]. We made 25 times as a threshold, then normalize the array .

  ​			sum(nums) = 200

  ​			Each number in the array is divided by (200/25),  0.5 is added to each number to avoid zeros.

  ​			Then, we round up and int each numnber. The result would be [2, 4, 1, 19, 2]. 

  ```python
  nums: 
  [1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 3, 1, 3, 1, 1, 1, 2, 2, 1, 4, 2, 1, 3, 5, 3, 2, 4, 2, 1, 3, 1, 1, 3, 2, 7, 2, 1, 6, 13, 1, 5, 2, 1, 4, 4, 2, 1, 3, 3, 2]
  
  after normalization:
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  
  The sum of the array after normalization is 56, we turn the number into zero after the 25:
  
  {file_1: [speaker_1, 1], 
   ...
   file_22: [speaker_1, 2],  #(although the speaker have 5 time intervals, we only choose 2 of them.)
   file_23: [speaker_1, 1], 
   file_24: [speaker_1, 0],
   ...
   file_50: [speaker_1, 0]
   }
  ```

  For example, the speaker_1 have 25 time intervals. We randomly select 2 from them:

  ```
  { file_1:{       
         speaker_1: {
              "age": 50,
              "gender": "male",
              "time": [
                  [
                      12.9,
                      21.03
                  ],
                  [
                      28.349999,
                      115.46
                  ],
                  ...
              ]
          },
          ...
  ```

  We use random.sample(database[file_1]\[speake_1]["time"],  k=2) to select two without replacement. 

  - **Problem encountered:**

    I used random.choice(), at the first time, I didn't noticed that it includes the replacement, so when the snippets are being extracted, I got the prompts of asking `y/N` to overwrite the existing file. It is weird because every file should be created for the first time, so there must be something wrong with the dataset. There're some duplicates in the "time", so I traced the problem to the misuse of a random function. 

  ```
  { file_1:{       
         speaker_1: {
              "age": 50,
              "gender": "male",
              "time": [
                  [
                      28.349999,
                      115.46
                  ],
                  [
                      1128.3433,
                      1145.456
                  ]
              ]
          },
          ...
  ```

  Finally, we have the dataset that can be used for extracting snippets. We put it on the hpc, where all the tv data stored, and use ffmpeg python wrapper to run the code. We have 928 files, 614 unique speakers, 7728 time intervals which means we will have 7728 snippets. 

The script can write all the information of the video snippet into a csv file, if a snippet is extracted from the video. 

[img]\(snippets_info_csv)





