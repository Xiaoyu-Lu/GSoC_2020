GSoC 2020: Age Group Prediction in Images & Audio

# Coding Phase

week 1:   June 1st. - June 5th.

Meeting on June 3rd, 2020

Tasks:

- Setup gentle (https://github.com/lowerquality/gentle)
- Extract mp3 from mp4 files.
- Run gentle to align mp3 and text file.


gentle:
```
git clone https://github.com/lowerquality/gentle.git
cd gentle
./install.sh
python3 align.py audio.mp3 words.txt
```
