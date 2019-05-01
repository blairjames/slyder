#!/usr/bin/env python3

from requests import session
from typing import List
from os import getcwd
import bs4


class Slyder:

    def __init__(self):
        self.indicators = []
        self.config_file: str = getcwd() + "/slyder.conf"
        self.domain: str = "http://xmh57jrzrnw6insl.onion"
        self.path: str = "/"
        self.logfile: str = getcwd() + "/slyder.log"


    def set_indicators(self):
         with open(self.config_file, "r") as file:
             self.indicators = [l for l in file.readlines()]


    def get_webpage(self, url: str, path: str):
        try:
            s = session()
            s.proxies = {}
            s.headers = {}
            s.proxies['http'] = 'socks5h://localhost:9050'
            s.proxies['https'] = 'socks5h://localhost:9050'
            s.headers['User-agent'] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)"
            res = s.get(url + path, headers = s.headers)
            return res.text
        except Exception as e:
            print("Error! in get_webpage: " + str(e))


    def writer(self, chunk: List):
        try:
            with open(self.logfile, "a") as file:
                file.writelines(chunk)
        except Exception as e:
            print("Error! in writer: " + str(e))


    def search_content(self, content: str, indicators: List):
        try:
            lines = content.splitlines()
            hits = []
            for i in indicators:
                hits = [l + "\n" for l in lines if i in l]
                if hits:
                    hits += hits
            if hits.__len__() > 0:
                return hits
        except Exception as e:
            print("Error! in search_content: " + str(e))


    def soup_links(self, web_content):
        bs = bs4.BeautifulSoup(web_content, "html.parser")
        anchors = bs.find('a')
        if not anchors:
            return


    def alert(self, hits: List):
        print("\nIndicators located in content: \n")
        [print(i + "\n") for i in hits]
        print("\nWere located in the following content:")


    def controller(self):
        #TODO: add recursion
        text = self.get_webpage(self.domain, self.path)
        self.soup_links(text)
        hits = self.search_content(text, self.indicators)
        if hits:
            self.alert(hits)


def singleton() -> Slyder:
    #TODO: read conf file and set instance vars
    new_slider = Slyder()
    new_slider.set_indicators()
    return new_slider


def main():
    s = singleton()
    s.controller()


if __name__ == '__main__':
    main()