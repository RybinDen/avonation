#Speaking player for online radiostation and audiofiles.
#version 0.0.1
# Denis Rybin https://github.com/rybinden/avonation

from datetime import datetime
import os, evdev, time, glob
from omxplayer.player import OMXPlayer

listModes = ['mainMenu', 'player', 'radio']
translateListModes = ['Главное меню', 'Плеер', 'Радио']
countModess = len(listModes)
activeMode = 0
selectMode = 0

station = [
'http://mds-station.com:8000/mds',
'http://212.75.194.94:8000/KemMayakFM',
'http://icecast.vgtrk.cdnvideo.ru/vestifm_aac_64kbps',
'http://ic7.101.ru:8000/v11_1'
]
stationName = ['mds', 'Маяк', 'Вести фм', 'comedy']
stationNumber = 0

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
command = 'echo Авонация запущена. Режим: ' + translateListModes[activeMode] + ' | RHVoice-test -p aleksandr'
os.system(command)

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
    command = 'echo время: ' + str(hour) + ':' + m + ' | RHVoice-test -p aleksandr'
    os.system(command)

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
    command = 'echo дата: ' + d + ' ' + m + ', ' + w + ' | RHVoice-test -p aleksandr'
    os.system(command)

def actionPressKeySpace():
    print('space')
    global activeMode, selectMode, player, playing
    if activeMode == 0:  # mainMenu
        activeMode = selectMode
        if activeMode == 0:
            selectItem = translateListModes[activeMode]
        elif activeMode == 1:
            selectItem = files[currentNumberFile]
            if os.path.isdir(selectItem):
                selectItem = 'директория: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
            else:
                selectItem = 'файл: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
        elif activeMode == 2:
            selectItem = stationName[stationNumber] + '. ' + str(stationNumber+1) + ' из ' + str(len(station))
        if activeMode == 0:
            command = 'echo ' + selectItem + ' | RHVoice-test -p aleksandr'
        else:
            command = 'echo включаю ' + translateListModes[activeMode] + '. Выбрано: ' + selectItem + ' | RHVoice-test -p aleksandr'
        os.system(command)
    elif activeMode == 1:  # player
        print(currentNumberFile)
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

def actionPressKeyEnter():
    global activeMode, selectMode, player
    if activeMode == 0:  # mainMenu
        activeMode = selectMode
        if activeMode == 0:
            selectItem = translateListModes[activeMode]
        if activeMode == 1:
            selectItem = files[currentNumberFile]
            if os.path.isdir(selectItem):
                selectItem = 'директория: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
            else:
                selectItem = 'файл: ' + selectItem + str(currentNumberFile + 1) + ' из ' + str(countFiles)
        elif activeMode == 2:
            selectItem = stationName[stationNumber] + '. ' + str(stationNumber+1) + ' из ' + str(len(station))
        if activeMode == 0:
            command = 'echo ' + selectItem + ' | RHVoice-test -p aleksandr'
        else:
            command = 'echo включаю ' + translateListModes[activeMode] + '. Выбрано: ' + selectItem + ' | RHVoice-test -p aleksandr'
        os.system(command)
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

def actionPressKeyLeft():
    print('left')
    global activeMode, selectMode
    if activeMode != 0:
        activeMode = 0
        quitPlayer()
    command = 'echo ' + translateListModes[selectMode] + ' | RHVoice-test -p aleksandr'
    os.system(command)

def actionPressKeyRight():
    print('right')
    global activeMode, selectMode
    if activeMode == 0:
        activeMode = selectMode
        if activeMode == 1:
            if os.path.isdir(files[currentNumberFile]):
                command = 'echo ' + str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' директория: ' + files[currentNumberFile] + ' | RHVoice-test -p aleksandr'
            else:    
                command = 'echo ' + str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' файл: ' + files[currentNumberFile] + ' | RHVoice-test -p aleksandr'
        elif activeMode == 2:
            command = 'echo ' + str(stationNumber + 1) + ' из ' + str(len(station)) + stationName[stationNumber] + ' | RHVoice-test -p aleksandr'
        os.system(command)

def actionPressKeyUp():
    print('up')                
    global currentNumberFile, selectMode, stationNumber, player, playing
    if activeMode == 0:  # main menu
        if selectMode > 0:
            selectMode -= 1
        command = 'echo ' + translateListModes[selectMode] + ' | RHVoice-test -p aleksandr'
        os.system(command)
    elif activeMode == 1:  # player
        if currentNumberFile>0:
            currentNumberFile -= 1
        if os.path.isdir(files[currentNumberFile]):
            command = 'echo ' + str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' директория: ' + files[currentNumberFile] + ' | RHVoice-test -p aleksandr'
        else:    
            command = 'echo ' + str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' файл: ' + files[currentNumberFile] + ' | RHVoice-test -p aleksandr'
        os.system(command)
    elif activeMode == 2:  # radio
        if stationNumber > 0:
            stationNumber -= 1
            if playing == False:
                command = 'echo ' + str(stationNumber + 1) + ' из ' + str(len(station)) + stationName[stationNumber] + ' | RHVoice-test -p aleksandr'
                os.system(command)
            else:
                if player != None:
                    quitPlayer()
                    playFile(station[stationNumber])

def actionPressKeyDown():
    print('down')
    global currentNumberFile, selectMode, stationNumber, player, playing
    if activeMode == 0:  # main menu
        if selectMode < countModess-1:
            selectMode += 1
        command = 'echo ' + translateListModes[selectMode] + ' | RHVoice-test -p aleksandr'
        os.system(command)
    elif activeMode == 1:  # player
        if currentNumberFile < (countFiles -1):
            currentNumberFile += 1
        if os.path.isdir(files[currentNumberFile]):
            command = 'echo ' + str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' директория: ' + files[currentNumberFile] + ' | RHVoice-test -p aleksandr'
        else:
            command = 'echo ' + str(currentNumberFile + 1) + ' из ' + str(countFiles) + ' файл: ' + files[currentNumberFile] + ' | RHVoice-test -p aleksandr'
        os.system(command)
    elif activeMode == 2:  # radio
        if stationNumber <len(station)-1:
            stationNumber += 1
            if playing == False:
                command = 'echo ' + str(stationNumber + 1) + ' из ' + str(len(station)) + stationName[stationNumber] + ' | RHVoice-test -p aleksandr'
                os.system(command)
            else:
                if player != None:
                    quitPlayer()
                    playFile(station[stationNumber])

def quitPlayer():
    global player, playing
    if player!=None:
        if playing != False:
            playing = False
        player.quit()
    print('Exit')

def playerExit(code):
    print('exit',code)
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
    print('Playing:', url)
    playing=True

def getDevice():
    for fn in evdev.list_devices():
        device = evdev.InputDevice(fn)
        caps = device.capabilities()
        if evdev.events.EV_KEY in caps:
            if evdev.ecodes.KEY_1 in caps[evdev.events.EV_KEY]:
                return device
    raise IOError('No keyboard found')

dev = getDevice()
print(dev)

for ev in dev.read_loop():
    if ev.type == evdev.ecodes.EV_KEY:
        #print(evdev.categorize(ev))
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
