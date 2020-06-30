#Speaking audio player for raspberry pi.
#version 0.4.0 update 30.06.2020
# Denis Rybin https://github.com/rybinden/avonation

import os, evdev, time, glob, requests, json, youtube_dl
import sys, logging, configparser
from datetime import date, datetime
from omxplayer.player import OMXPlayer
from xml.etree import ElementTree
logFile = 'avonation.log'
configFile = 'setting.conf'
if len(sys.argv) == 2:
    if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
        logging.basicConfig(level=logging.DEBUG, filename=logFile)
    else:
        logging.basicConfig(level=logging.ERROR, filename=logFile)
else:
    logging = None

listModes = ['mainMenu', 'player', 'radio', 'podcast', 'youtube']
translateListModes = ['Главное меню', 'Плеер', 'Радио', 'подкасты', 'ютуб']
activeMode = 0
selectMode = 0

stationName = []
station = [] #url
stationNumber = 0
with open('radio.txt', 'r', encoding='utf-8') as f:
    for item in f.readlines():
        data = json.loads(item)
        stationName.append(data['name'])
        station.append(data['url'])

podcastList = []
podcastTitle = ''
podcastName = []
podcastUrl = []
currentPodcast = 0
channelList = []
currentChannel = 0
channelTitle = ''
youtubeVideoUrl = []
youtubeAudioUrl = ''  #current youtube audio link
currentElement = 0
totalElements = 10

def create_config(configFile): # Create a config file
    config = configparser.ConfigParser()
    section = "general"
    config.add_section(section)
    config.set(section, "language", "ru")
    config.set(section, "synthesizer", "espeak")
    section = "espeak"
    config.add_section(section)
    config.set(section, "speed", "200")
    config.set(section, "pitch", "50")
    config.set(section, "volume", "100")
    section = "rhvoice"
    config.add_section(section)
    config.set(section, "voice", "aleksandr")
    with open(configFile, "w") as config_file:
        config.write(config_file)

if not os.path.isfile(configFile):
    create_config(configFile)
def get_setting(configFile, section, setting): # Print out a setting
    config = configparser.ConfigParser()
    config.read(configFile)
    value = config.get(section, setting)
    return value

def speak(text):
    synthesizer = get_setting(configFile, "general", "synthesizer")
    if synthesizer == 'espeak':
        command = synthesizer + ' -v ' + get_setting(configFile, "general", "language") + ' -a ' + get_setting(configFile, synthesizer, "volume") + ' -p ' + get_setting(configFile, synthesizer, "pitch") + ' -s ' + get_setting(configFile, synthesizer, "speed") + ' "' + text + '"'
    if synthesizer == 'rhvoice':
        command = 'echo "' + text + '" | RHVoice-test -p ' + get_setting(configFile, synthesizer, "voice")
    os.system(command)

def parseYoutubeChannels():
    global channelList, channelTitle, youtubeVideoUrl, totalElements
    with open('youtube.txt') as f:
        channelList = f.read().splitlines()

    url = 'http://www.youtube.com/feeds/videos.xml?channel_id=' + channelList[currentChannel]
    response = requests.get(url)
    root = ElementTree.fromstring(response.text)
    ns = '{http://www.w3.org/2005/Atom}'
    channelTitle = root.findtext(ns + 'title')
    element = 0
    for item in root.findall(ns + 'entry'):
        if element < totalElements:
            element += 1
            youtubeVideoUrl.insert(element, item.find(ns + 'link').get('href'))
        else:
            break

def parseYoutubeVideo():
    global youtubeVideoUrl, currentElement, youtubeAudioUrl
    today = date.today()
    totalDays = int(today.strftime('%j'))  # количество дней, прошедших с начала года до текущего дня
    currentWeekDay = today.isoweekday()
    currentDay = today.day
    currentMonth = today.month
    currentYear = today.year
    if currentYear%4==0:
        currentDaysYear = 366
    else:
        currentDaysYear = 365
    message = ''
    options = { # Настройки youtube_dl
        'outtmpl': 'youtube/%(uploader)s/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'quiet': True,  # не показывать инфо сообщения в stdout
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        r = ydl.extract_info(youtubeVideoUrl[currentElement], download=False) # Вставляем нашу ссылку с ютуба
    youtubeAudioUrl = r['url']
    message += r['title'] + ' '
    message += 'Просмотров: ' + str(r['view_count'])
    upload_date = r['upload_date']
    uploadDate = date(int(upload_date[:4]), int(upload_date[4:6]), int(upload_date[6:8]))
    delta = today - uploadDate
    uDays = delta.days  # количество дней прошедших с загрузки видео
    monthName = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')
    if uDays <= currentWeekDay:
        if uDays == 0:
            message += 'сегодня'
        elif uDays == 1:
            message += 'вчера'
        elif uDays == 2:
            message += 'позавчера'
        elif uDays ==3:
            message += '3 дня назад'
        elif uDays ==4:
            message += '4 дня назад'
        elif uDays == 5:
            message += '5 дней назад'
        elif uDays == 6:
            message += '6 дней назад'
    elif uDays >= currentWeekDay and (uDays < currentWeekDay + 7):
        message += 'на прошой недели'
    elif (uDays >= currentWeekDay + 7) and uDays < currentDay:
        message += 'в этом месяце'
    elif uDays >= currentDay and uDays <= totalDays and uDays <= currentDaysYear:
        if uploadDate.month == currentMonth - 1:
            message += 'в прошлом месяце'
        else:
            message += monthName[uploadDate.month-1]
    else:
        if uploadDate.year == currentYear-1:
            message += 'В прошлом году'
        else:
            message += uploadDate.year

    message += ' длилтельность '
    h, m, s = 0, 0, 0
    duration = r['duration']
    m = duration // 60
    if m >= 60:
        h = m // 60
        m = m % 60
    s = duration % 60
    if h:
        message += str(h) + ' час '
    if m:
        message += str(m) + ' мин. '
    if s:
        message += str(s) + ' сек '
    return message

def parsePodcast():
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements
    if len(podcastList) == 0:
        with open('podcast.txt') as f:
            podcastList = f.read().splitlines()

    podcastName.clear()
    podcastUrl.clear()
    if currentElement != 0:
        currentElement = 0

    response = requests.get(podcastList[currentPodcast])
    root = ElementTree.fromstring(response.text)
    podcastTitle = root.findtext('channel/title')
    for item in root.findall('channel/item'):
        if currentElement == totalElements:
            break
        enclosure = item.find('enclosure')
        if enclosure != None:
            podcastName.insert(currentElement, item.findtext('title'))
            podcastUrl.insert(currentElement, enclosure.get('url'))
        currentElement += 1
    currentElement = 0

files = []
totalObject = glob.glob('*')
for item in totalObject:
    if os.path.isdir(item):
        files.append(item)
files  += glob.glob('*.mp3')
files  += glob.glob('*.wav')
countFiles = len(files)
currentNumberFile = 0

player = None
playing = False
volume=0.5
speak('Авонация запущена. Режим: ' + translateListModes[activeMode])

def increseVolume():
    global player, volume
    if player!=None:
        if volume < 1:
            volume+=0.1
            player.set_volume(volume)

def decreseVolume():
    global player, volume
    if player!=None:
        if volume>0:
            volume-=0.1
            player.set_volume(volume)

def speakTime():
    time_checker = datetime.now()
    hour = time_checker.hour
    minut = time_checker.minute
    if minut < 10:
        m = '0' + str(minut)
    else:
        m = str(minut)
    speak('время: ' + str(hour) + ':' + m)

def speakDate():
    time_checker = datetime.now()
    day = time_checker.day
    if day == 1:
        d = 'первое'
    elif day == 2:
        d = 'второе'
    elif day == 3:
        d = 'третье'
    elif day == 4:
        d = 'четвертое'
    elif day == 5:
        d = 'пятое'
    elif day == 6:
        d = 'шестое'
    elif day == 7:
        d = 'седьмое'
    elif day == 8:
        d = 'восьмое'
    elif day == 9:
        d = 'девятое'
    elif day == 10:
        d = 'десятое'
    elif day == 11:
        d = 'одиннадцатое'
    elif day == 12:
        d = 'двенадцатое'
    elif day == 13:
        d = 'тринадцатое'
    elif day == 14:
        d = 'четырнадцатое'
    elif day == 15:
        d = 'пятнадцатое'
    elif day == 16:
        d = 'шестнадцатое'
    elif day == 17:
        d = 'семнадцатое'
    elif day == 18:
        d = 'восемнадцатое'
    elif day == 19:
        d = 'деветнадцатое'
    elif day == 20:
        d = 'двадцатое'
    elif day == 21:
        d = 'двадцать первое'
    elif day == 22:
       d = 'двадцать второе'
    elif day == 23:
        d = 'двадцать третье'
    elif day == 24:
        d = 'двадцать четвертое'
    elif day == 25:
        d = 'двадцать пятое'
    elif day == 26:
        d = 'двадцать шестое'
    elif day == 27:
        d = 'двадцать седьмое'
    elif day == 28:
        d = 'двадцать восьмое'
    elif day == 29:
        d = 'двадцать девятое'
    elif day == 30:
        d = 'тридцатое'
    elif day == 31:
        d = 'тридцать первое'
    month = time_checker.month
    if month == 1:
        m = 'Января'
    elif month == 2:
        m = 'февраля'
    elif month == 3:
        m = 'марта'
    elif month == 4:
        m = 'апреля'
    elif month == 5:
        m = 'мая'
    elif month == 6:
        m = 'июня'
    elif month == 7:
       m = 'июля'
    elif month == 8:
        m = 'августа'
    elif month == 9:
        m = 'сентября'
    elif month == 10:
        m = 'октября'
    elif month == 11:
        m = 'ноября'
    elif month == 12:
        m = 'векабря'
    weekday = time_checker.weekday()
    if weekday == 0:
            w = 'понедельник'
    elif weekday == 1:
        w = 'вторник'
    elif weekday == 2:
        w = 'среда'
    elif weekday == 3:
        w = 'четверг'
    elif weekday == 4:
        w = 'пятница'
    elif weekday == 5:
        w = 'суббота'
    elif weekday == 6:
        w = 'воскресенье'
    speak('дата: ' + d + ' ' + m + ', ' + w)

def actionPressKeySpace():
    global activeMode, selectMode, player, playing
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements
    global channelList, currentChannel, channelTitle, youtubeVideoUrl, youtubeAudioUrl
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('press space')
    if activeMode == 0:  # mainMenu
        activeMode = selectMode
        if activeMode == 0:
            selectItem = translateListModes[activeMode]
            text = selectItem
        elif activeMode == 1:
            selectItem = files[currentNumberFile]
            if os.path.isdir(selectItem):
                selectItem = 'директория: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
            else:
                selectItem = 'файл: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
        elif activeMode == 2:
            selectItem = stationName[stationNumber] + '. ' + str(stationNumber+1) + ' из ' + str(len(station))
        elif activeMode == 3:
            parsePodcast()
            selectItem = podcastTitle + '. ' + str(currentPodcast +1) + ' из ' + str(len(podcastList))
        elif activeMode == 4:
            parseYoutubeChannels()
            selectItem = channelTitle + '. ' + str(currentChannel +1) + ' из ' + str(len(channelList))
        else: #?
            text = 'включаю ' + translateListModes[activeMode] + '. Выбрано: ' + selectItem
        speak(text)
    elif activeMode == 1:  # player
        if player == None:
            playFile(files[currentNumberFile])
            playing = True
        else:
            if playing == True:
                player.pause()
                playing = False
            else:
                player.play()
                playing = True
    elif activeMode == 2:  # radio
        if player != None:
            quitPlayer()
        else:
            playFile(station[stationNumber])
    elif activeMode == 3:  #  all podcasts
        activeMode = 5
        selectItem = podcastName[currentElement] + '. ' + str(currentElement +1) + ' из ' + str(totalElements)
        speak(podcastTitle + '. Выбрано: ' + selectItem)
    elif activeMode == 4:  #  all channel
        activeMode = 6
        selectItem = parseYoutubeVideo()
        speak(channelTitle + '. Выбрано: ' + selectItem)
    elif activeMode == 5:  # current podcast
        if not podcastName:
            speak('Этот подкаст не имеет аудио версии')
        else:
            if player == None:
                playFile(podcastUrl[currentElement])
                playing = True
            else:
                if playing == True:
                    player.pause()
                    playing = False
                else:
                    player.play()
                    playing = True
    elif activeMode == 6:  # current youtube file
        if player == None:
            playFile(youtubeAudioUrl)
            playing = True
        else:
            if playing == True:
                player.pause()
                playing = False
            else:
                player.play()
                playing = True

def actionPressKeyEnter():
    global activeMode, selectMode, player
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements
    global channelList, currentChannel, channelTitle, youtubeVideoUrl, youtubeAudioUrl
    if activeMode == 0:  # mainMenu
        activeMode = selectMode
        if activeMode == 0:
            selectItem = translateListModes[activeMode]
            text = selectItem
        if activeMode == 1:
            selectItem = files[currentNumberFile]
            if os.path.isdir(selectItem):
                selectItem = 'директория: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
            else:
                selectItem = 'файл: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
        elif activeMode == 2:
            selectItem = stationName[stationNumber] + '. ' + str(stationNumber+1) + ' из ' + str(len(station))
        elif activeMode == 3:
            parsePodcast()
            selectItem = podcastTitle + '. ' + str(currentPodcast +1) + ' из ' + str(len(podcastList))
        elif activeMode == 4:
            parseYoutubeChannels()
            selectItem = channelTitle + '. ' + str(currentChannel +1) + ' из ' + str(len(channelList))
        else: #?
            text = 'включаю ' + translateListModes[activeMode] + '. Выбрано: ' + selectItem
        speak(text)
    elif activeMode == 1:  # player
        if player == None:
            playFile(files[currentNumberFile])
            playing = True
        else:
            player.stop()
            playing = False
            player = None
    elif activeMode == 2:  # radio
        if player != None:
            quitPlayer()
        else:
            playFile(station[stationNumber])
    elif activeMode == 3:  #  all podcasts
        activeMode = 5
        selectItem = podcastName[currentElement] + '. ' + str(currentElement +1) + ' из ' + str(totalElements)
        speak(podcastTitle + '. Выбрано: ' + selectItem)
    elif activeMode == 4:  #  all channel
        activeMode = 6
        selectItem = parseYoutubeVideo()
        speak(channelTitle + '. Выбрано: ' + selectItem)
    elif activeMode == 5:  # current podcast
        if player == None:
            playFile(podcastUrl[currentElement])
            playing = True
        else:
            if playing == True:
                player.pause()
                playing = False
            else:
                player.play()
                playing = True
    elif activeMode == 6:  # current youtube file
        if player == None:
            playFile(youtubeAudioUrl)
            playing = True
        else:
            if playing == True:
                player.pause()
                playing = False
            else:
                player.play()
                playing = True

def actionPressKeyLeft():
    global activeMode, selectMode
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements
    global channelList, currentChannel, channelTitle, youtubeVideoUrl, youtubeAudioUrl
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('press left')
    if activeMode < len(listModes):
        activeMode = 0
        text = translateListModes[selectMode]
    if activeMode == 5:
        activeMode = 3
        text = translateListModes[activeMode] + '. ' + podcastTitle + '. ' + str(currentPodcast+1) + ' из ' + str(len(podcastList))
    quitPlayer()
    if activeMode == 6:
        activeMode = 4
        currentElement = 0
        text = translateListModes[activeMode] + '. ' + channelTitle + '. ' + str(currentChannel+1) + ' из ' + str(len(channelList))
    quitPlayer()
    speak(text)

def actionPressKeyRight():
    global activeMode, selectMode
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements, selectItem
    global channelList, currentChannel, channelTitle, youtubeVideoUrl, youtubeAudioUrl
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('press right')
    if activeMode == 0:
        activeMode = selectMode
        if activeMode == 1:
            if os.path.isdir(files[currentNumberFile]):
                text = str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' директория: ' + files[currentNumberFile]
            else:    
                text = str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' файл: ' + files[currentNumberFile]
        elif activeMode == 2:
            text = str(stationNumber + 1) + ' из ' + str(len(station)) + stationName[stationNumber]
        elif activeMode == 3:
            parsePodcast()
            text = translateListModes[activeMode] + '. Выбрано: ' + podcastTitle + '. ' + str(currentPodcast +1) + ' из ' + str(len(podcastList))
        elif activeMode == 4:
            parseYoutubeChannels()
            text = translateListModes[activeMode] + '. Выбрано: ' + channelTitle + '. ' + str(currentChannel +1) + ' из ' + str(len(channelList))
    elif activeMode == 3:  #  all podcasts
        activeMode = 5
        if not podcastName:
            text = 'Этот подкаст не имеет аудио версии'
        else:
            selectItem = podcastName[currentElement] + '. ' + str(currentElement +1) + ' из ' + str(totalElements)
            text = podcastTitle + '. Выбрано: ' + selectItem
    elif activeMode == 4:  #  youtube mode
        activeMode = 6
        selectItem = parseYoutubeVideo()
        text = channelTitle + '. Выбрано: ' + selectItem
    elif activeMode == 5:  #  current podcasts
        if not podcastName:
            text = 'Этот подкаст не имеет аудио версии'
        else:
            selectItem = podcastName[currentElement] + '. ' + str(currentElement +1) + ' из ' + str(totalElements)
            text = podcastTitle + '. Выбрано: ' + selectItem
    elif activeMode == 6:  #  current youtube file
        selectItem = parseYoutubeVideo()
        text = channelTitle + '. Выбрано: ' + selectItem
    speak(text)

def actionPressKeyUp():
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('press up')
    global currentNumberFile, selectMode, stationNumber, player, playing
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements
    global channelList, currentChannel, channelTitle, youtubeVideoUrl, youtubeAudioUrl
    if activeMode == 0:  # main menu
        if selectMode > 0:
            selectMode -= 1
        speak(translateListModes[selectMode])
    elif activeMode == 1:  # player
        if currentNumberFile>0:
            currentNumberFile -= 1
        if os.path.isdir(files[currentNumberFile]):
            text = str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' директория: ' + files[currentNumberFile]
        else:    
            text = str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' файл: ' + files[currentNumberFile]
        speak(text)
    elif activeMode == 2:  # radio
        if stationNumber > 0:
            stationNumber -= 1
            if playing == False:
                speak(str(stationNumber + 1) + ' из ' + str(len(station)) + stationName[stationNumber])
            else:
                if player != None:
                    quitPlayer()
                    playFile(station[stationNumber])
    elif activeMode == 3:  # all podcasts
        if currentPodcast > 0:
            currentPodcast -= 1
            parsePodcast()
            speak(podcastTitle + '. ' + str(currentPodcast + 1) + ' из ' + str(len(podcastList)))
    elif activeMode == 4:  # all channels
        if currentChannel > 0:
            currentChannel -= 1
            parseYoutubeChannels()
            speak(channelTitle + '. ' + str(currentChannel + 1) + ' из ' + str(len(channelList)))
    elif activeMode == 5:  # current podcast
        if currentElement > 0:
            currentElement -= 1
            if playing == False:
                if podcastName != []:
                    text = podcastName[currentElement] + '. ' + str(currentElement + 1) + ' из ' + str(totalElements)
                else:
                    text = 'У этого подкаста нет аудио версии'
                speak(text)
            else:
                if player != None:
                    quitPlayer()
                    if podcastName != []:
                        playFile(podcastUrl[currentElement])
                    else:
                        speak('У этого подкаста нет аудио версии')
    elif activeMode == 6:  # current youtube file
        if currentElement > 0:
            currentElement -= 1
            if playing == False:
                speak(str(currentElement + 1) + ' из ' + str(totalElements) + ' ' + parseYoutubeVideo())
            else:
                if player != None:
                    quitPlayer()
                playFile(youtubeAudioUrl)

def actionPressKeyDown():
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('press down')
    global currentNumberFile, selectMode, stationNumber, player, playing
    global podcastList, podcastTitle, podcastName, podcastUrl, currentPodcast, currentElement, totalElements
    global channelList, currentChannel, channelTitle, youtubeVideoUrl, youtubeAudioUrl
    if activeMode == 0:  # main menu
        if selectMode < len(listModes)-1:
            selectMode += 1
        speak(translateListModes[selectMode])
    elif activeMode == 1:  # player
        if currentNumberFile < (countFiles -1):
            currentNumberFile += 1
        if os.path.isdir(files[currentNumberFile]):
            text = str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' директория: ' + files[currentNumberFile]
        else:
            text = str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' файл: ' + files[currentNumberFile]
        speak(text)
    elif activeMode == 2:  # radio
        if stationNumber <len(station)-1:
            stationNumber += 1
            if playing == False:
                speak(str(stationNumber + 1) + ' из ' + str(len(station)) + stationName[stationNumber])
            else:
                if player != None:
                    quitPlayer()
                    playFile(station[stationNumber])
    elif activeMode == 3:  # all podcasts
        if currentPodcast < len(podcastList):
            currentPodcast += 1
            parsePodcast()
            speak(podcastTitle + '. ' + str(currentPodcast + 1) + ' из ' + str(len(podcastList)))
    elif activeMode == 4:  # all channels
        if currentChannel < len(channelList)-1:
            currentChannel += 1
            parseYoutubeChannels()
            speak(channelTitle + '. ' + str(currentChannel + 1) + ' из ' + str(len(channelList)))
    elif activeMode == 5:  # current podcast
        if currentElement < totalElements:
            currentElement += 1
            if playing == False:
                if podcastName != []:
                    text = podcastName[currentElement] + '. ' + str(currentElement + 1) + ' из ' + str(totalElements)
                else:
                    text = 'У этого подкаста нет аудио версии'
                speak(text)
            else:
                if player != None:
                    quitPlayer()
                    if podcastName != []:
                        playFile(podcastUrl[currentElement])
                    else:
                        speak('У этого подкаста нет аудио версии')
    elif activeMode == 6:  # current youtube file
        if currentElement < totalElements-1:
            currentElement += 1
            if playing == False:
                speak(str(currentElement + 1) + ' из ' + str(totalElements) + ' ' + parseYoutubeVideo())
            else:
                if player != None:
                    quitPlayer()
                speak(parseYoutubeVideo())
                playFile(youtubeAudioUrl)

def quitPlayer():
    global player, playing
    if player!=None:
        if playing != False:
            playing = False
        player.quit()
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('exit player')

def playerExit(code):
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('exit code player: %s', code)
    global playing, player
    playing=False
    player = None

def playFile(url):
    global player,playing
    if player==None:
        player=OMXPlayer(url)
        player.set_volume(volume)
        player.exitEvent += lambda _, exit_code: playerExit(exit_code)
    else:
        player.load(url)
    playing=True
    if logging != None:
        logger = logging.getLogger(listModes[activeMode])
        logger.debug('playing: %s', url)

def getDevice():
    for fn in evdev.list_devices():
        device = evdev.InputDevice(fn)
        caps = device.capabilities()
        if evdev.events.EV_KEY in caps:
            if evdev.ecodes.KEY_1 in caps[evdev.events.EV_KEY]:
                return device
    raise IOError('No keyboard found')

dev = getDevice()
if logging != None:
    logger = logging.getLogger(listModes[activeMode])
    logger.debug(dev)

for ev in dev.read_loop():
    if ev.type == evdev.ecodes.EV_KEY:
        active=dev.active_keys()
        if evdev.ecodes.KEY_LEFTCTRL in active and (evdev.ecodes.KEY_X in active or evdev.ecodes.KEY_C in active):
           quitPlayer()           
           break

        if ev.code ==  evdev.ecodes.KEY_ESC and ev.value == 1:
            os.system('sudo shutdown -h now')

        if ev.code ==  evdev.ecodes.KEY_T and ev.value == 1:
            speakTime()
        
        if ev.code ==  evdev.ecodes.KEY_D and ev.value == 1:
            speakDate()

        if ev.code ==  evdev.ecodes.KEY_1 and ev.value == 1:
            decreseVolume()
        if ev.code ==  evdev.ecodes.KEY_2 and ev.value == 1:
            increseVolume()

        if ev.code ==  evdev.ecodes.KEY_SPACE and ev.value == 1:
            actionPressKeySpace()

        if ev.code ==  evdev.ecodes.KEY_ENTER and ev.value == 1:
            actionPressKeyEnter()

        if ev.code ==  evdev.ecodes.KEY_LEFT and ev.value == 1:
            actionPressKeyLeft()

        if ev.code ==  evdev.ecodes.KEY_RIGHT and ev.value == 1:
            actionPressKeyRight()

        if ev.code ==  evdev.ecodes.KEY_UP and ev.value == 1:
            actionPressKeyUp()

        if ev.code ==  evdev.ecodes.KEY_DOWN and ev.value == 1:
            actionPressKeyDown()
