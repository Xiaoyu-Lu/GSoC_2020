### Dataset Building

- cleaned out the data that has script (tpt file).

  ```
  [tpt file] | [mp4 file]
  
  /mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-15/2018-04-15_1000_US_CNN_New_Day_Sunday.tpt|/mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-15/2018-04-15_1000_US_CNN_New_Day_Sunday.mp4
  /mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-15/2018-04-15_1100_US_CNN_New_Day_Sunday.tpt|/mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-15/2018-04-15_1100_US_CNN_New_Day_Sunday.mp4
  /mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-15/2018-04-15_1200_US_CNN_Inside_Politics.tpt|/mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-15/2018-04-15_1200_US_CNN_Inside_Politics.mp4
  /mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-27/2018-04-27_1700_US_CNN_Wolf.tpt|/mnt/rds/redhen/gallina/tv/2018/2018-04/2018-04-27/2018-04-27_1700_US_CNN_Wolf.mp4
  ```

- retrieved the person's birthday by his/her name and then count his/her age 

  ```
  if the news was broadcast on 2012-09-11:
  [name] [gender] [birthday] [age]
  
  Martin_Savidge male 1958-05-27 54
  Barack_Obama male 1961-08-04 51
  Leon_Panetta male 1938-06-28 74
  Joseph_Biden male 1942-11-20 69
  Rudolph_Giuliani male 1944-05-28 68
  Rosaleen_Tallon None None None
  Wolf_Blitzer male 1948-03-22 64
  Howard_Lutnick male 1961-07-14 51
  UNKNOWN None None None
  Mitt_Romney male 1947-03-12 65
  Dan_Simon None None None
  Elizabeth_Cohen female None None
  STEVE_PERRY None None None
  Rahm_Emanuel male 1959-11-29 52
  Sunny_Hostin female 1968-10-20 43
  Christine_Romans female 1971-1-31 41
  Roberton_Williams None None None
  Sara_Sidner female 1972-05-31 40
  Angelina_Jolie female 1975-06-04 37
  ```

  



