import requests, youtube_dl
from xml.etree import ElementTree
from datetime import date
class Youtube:
    channelList = []
    currentChannel = 0
    channelTitle = ''
    youtubeVideoUrl = []
    youtubeAudioUrl = ''  #current youtube audio link
    currentElement = 0
    totalElements = 10
    
    def parseYoutubeChannels(self):
        with open('../youtube.txt') as f:
            self.channelList = f.read().splitlines()
    
        url = 'http://www.youtube.com/feeds/videos.xml?channel_id=' + self.channelList[self.currentChannel]
        response = requests.get(url)
        root = ElementTree.fromstring(response.text)
        ns = '{http://www.w3.org/2005/Atom}'
        self.channelTitle = root.findtext(ns + 'title')
        element = 0
        for item in root.findall(ns + 'entry'):
            if element < self.totalElements:
                self.youtubeVideoUrl.insert(element, item.find(ns + 'link').get('href'))
                element += 1
            else:
                break
    
    def parseYoutubeVideo(self):
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
            r = ydl.extract_info(self.youtubeVideoUrl[self.currentElement], download=False) # Вставляем нашу ссылку с ютуба
        self.youtubeAudioUrl = r['url']
        message += r['title'] + ' '
        message += 'Просмотров: ' + str(r['view_count']) + '. '
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
    
        message += '. Длилтельность: '
        h, m, s = 0, 0, 0
        duration = r['duration']
        m = duration // 60
        if m >= 60:
            h = m // 60
            m = m % 60
        s = duration % 60
        if h:
            message += str(h) + ' час, '
        if m:
            message += str(m) + ' мин. '
        if s:
            message += str(s) + ' сек. '
        return message
    
    