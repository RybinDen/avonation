## Description
Description for Russian [Описание на русском](https://github.com/rybinden/avonation/blob/master/readme-ru.md) 
Avonation is a python console audio player for raspberry pi.
Control is carried out using the keyboard.

### Installing and starting

```
python3 -m pip install -r requirements.txt
python3 avonation.py
```

### Functions:

- Play online radio stations, audio files.
- Listening to audio podcasts.
- Play files from youtube.
- Player volume, keys +, -.
- Element activation - keys: L, right, space, enter.
- Go backward - keys: J, left.
- prev element: I, up
-  next element: K, down
- Exit the script: Q, ESC

For playback, omxplayer is used.

### Listening to the radio

The radio station name and links should be stored in the "radiostations" file, which should be in the user folder. Each station is written on a new line, with a separator "	" tab between the name and link.
Example:
``,
mds	http://mds-station.com:8000/mds
маяк	http://212.75.194.94:8000/KemMayakFM
``,

### listening to mp3, wav files

Audio files must be placed in the same folder where the script is located, so far only one file is played.

### Listening to podcasts

To listen to your favorite podcasts, you need to create a text file called podcast.txt in the same folder where the script is located.
In this file, you need to write a link to the xml file of your podcast.
You can specify several links, each must be on a new line.

### Listening to youtube

To listen to videos from your favorite youtube channels, create a text file called youtube.txt in the same folder as the script.
In this file, you need to write down the identifiers of the channels that you want to listen to.
Each channel id must be on a new line.
The script will display the name of the channel and its files, the number of views, duration, publication date in the format -
today | yesterday | the day before yesterday | 3 days ago | ... | last week | this month | last month | month | year.