import requests
from xml.etree import ElementTree
class Podcast:
    podcastList = []
    podcastTitle = ''
    podcastName = []
    podcastUrl = []
    currentPodcast = 0
    currentElement = 0
    totalElements = 10
    def parsePodcast(self):
        if len(self.podcastList) == 0:
            with open('../podcast.txt') as f:
                self.podcastList = f.read().splitlines()
        self.podcastName.clear()
        self.podcastUrl.clear()
        if self.currentElement != 0:
            self.currentElement = 0
        response = requests.get(self.podcastList[self.currentPodcast])
        root = ElementTree.fromstring(response.text)
        self.podcastTitle = root.findtext('channel/title')
        for item in root.findall('channel/item'):
            if self.currentElement == self.totalElements:
                break
            enclosure = item.find('enclosure')
            if enclosure != None:
                self.podcastName.insert(self.currentElement, item.findtext('title'))
                self.podcastUrl.insert(self.currentElement, enclosure.get('url'))
            self.currentElement += 1
        self.currentElement = 0

