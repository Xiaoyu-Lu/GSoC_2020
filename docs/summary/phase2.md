- [Summary of Phase 1:](#summary-of-phase-1)

  * [Review1: Get rough corpus](#review1-get-rough-corpus)
  
  * [Review2: Build speakers' database](#review2-build-speakers--database)
  
  * [Review3: Form lean corpus](#review3-form-lean-corpus)
  
  * [Review4: Extract video snippets](#review4-extract-video-snippets)
  
- [Phase 2: Perparing Neural Net Input](#phase-2-perparing-neural-net-input)

  * [Step1: Snippets concatenation](#step1-snippets-concatenation)
  
  * [Step2: Face detection, tracking and embedding](#step2-face-detection--tracking-and-embedding)
  
  * [Step3: Face clustering and image cropping](#step3-face-clustering-and-image-cropping)


### Summary of Phase 1:

At the end of Phase 1, we got a csv file that contains all the information of file path, start and end times, speakers' name, age and gender, etc. 

#### Review1: Get rough corpus

We started from the gentle output (force aligned output), convert it into a json structure. 

`gentle_paths.txt`➔ `datasetBuilder_0_gentle_and_tpt.py` ➔ `corpus_2018_new.json`

*Peek into the corpus_2018_new.json file:*

```
{
    "2018-01-16_0100_US_CNN_Anderson_Cooper_360": {
        "Ana_Navarro": {
            "time": [
                [
                    1977.66,
                    2027.059999
                ]
            ]
        },
        "Anderson_Cooper": {
            "time": [
                [
                    12.9,
                    21.03
                ],
```

#### Review2: Build speakers' database

We use this json file to get the speakers' informtion by web scraping.

`corpus_2018_new.json `➔ `datasetBuilder_1_speaker_db.py` ➔ `speaker_db.json`

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

#### Review3: Form lean corpus

Input the both output file from above into the python script to get a well formed structure. 

`corpus_2018_new.json` & ` speaker_db.json`   ➔ `datasetBuilder_2_lean.py` ➔ `lean_corpus_2018_trimmed.json`

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

#### Review4: Extract video snippets

Based on this json file, we can extract snippets from the original news video.

`lean_corpus_2018_trimmed.json` ➔ `datasetBuilder_3_extract_snippets.py` ➔ `snippets/*.mp4` & `snippets_info_with_age_gender.csv`

###  Phase 2: Perparing Neural Net Input

We decide to use nerual network to train the model. The training input should be faces images:

![face-img](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/phase2-wiki.png)

#### Step1: Snippets concatenation

Since a speaker might show up in different news program, we had to concatenate the snippets of one speaker together into one video clip.

`snippets/*.mp4` & `snippets_info_with_age_gender.csv` ➔ `datasetBuilder_4_concat` ➔ `merged_snippets/*.mp4` & `merged_snippets/merged_files.txt`

*Peek into the merged_files.txt:*

```
./Malcolm_Jenkins-male-30.mp4
./Chief_Roger_Moore-male-48.mp4
./Alex_Jones-male-44.mp4
./Sen._Jim_Inhofe-male-83.mp4
./Rana_Foroohar-female-47.mp4
./Jack_Kingston-male-62.mp4
...
```

#### Step2: Face detection, tracking and embedding

![news-imgs](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/phase2-shows.png)

More then one person could exist on one screen, we have to identify which one is the speaker. Here, we use the open source tool [pyannote-video](https://github.com/pyannote/pyannote-video) to get the work done. 

`merged_snippets/*.mp4` ➔ `datasetBuilder_5_track_embed.sh` *(pyannote virtual enviroment)* ➔ `merged_snippets/*.shots.json` & `merged_snippets/*.track.txt `& `merged_snippets/*.landmarks.txt` & `merged_snippets/*.embedding.txt`

*Peek into the shots.json:*

```
{"pyannote": "Timeline", "content": [{"start": 0.0, "end": 3.6036}, {"start": 3.6036, "end": 11.211200000000002}, {"start": 11.211200000000002, "end": 31.2312}, {"start": 31.2312, "end": 31.76506666666667}, {"start": 31.76506666666667, "end": 39.57286666666667}, {"start": 39.57286666666667, "end": 40.87416666666667}, {"start": 40.87416666666667, "end": 59.57}]}
```

*Peek into the track.txt :*

```
0.000 0 0.328 0.185 0.530 0.541 detection
0.033 0 0.331 0.182 0.536 0.544 forward
0.067 0 0.328 0.185 0.530 0.541 forward
0.100 0 0.333 0.182 0.537 0.544 forward
...
```

*Peek into the landmarks.txt:*

```
0.000 0 0.39531 0.29006 0.39219 0.32320 0.39219 0.35359 0.39219 0.38950 0.39375 0.42265 0.39844 0.45580 0.40469 0.48066 0.41094 0.50829 0.42656 0.52210 0.45156 0.52762 0.47969 0.51934 0.50625 ...
```

*Peek into the embedding.txt:*

```
0.000 0 -0.04512 0.05249 0.06020 -0.01219 -0.04242 0.01722 -0.04664 -0.04774 0.11243 -0.02679 0.18594 0.00547 -0.23331 0.05367 0.03443 0.06313 -0.12638 -0.01756 -0.13083 -0.05724 -0.09808 -0.00435 0.09230 -0.08691 -0.12340 -0.27906 -0.11750 -0.17024 0.11947 -0.06781 0.01936 0.05774 -0.11125 -0.06249 0.04176 0.10610 -0.09060 0.00216 0.26070 
...
```

#### Step3: Face clustering and image cropping

Once we have all the files, we cluster the face. After clustering, we extract the frames that contains the speaker and crop out the face based on its coordinates.

`merged_snippets/*.mp4 `& `merged_snippets/*.embedding.txt` &`merged_snippets/*.track.txt` ➔ `datasetBuilder_6_cluster_imgcrop.py` *(pyannote virtual enviroment)* ➔ `merged_snippets/*_frames` & `merged_snippets/cropped_frames/*_cropped_frames`

![aaron-david-miller](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/phase2-cropped-dir.png)

![cropped](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/phase2-cropped-image-female.png)



