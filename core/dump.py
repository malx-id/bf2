'''
Name: Dump
Date: 13-07-2020
Edited: 4-08-2020
'''

from bs4 import BeautifulSoup
from requests import Session
import re

class Dump:

    def __init__(self, cookie):
        self.cookie = cookie
        self.req = Session()
        self.head = 'https://free.facebook.com'

        self.id = []

    def search_name(self, query):
        url = self.req.get(self.head+'/search/top/?q='+query, cookies=self.cookie).text
        parse = BeautifulSoup(url, 'html.parser')
        a = parse.find('a', string='Lihat Semua')['href']
        page = self.req.get(self.head+a, cookies=self.cookie).text

        try:
            while True:
                if 'Anda Tidak Dapat Menggunakan Fitur Ini Sekarang' in page:
                    break
                else:
                    a = re.findall(r'\<a\ href\=\"(.*?)\"\ class\=\"(.*?)\">', page)
                    for x in a:
                        try:
                            email = re.search(r'add\_friend\.php\?id\=(.*?)\&amp', x[0]).group(1)
                            self.id.append(email)
                        except:
                            pass
                    page = self.get_next_page(page, 'Lihat Hasil Selanjutnya')
                    print(f'\r    -> {str(len(self.id))} ID Telah Dikumpulkan', end='', flush=True)
        except:
            pass
        return self.id

    def likes(self, url_postingan):
        if 'permalink' in url_postingan:
            id_post = re.search(r'permalink\/(.*?)\/\?', url_postingan).group(1)
        elif 'posts' in url_postingan:
            id_post = re.search(r'posts\/(.*?)\/\?', url_postingan).group(1)
        url = self.head+'/ufi/reaction/profile/browser/?ft_ent_identifier='+id_post
        page = self.req.get(url, cookies=self.cookie).text
        try:
            while True:
                if 'Anda Tidak Dapat Menggunakan Fitur Ini Sekarang' in page:
                    break
                else:
                    a = re.findall(r'\<a\ href\=\"(.*?)\"\ class\=\"(.*?)\">', page)
                    for x in a:
                        try:
                            email = re.search(r'add\_friend\.php\?id\=(.*?)\&amp', x[0]).group(1)
                            self.id.append(email)
                        except:
                            pass
                    page = self.get_next_page(page, 'Lihat Selengkapnya')
                    print(f'\r    -> {str(len(self.id))} ID Telah Dikumpulkan', end='', flush=True)
        except:
            pass
        return self.id

    def user(self, fros, loop=True):
        me = self.req.get(self.head+fros, cookies=self.cookie).text
        page = self.get_next_page(me, 'Teman')
        try:
            if loop:
                while True:
                    if 'Anda Tidak Dapat Menggunakan Fitur Ini Sekarang' in page:
                        break
                    else:
                        self.get_id(page)
                        me = page
                        page = self.get_next_page(me, 'Lihat Teman Lain')
                        print(f'\r    -> {str(len(self.id))} ID Telah Dikumpulkan', end='', flush=True)
            else:
                self.get_id(page)
        except:
            pass
        return self.id

    def get_next_page(self, target, string):
        parse = BeautifulSoup(target, 'html.parser')
        a = parse.find_all('a', string=string)
        for x in a:
            if '/graphsearch' in str(x):
                page = self.req.get(x['href'], cookies=self.cookie).text
                return page
            elif '/ufi/reaction/profile/browser' or '/friends?' in str(x) or '/profile.php' in str(x):
                page = self.req.get(self.head+x['href'], cookies=self.cookie).text
                return page


    def get_id(self, page):
        a = re.findall(r'middle\"\>\<a\ class\=\"(.*?)\"\ href\=\"(.*?)\"\>', page)
        for x in a:
            if 'friends/hovercard/mbasic/' in x[1]:
                pass
            elif 'profile.php' in x[1]:
                try:
                    email = re.search(r'id\=(.*?)\&', x[1]).group(1)
                    self.id.append(email)
                except:
                    pass
            else:
                try:
                    email = re.search(r'\/(.*?)\?', x[1]).group(1)
                    self.id.append(email)
                except:
                    pass
