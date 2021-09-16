import os
class Action:
    def pressKeySpace(self, app):
        if app.activeMode == 0:  # mainMenu
            app.activeMode = app.selectMode
            if app.activeMode == 0:
                selectItem = app.listModes[app.activeMode]
                text = selectItem 
            elif app.activeMode == 1:
                selectItem = app.player.files[app.player.currentNumberFile]
                if os.path.isdir(selectItem):
                    selectItem = 'директория: ' + selectItem + str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles)
                else:
                    selectItem = 'файл: ' + selectItem + str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles)
                text = selectItem
            elif app.activeMode == 2:
                selectItem = app.radio.stationName[app.radio.stationNumber] + '. ' + str(app.radio.stationNumber+1) + ' из ' + str(len(app.radio.station))
                text = selectItem
            elif app.activeMode == 3:
                app.podcast.parsePodcast()
                selectItem = app.podcast.podcastTitle + '. ' + str(app.podcast.currentPodcast +1) + ' из ' + str(len(app.podcast.podcastList))
                text = selectItem
            elif app.activeMode == 4:
                app.youtube.parseYoutubeChannels()
                selectItem = app.youtube.channelTitle + '. ' + str(app.youtube.currentChannel +1) + ' из ' + str(len(app.youtube.channelList))
                text = selectItem
            else: #?
                text = 'включаю ' + app.listModes[app.activeMode] + '. Выбрано: ' + selectItem
            app.display(text)

        elif app.activeMode == 1:  # player
            if app.player.player == None:
                app.player.playFile(app.player.files[app.player.currentNumberFile])
                app.player.playing = True
            else:
                if app.player.playing == True:
                    app.player.player.pause()
                    app.player.playing = False
                else:
                    app.player.player.play()
                    app.player.playing = True
        elif app.activeMode == 2:  # radio
            if app.player.player != None:
                app.player.quitPlayer()
            else:
                app.player.playFile(app.radio.station[app.radio.stationNumber])
        elif app.activeMode == 3:  #  all podcasts
            app.activeMode = 5
            selectItem = app.podcast.podcastName[app.podcast.currentElement] + '. ' + str(app.podcast.currentElement +1) + ' из ' + str(app.podcast.totalElements)
            text = app.podcast.podcastTitle + '. Выбрано: ' + selectItem
            app.display(text)
        elif app.activeMode == 4:  #  all channel
            app.activeMode = 6
            selectItem = app.youtube.parseYoutubeVideo()
            text = app.youtube.channelTitle + '. Выбрано: ' + selectItem
            app.display(text)
        elif app.activeMode == 5:  # current podcast
            if not app.podcast.podcastName:
                text = 'Этот подкаст не имеет аудио версии'
                app.display(text)
            else:
                if app.player.player == None:
                    app.player.playFile(app.podcast.podcastUrl[app.podcast.currentElement])
                    app.player.playing = True
                else:
                    if app.player.playing == True:
                        app.player.player.pause()
                        app.player.playing = False
                    else:
                        app.player.player.play()
                        app.player.playing = True
        elif app.activeMode == 6:  # current youtube file
            if app.player.player == None:
                app.player.playFile(app.youtube.youtubeAudioUrl)
                app.player.playing = True
            else:
                if app.player.playing == True:
                    app.player.player.pause()
                    app.player.playing = False
                else:
                    app.player.player.play()
                    app.player.playing = True
    
    def pressEnter(self, app):
        if app.activeMode == 0:  # mainMenu
            app.activeMode = app.selectMode
            if app.activeMode == 0:
                selectItem = app.listModes[app.activeMode]
                text = selectItem
            if app.activeMode == 1:
                selectItem = app.player.files[app.player.currentNumberFile]
                if os.path.isdir(selectItem):
                    selectItem = 'директория: ' + selectItem + str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles)
                else:
                    selectItem = 'файл: ' + selectItem + str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles)
            elif app.activeMode == 2:
                selectItem = app.radio.stationName[app.radio.stationNumber] + '. ' + str(app.radio.stationNumber+1) + ' из ' + str(len(app.radio.station))
            elif app.activeMode == 3:
                app.podcast.parsePodcast()
                selectItem = app.podcast.podcastTitle + '. ' + str(app.podcast.currentPodcast +1) + ' из ' + str(len(app.podcast.podcastList))
            elif app.activeMode == 4:
                app.youtube.parseYoutubeChannels()
                selectItem = app.youtube.channelTitle + '. ' + str(app.youtube.currentChannel +1) + ' из ' + str(len(app.youtube.channelList))
            text = 'включаю ' + app.listModes[app.activeMode] + '. Выбрано: ' + selectItem
            app.display(text)

        elif app.activeMode == 1:  # player
            if app.player.player == None:
                app.player.playFile(app.player.files[app.player.currentNumberFile])
                app.player.playing = True
            else:
                app.player.player.stop()
                app.player.playing = False
                app.player.player = None
        elif app.activeMode == 2:  # radio
            if app.player.player != None:
                app.player.quitPlayer()
            else:
                app.player.playFile(app.radio.station[app.radio.stationNumber])
        elif app.activeMode == 3:  #  all podcasts
            app.activeMode = 5
            selectItem = app.podcast.podcastName[app.podcast.currentElement] + '. ' + str(app.podcast.currentElement +1) + ' из ' + str(app.podcast.totalElements)
            text = app.podcast.podcastTitle + '. Выбрано: ' + selectItem
            app.display(text)
        elif app.activeMode == 4:  #  all channel
            app.activeMode = 6
            selectItem = app.youtube.parseYoutubeVideo()
            text = app.youtube.channelTitle + '. Выбрано: ' + selectItem
            app.display(text)
        elif app.activeMode == 5:  # current podcast
            if app.player.player == None:
                app.player.playFile(app.podcast.podcastUrl[app.podcast.currentElement])
                app.player.playing = True
            else:
                if app.player.playing == True:
                    app.player.player.pause()
                    app.player.playing = False
                else:
                    app.player.player.play()
                    app.player.playing = True
        elif app.activeMode == 6:  # current youtube file
            if app.player.player == None:
                app.player.playFile(app.youtube.youtubeAudioUrl)
                app.player.playing = True
            else:
                if app.player.playing == True:
                    app.player.player.pause()
                    app.player.playing = False
                else:
                    app.player.player.play()
                    app.player.playing = True
    
    def pressKeyLeft(self, app):
        if app.activeMode < len(app.listModes):
            app.activeMode = 0
            text = app.listModes[app.selectMode]
        if app.activeMode == 5:
            app.activeMode = 3
            text = app.listModes[app.activeMode] + '. ' + app.podcast.podcastTitle + '. ' + str(app.podcast.currentPodcast+1) + ' из ' + str(len(app.podcast.podcastList))
        app.player.quitPlayer()
        if app.activeMode == 6:
            app.activeMode = 4
            app.youtube.currentElement = 0
            text = app.listModes[app.activeMode] + '. ' + app.youtube.channelTitle + '. ' + str(app.youtube.currentChannel+1) + ' из ' + str(len(app.youtube.channelList))
        app.player.quitPlayer()
        app.display(text)
    
    def pressKeyRight(self, app):
        if app.activeMode == 0:
            app.activeMode = app.selectMode
            if app.activeMode == 1:
                if os.path.isdir(app.player.files[app.player.currentNumberFile]):
                    text = str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles) + ' директория: ' + app.player.files[app.player.currentNumberFile]
                else:    
                    text = str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles) + ' файл: ' + app.player.files[app.player.currentNumberFile]
            elif app.activeMode == 2:
                text = str(app.radio.stationNumber + 1) + ' из ' + str(len(app.radio.station)) + app.radio.stationName[app.radio.stationNumber]
            elif app.activeMode == 3:
                app.podcast.parsePodcast()
                text = app.listModes[app.activeMode] + '. Выбрано: ' + app.podcast.podcastTitle + '. ' + str(app.podcast.currentPodcast +1) + ' из ' + str(len(app.podcast.podcastList))
            elif app.activeMode == 4:
                app.youtube.parseYoutubeChannels()
                text = app.listModes[app.activeMode] + '. Выбрано: ' + app.youtube.channelTitle + '. ' + str(app.youtube.currentChannel +1) + ' из ' + str(len(app.youtube.channelList))

        elif app.activeMode == 3:  #  all podcasts
            app.activeMode = 5
            if not app.podcast.podcastName:
                text = 'Этот подкаст не имеет аудио версии'
            else:
                selectItem = app.podcast.podcastName[app.podcast.currentElement] + '. ' + str(app.podcast.currentElement +1) + ' из ' + str(app.podcast.totalElements)
                text = app.podcast.podcastTitle + '. Выбрано: ' + selectItem
        elif app.activeMode == 4:  #  youtube mode
            app.activeMode = 6
            app.youtube.selectItem = app.youtube.parseYoutubeVideo()
            text = app.youtube.channelTitle + '. Выбрано: ' + app.youtube.selectItem
        elif app.activeMode == 5:  #  current podcasts
            if not app.podcast.podcastName:
                text = 'Этот подкаст не имеет аудио версии'
            else:
                selectItem = app.podcast.podcastName[app.podcast.currentElement] + '. ' + str(app.podcast.currentElement +1) + ' из ' + str(app.podcast.totalElements)
                text = app.podcast.podcastTitle + '. Выбрано: ' + selectItem
        elif app.activeMode == 6:  #  current youtube file
            selectItem = app.youtube.parseYoutubeVideo()
            text = app.youtube.channelTitle + '. Выбрано: ' + selectItem
        app.display(text)
    
    def pressKeyUp(self, app):
        if app.activeMode == 0:  # main menu
            if app.selectMode > 0:
                app.selectMode -= 1
            text = app.listModes[app.selectMode]
            app.display(text)
        elif app.activeMode == 1:  # player
            if app.player.currentNumberFile>0:
                app.player.currentNumberFile -= 1
            if os.path.isdir(app.player.files[app.player.currentNumberFile]):
                text = str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles) + ' директория: ' + app.player.files[app.player.currentNumberFile]
            else:    
                text = str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles) + ' файл: ' + app.player.files[app.player.currentNumberFile]
            app.display(text)
        elif app.activeMode == 2:  # radio
            if app.radio.stationNumber > 0:
                app.radio.stationNumber -= 1
                if app.player.playing == False:
                    text = str(app.radio.stationNumber + 1) + ' из ' + str(len(app.radio.station)) + app.radio.stationName[app.radio.stationNumber]
                    app.display(text)
                else:
                    if app.player.player != None:
                        app.player.quitPlayer()
                        text = app.radio.stationName[app.radio.stationNumber]
                        app.display(text)
                        app.player.playFile(app.radio.station[app.radio.stationNumber])
        elif app.activeMode == 3:  # all podcasts
            if app.podcast.currentPodcast > 0:
                app.podcast.currentPodcast -= 1
                app.podcast.parsePodcast()
                text = app.podcast.podcastTitle + '. ' + str(app.podcast.currentPodcast + 1) + ' из ' + str(len(app.podcast.podcastList))
                app.display(text)
        elif app.activeMode == 4:  # all channels
            if app.youtube.currentChannel > 0:
                app.youtube.currentChannel -= 1
                app.youtube.parseYoutubeChannels()
                text = app.youtube.channelTitle + '. ' + str(app.youtube.currentChannel + 1) + ' из ' + str(len(app.youtube.channelList))
                app.display(text)
        elif app.activeMode == 5:  # current podcast
            if app.podcast.currentElement > 0:
                app.podcast.currentElement -= 1
                if app.player.playing == False:
                    if app.podcast.podcastName != []:
                        text = app.podcast.podcastName[app.podcast.currentElement] + '. ' + str(app.podcast.currentElement + 1) + ' из ' + str(app.podcast.totalElements)
                    else:
                        text = 'У этого подкаста нет аудио версии'
                    app.display(text)
                else:
                    if app.player.player != None:
                        app.player.quitPlayer()
                        if app.podcast.podcastName != []:
                            text = app.podcast.podcastName[app.podcast.currentElement]
                            app.display(text)
                            app.player.playFile(app.podcast.podcastUrl[app.podcast.currentElement])
                        else:
                            text = 'У этого подкаста нет аудио версии'
                            app.display(text)
        elif app.activeMode == 6:  # current youtube file
            if app.youtube.currentElement > 0:
                app.youtube.currentElement -= 1
                if app.player.playing == False:
                    text = str(app.youtube.currentElement + 1) + ' из ' + str(app.youtube.totalElements) + ' ' + app.youtube.parseYoutubeVideo()
                    app.display(text)
                else:
                    if app.player.player != None:
                        app.player.quitPlayer()
                    text = app.youtube.parseYoutubeVideo(info = False)
                    app.display(text)
                    app.player.playFile(app.youtube.youtubeAudioUrl)
    
    def pressKeyDown(self, app):
        if app.activeMode == 0:  # main menu
            if app.selectMode < len(app.listModes)-1:
                app.selectMode += 1
            text = app.listModes[app.selectMode]
            app.display(text)
        elif app.activeMode == 1:  # player
            if app.player.currentNumberFile < (app.player.countFiles -1):
                app.player.currentNumberFile += 1
            if os.path.isdir(app.player.files[app.player.currentNumberFile]):
                text = str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles) + ' директория: ' + app.player.files[app.player.currentNumberFile]
            else:
                text = str(app.player.currentNumberFile + 1) + ' из ' + str(app.player.countFiles) + ' файл: ' + app.player.files[app.player.currentNumberFile]
            app.display(text)
        elif app.activeMode == 2:  # radio
            if app.radio.stationNumber <len(app.radio.station)-1:
                app.radio.stationNumber += 1
                if app.player.playing == False:
                    text = str(app.radio.stationNumber + 1) + ' из ' + str(len(app.radio.station)) + app.radio.stationName[app.radio.stationNumber]
                    app.display(text)
                else:
                    if app.player.player != None:
                        app.player.quitPlayer()
                        text = app.radio.stationName[app.radio.stationNumber]
                        app.display(text)
                        app.player.playFile(app.radio.station[app.radio.stationNumber])
        elif app.activeMode == 3:  # all podcasts
            if app.podcast.currentPodcast < len(app.podcast.podcastList):
                app.podcast.currentPodcast += 1
                app.podcast.parsePodcast()
                text = app.podcast.podcastTitle + '. ' + str(app.podcast.currentPodcast + 1) + ' из ' + str(len(app.podcast.podcastList))
                app.display(text)
        elif app.activeMode == 4:  # all channels
            if app.youtube.currentChannel < len(app.youtube.channelList)-1:
                app.youtube.currentChannel += 1
                app.youtube.parseYoutubeChannels()
                text = app.youtube.channelTitle + '. ' + str(app.youtube.currentChannel + 1) + ' из ' + str(len(app.youtube.channelList))
                app.display(text)
        elif app.activeMode == 5:  # current podcast
            if app.podcast.currentElement < app.podcast.totalElements:
                app.podcast.currentElement += 1
                if app.player.playing == False:
                    if app.podcast.podcastName != []:
                        text = app.podcast.podcastName[app.podcast.currentElement] + '. ' + str(app.podcast.currentElement + 1) + ' из ' + str(app.podcast.totalElements)
                    else:
                        text = 'У этого подкаста нет аудио версии'
                    app.display(text)
                else:
                    if app.player.player != None:
                        app.player.quitPlayer()
                        if app.podcast.podcastName != []:
                            text = app.podcast.podcastName[app.podcast.currentElement]
                            app.display(text)
                            app.player.playFile(app.podcast.podcastUrl[app.podcast.currentElement])
                        else:
                            text = 'У этого подкаста нет аудио версии'
                            app.display(text)
        elif app.activeMode == 6:  # current youtube file
            if app.youtube.currentElement < app.youtube.totalElements-1:
                app.youtube.currentElement += 1
                if app.player.playing == False:
                    text = str(app.youtube.currentElement + 1) + ' из ' + str(app.youtube.totalElements) + ' ' + app.youtube.parseYoutubeVideo()
                    app.display(text)
                else:
                    if app.player.player != None:
                        app.player.quitPlayer()
                    text = app.youtube.parseYoutubeVideo(info = False)
                    app.display(text)
                    app.player.playFile(app.youtube.youtubeAudioUrl)
    