## Timeline

| weeks  | date        | goal                                                         |
| ------ | ----------- | ------------------------------------------------------------ |
| week4  | 06.22-06.28 | extract video snippets and clear up the unwanted files       |
| week5  | 06.29-07.05 | decide the input and modify a neural network model           |
| week6  | 07.06-07.12 | train the first model                                        |
|        |             |                                                              |

#### divided into 3 groups

young [18-40]

middle [45-65]

old[70-100]

#### extract snippets from video:

e.g. middle

```
2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1474.39-1477.1_Chris_Cuomo.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1477.93-1493.62_Chris_Cuomo.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1612.73-1618.81_Chris_Cuomo.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1619.54-1626.15_Chris_Cuomo.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1627.14-1629.73_Van_Jones.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1629.94-1632.2_Van_Jones.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1634.32-1636.64_Van_Jones.mp4

2018-01-16_0200_US_CNN_Cuomo_Prime_Time_1656.29-1662.04_Chris_Cuomo.mp4

2018-01-20_0100_US_CNN_Anderson_Cooper_360_819.18-823.73_Mick_Mulvaney.mp4

2018-05-01_2000_US_CNN_The_Lead_With_Jake_Tapper_388.49-391.05_Jake_Tapper.mp4

2018-05-25_0100_US_CNN_Anderson_Cooper_360_536.14-537.83_Anderson_Cooper.mp4

2018-06-05_1700_US_CNN_Wolf_342.77-355.28_Jim_Acosta.mp4

2018-06-22_2000_US_CNN_The_Lead_With_Jake_Tapper_1800.48-1803.49_Paul_Begala.mp4

...
```
After face clustering, we can have the results like:

![img](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/week4-fc0.png)

![img](https://github.com/Xiaoyu-Lu/GSoC_2020/blob/master/docs/img/week4-fc1.png)

Then, we need to figure out who is the speaker of the snippet.

After the meeting with mentor, we made an assumption, the one has the longest duration is the right one.

So we will randomly choose 12 snippets to test the assumption. 















