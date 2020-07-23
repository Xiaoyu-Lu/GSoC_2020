We examined those snippets we have exacted. There are several types in the snippets:

- single speaker (the diresiable )

- two people in one scene 
- multiply people in one scene 
- changed scenes
- voice over (no speaker showing up)

To avoid losing more data, we select the snippets in which the scenes of a single speaker appeared more often than others as the training data; the left snippets as the testing data.

### Face clustering

For a 1 minutes 22 seconds long video, we want to figure out whether it belongs to the training dataset. We could see from the following output from face clustering that the label indicates who the person to which index is. 

```
[ start_time   -->  end_time] index label
[ 00:00:00.000 -->  00:00:00.667] 0 12
[ 00:00:01.935 -->  00:00:05.606] 1 7
[ 00:00:01.935 -->  00:00:05.606] 2 11
[ 00:00:05.639 -->  00:00:14.882] 3 7
[ 00:00:14.848 -->  00:00:19.987] 4 7
[ 00:00:20.020 -->  00:00:27.461] 5 7
[ 00:00:20.020 -->  00:00:27.461] 6 8
[ 00:00:27.494 -->  00:00:36.136] 7 7
[ 00:00:29.963 -->  00:00:31.765] 8 8
[ 00:00:31.365 -->  00:00:34.434] 9 8
[ 00:00:34.301 -->  00:00:36.136] 10 8
[ 00:00:36.169 -->  00:00:36.703] 11 11
[ 00:00:36.169 -->  00:00:36.703] 12 12
[ 00:00:36.703 -->  00:00:40.574] 13 7
[ 00:00:36.703 -->  00:00:52.519] 14 11
[ 00:00:40.407 -->  00:00:41.608] 15 7
[ 00:00:41.642 -->  00:00:45.145] 16 7
[ 00:00:45.078 -->  00:00:50.751] 17 7
[ 00:00:50.050 -->  00:00:52.519] 18 7
[ 00:00:52.553 -->  00:00:54.855] 19 7
[ 00:00:52.553 -->  00:00:56.189] 20 8
[ 00:00:52.553 -->  00:00:56.256] 21 21
[ 00:00:56.290 -->  00:01:13.774] 22 7
[ 00:01:12.873 -->  00:01:13.574] 23 8
[ 00:01:13.974 -->  00:01:15.008] 24 7
[ 00:01:14.975 -->  00:01:20.781] 25 7
[ 00:01:18.745 -->  00:01:20.013] 26 8
[ 00:01:20.714 -->  00:01:21.782] 27 7
[ 00:01:21.815 -->  00:01:22.382] 28 28
```

After counting the number of labels, we could find out that label 7 shows up more than the other labels. Thus, we assumed that label 7 would be the speaker, and we keep this snippet in the training dataset.  

### Tracking

Next step is finding the binding box. We checked the tracking result:

```
0.000 0 0.441 0.221 0.609 0.517 detection
0.033 0 0.431 0.232 0.602 0.530 forward+backward
0.067 0 0.430 0.238 0.598 0.530 forward+backward
0.100 0 0.430 0.235 0.598 0.530 forward+backward
0.133 0 0.433 0.238 0.598 0.528 forward+backward
0.167 0 0.433 0.238 0.598 0.528 forward+backward
0.200 0 0.434 0.240 0.598 0.528 forward+backward
0.234 0 0.434 0.240 0.598 0.528 forward+backward
0.267 0 0.436 0.243 0.598 0.530 forward+backward
0.300 0 0.438 0.251 0.595 0.525 forward+backward
0.334 0 0.434 0.246 0.595 0.528 forward+backward
0.367 0 0.438 0.251 0.595 0.530 forward+backward
0.400 0 0.433 0.249 0.595 0.530 forward+backward
0.434 0 0.434 0.249 0.597 0.530 forward+backward
0.467 0 0.422 0.254 0.591 0.550 detection
0.501 0 0.422 0.254 0.591 0.550 forward
0.534 0 0.422 0.254 0.591 0.550 forward
0.567 0 0.422 0.254 0.591 0.550 forward
0.601 0 0.422 0.254 0.591 0.552 forward
0.634 0 0.420 0.254 0.591 0.552 forward
0.667 0 0.422 0.254 0.591 0.550 forward
1.935 1 0.216 0.207 0.334 0.417 backward
```

There are 7 columns in the result, namely:

```
names = ['t', 'track_id', 'left', 'top', 'right', 'bottom', 'status']
# t      = elapsed time since the beginning of the video (unit = seconds)
# track  = all faces belonging to the same tracklet share this same id
# left   = bounding box left boundary (unit = ratio of frame width)
# top    = bounding box top boundary (unit = ratio of frame height)
# right  = bounding box right boundary (unit = ratio of frame width)
# bottom = bounding box bottom boundary (unit = ratio of frame width)
```

So, from 0 second to 0.667 is one speaker, from 1.935 s is another. This time intervals echos with the face clustering result. 

```
# tracking result
0.000 0 0.441 0.221 0.609 0.517 detection
....
0.667 0 0.422 0.254 0.591 0.550 forward
1.935 1 0.216 0.207 0.334 0.417 backward
# face clustering result
[ 00:00:00.000 -->  00:00:00.667] 0 12
[ 00:00:01.935 -->  00:00:05.606] 1 7
```

Now, we have the binding box of label 7 for each frame. This could use as input for our upcoming training model.

 



 

 