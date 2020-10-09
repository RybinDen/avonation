import os, time
from datetime import date, datetime
from avonation.config import Config
class Sint:
    def __init__(self):
        config = Config()
        self.config = config
        self.synthesizer = config.get_setting("general", "synthesizer")

    def speak(self, text):
        if self.synthesizer == 'espeak':
            command = self.synthesizer + ' -v ' + self.config.get_setting("general", "language") + ' -a ' + self.config.get_setting(self.synthesizer, "volume") + ' -p ' + self.config.get_setting(self.synthesizer, "pitch") + ' -s ' + self.config.get_setting(self.synthesizer, "speed") + ' "' + text + '"'
        if self.synthesizer == 'rhvoice':
            command = 'echo "' + text + '" | RHVoice-test -p ' + self.config.get_setting(self.synthesizer, "voice")
        os.system(command)

    def speakTime(self):
        time_checker = datetime.now()
        hour = time_checker.hour
        minut = time_checker.minute
        if minut < 10:
            m = '0' + str(minut)
        else:
            m = str(minut)
        self.speak('время: ' + str(hour) + ':' + m)

    def speakDate(self):
        time_checker = datetime.now()
        day = time_checker.day
        daysName = (
            'первое',
            'второе',
            'третье',
            'четвертое',
            'пятое',
            'шестое',
            'седьмое',
            'восьмое',
            'девятое',
            'десятое',
            'одиннадцатое',
            'двенадцатое',
            'тринадцатое',
            'четырнадцатое',
            'пятнадцатое',
            'шестнадцатое',
            'семнадцатое',
            'восемнадцатое',
            'деветнадцатое',
            'двадцатое',
            'двадцать первое',
            'двадцать второе',
            'двадцать третье',
            'двадцать четвертое',
            'двадцать пятое',
            'двадцать шестое',
            'двадцать седьмое',
            'двадцать восьмое',
            'двадцать девятое',
            'тридцатое',
            'тридцать первое'
        )
        d = daysName[day-1]
        month = time_checker.month
        monthName = (
            'Января',
            'февраля',
            'марта',
            'апреля',
            'мая',
            'июня',
            'июля',
            'августа',
            'сентября',
            'октября',
            'ноября',
            'векабря'
        )
        m = monthName[month-1]
        weekday = time_checker.weekday()
        weekdayName = (
            'понедельник',
            'вторник',
            'среда',
            'четверг',
            'пятница',
            'суббота',
            'воскресенье'
        )
        w = weekdayName[weekday]
        self.speak('дата: ' + d + ' ' + m + ', ' + w)

