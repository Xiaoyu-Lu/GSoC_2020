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

`input`➔ `script` ➔ `output`

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

Once we have all four files above for each concatenated video clip, we feed the files into pyannotate, which labels each unique face with a unique integer label. We assume the face of the speaker to extract has the most label occurences among all identified faces. After clustering the faces and identifying the speaker's face, we extract the frames that contains the speaker based on time points and crop out the face based on its coordinates.

`merged_snippets/*.mp4 `& `merged_snippets/*.embedding.txt` &`merged_snippets/*.track.txt` ➔ `datasetBuilder_6_cluster_imgcrop.py` *(pyannote virtual enviroment)* ➔ `merged_snippets/*_frames` & `merged_snippets/cropped_frames/*_cropped_frames`

For example, the result of the face clustering using the embedding file should look like as follows:
```
[ start_time   -->  end_time] track label
[ 00:00:00.000 -->  00:00:01.468] 0 0
[ 00:00:01.502 -->  00:00:03.570] 1 9
[ 00:00:03.604 -->  00:00:07.107] 2 9
[ 00:00:07.074 -->  00:00:11.178] 3 9
[ 00:00:07.207 -->  00:00:08.509] 4 4
[ 00:00:08.742 -->  00:00:11.178] 5 8
[ 00:00:11.512 -->  00:00:15.616] 6 6
[ 00:00:12.679 -->  00:00:23.590] 7 9
[ 00:00:16.216 -->  00:00:31.198] 8 8
[ 00:00:23.524 -->  00:00:31.198] 9 9
[ 00:00:31.765 -->  00:00:39.540] 10 9
[ 00:00:39.573 -->  00:00:40.841] 11 9
[ 00:00:40.874 -->  00:00:41.475] 12 9
[ 00:00:41.408 -->  00:00:50.551] 13 9
[ 00:00:50.584 -->  00:00:59.393] 14 9
[ 00:00:52.152 -->  00:00:55.489] 15 15
[ 00:00:55.389 -->  00:00:58.325] 16 18
[ 00:00:57.758 -->  00:00:58.792] 17 17
[ 00:00:58.225 -->  00:00:58.792] 18 18

json version: 
{'pyannote': 'Annotation', 'content': [{'segment': {'start': 0.0, 'end': 1.4680000000000002}, 'track': 0, 'label': 0}, {'segment': {'start': 1.5019999999999998, 'end': 3.57}, 'track': 1, 'label': 9}, {'segment': {'start': 3.6039999999999996, 'end': 7.107}, 'track': 2, 'label': 9}, {'segment': {'start': 7.074, 'end': 11.177999999999999}, 'track': 3, 'label': 9}, {'segment': {'start': 7.207000000000001, 'end': 8.509}, 'track': 4, 'label': 4}, {'segment': {'start': 8.742, 'end': 11.177999999999999},...
```
We find the mode label, in this case is 9. Therefore, we determine that the speaker to extract corresponds to label 9. 

Then, we read the tracking file:
```
           t  track   left    top  right  bottom     status
0      0.000      0  0.328  0.185  0.530   0.541  detection
1      0.033      0  0.331  0.182  0.536   0.544    forward
2      0.067      0  0.328  0.185  0.530   0.541    forward
3      0.100      0  0.333  0.182  0.537   0.544    forward
4      0.133      0  0.330  0.185  0.533   0.541    forward
     ...    ...    ...    ...    ...     ...        ...
2414  59.293     14  0.156  0.243  0.236   0.384    forward
2415  59.326     14  0.153  0.246  0.233   0.387    forward
2416  59.359     14  0.150  0.251  0.231   0.392    forward
2417  59.393     14  0.150  0.254  0.230   0.398    forward
2418  59.426     14  0.147  0.260  0.227   0.401    forward

[2659 rows x 7 columns]
```
Then, we select those tracks with label 9:
```
           t  track   left    top  right  bottom    status
45     1.502      1  0.306  0.174  0.369   0.282  backward
46     1.535      1  0.305  0.171  0.369   0.282  backward
47     1.568      1  0.306  0.174  0.369   0.282  backward
48     1.602      1  0.303  0.171  0.367   0.285  backward
49     1.635      1  0.303  0.174  0.366   0.282  backward
     ...    ...    ...    ...    ...     ...       ...
2414  59.293     14  0.156  0.243  0.236   0.384   forward
2415  59.326     14  0.153  0.246  0.233   0.387   forward
2416  59.359     14  0.150  0.251  0.231   0.392   forward
2417  59.393     14  0.150  0.254  0.230   0.398   forward
2418  59.426     14  0.147  0.260  0.227   0.401   forward

[1685 rows x 7 columns]
```
For each track group, we randomly select one as the frame to extract:

```
     time  track   left    top  right  bottom            status
0   1.902      1  0.300  0.171  0.366   0.285          backward
1   5.105      2  0.420  0.182  0.589   0.478  forward+backward
2   7.641      3  0.164  0.246  0.244   0.384  forward+backward
3  14.815      7  0.169  0.238  0.250   0.378  forward+backward
4  24.024      9  0.167  0.260  0.236   0.381  forward+backward
5  32.266     10  0.403  0.177  0.573   0.478  forward+backward
6  40.007     11  0.303  0.160  0.367   0.276  forward+backward
7  41.041     12  0.405  0.188  0.572   0.483          backward
8  47.814     13  0.388  0.210  0.555   0.506  forward+backward
9  57.958     14  0.152  0.251  0.231   0.392  forward+backward
 ```

We use ffmpeg to extract the frame at specific time:
```
ffmpeg -ss $time -i $input_video -vframes 1 -q:v 2 $output.jpg
```
Then we examine the data of bounding box in the track file:
```
# left   = bounding box left boundary (unit = ratio of frame width)
# top    = bounding box top boundary (unit = ratio of frame height)
# right  = bounding box right boundary (unit = ratio of frame width)
# bottom = bounding box bottom boundary (unit = ratio of frame width)
  left    top  right  bottom
 0.300  0.171  0.366   0.285
 ```
So we have to transform the float into the integer that corresponds to the extracted frame. Because the face takes up too much portion of the images, it will be better to enlarge the bounding box. For example, the box is enlarged by 20%:
```
original face box coordinates:  192 234 61 103
enlarged face box coordinates:  183 242 52 111
```

![aaron-david-miller](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/phase2-cropped-dir.png)

![cropped](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/phase2-cropped-image-female.png)



