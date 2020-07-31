import scrapy
import json
import os
import sys
import urllib
from subprocess import call
import pickle
class DomainsSpider(scrapy.Spider):
    name = "domains"

        
    def readSettings(self):
        path = os.getcwd()
        
        path = path + '\\domains\\querySettings.json'
        print(path)
        if not os.path.exists(path):
            return False

        with open(path) as settings:
            settings = json.load(settings)
            self.useCSS = bool(settings['flags'][0]['status'])
            self.useXPath = bool(settings['flags'][1]['status'])
            self.useRegex = bool(settings['flags'][3]['status'])
            self.useFunction = bool(settings['flags'][2]['status'])

            self.url = settings['url']
            self.queryText = settings['text'][0]['raw']
            self.functionText = settings['text'][1]['raw']
            self.regexText = settings['text'][2]['raw']
            print(self.useCSS)
            print(self.useXPath)
            print(self.useRegex)
            print(self.useFunction)

            print(self.url)
            print(self.queryText)
            print(self.functionText)
            print(self.regexText)

            with open('extra_python.py', 'w') as extra_python:

                boiler='''
import pickle
if __name__ == '__main__':
    result = pickle.load(open('output.txt', 'rb'))
    print(result)
    result_changed = extra_python(result)
    if result_changed == None:
        pass
    else:
        open('output.txt', 'w').close()
        pickle.dump(result_changed, open('output.txt', 'wb'))'''
                self.functionText = self.functionText + boiler
                extra_python.write(self.functionText)
            try:
                fp = urllib.request.urlopen(self.url)
                return True
            except:
                return False
        return True
    
    def start_requests(self):
        if not self.readSettings():
            print('rip', '-'*50)
            return
        urls = [
            self.url
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.readSettings()
        page = response.url.split("/")[-2]
        filename = 'output.html'
        with open(filename, 'wb') as f:
            result = response
            if self.useCSS:
                result = result.css(self.queryText)
            
            if self.useXPath:
                result = result.xpath(self.queryText)

            if self.useRegex:
                result = result.re(self.regexText)
            else:
                result = result.getall()

            if self.useFunction:
                pickle.dump(result, open('output.txt', 'wb'))
                # set a timeout probably
                call(['py', 'extra_python.py'])
                result = pickle.load(open('output.txt', 'rb'))
            print(result)
            pickle.dump(result, open('output.txt', 'wb'))
        self.log('Saved file %s' % filename)