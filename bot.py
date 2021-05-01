import os
import random
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from secrets import min_followers, max_followers, min_following, max_following, comments
import secrets
from datetime import datetime

class Bot:

    def __init__(self):
        # self.save_to_file()
        # options = Options()
        # options.headless = True
        self.driver = webdriver.Firefox()

        now = datetime.now()
        self.current_time = now.strftime("%H:%M")
        
        self.scanned = []
        self.scanned_links = []
        self.followed_persons = []
        self.hashtags = secrets.hashtags

        self.import_files()
        self.login()

    def import_files(self):

        if os.path.exists('scanned_links.txt') and os.path.exists('followed_persons.txt'):
            
            with open('scanned_links.txt', 'r+') as scanned_links_file:
                for line in scanned_links_file:
                    line = line.replace('\n','')
                    self.scanned.append(line)

            with open('followed_persons.txt', 'r+') as followed_persons_file:
                for line in followed_persons_file:
                    line = line.replace('\n','')
                    self.followed_persons.append(line)

            self.info_chars("PL1KI TEKST0WE3 Z4IMP0RT0WAn3 D0 L1ST")
        else:

            print("Nie udało się wczytać jednego z plików tekstowych: 'scanned_links.txt, 'followed_persons.txt")
            sys.exit()

        with open('pass.json', 'r') as f:
            self.config = json.load(f)

    def info_chars(self, message):
        count = (len("[>---------[ \ "+message+" / ]----------<]")-4)
        print("[>"+"-"*count+"<]")
        print("[>---------[ \ "+message+" / ]----------<]")
        print("[>"+"-"*count+"<]")

    def if_ban(self):
        pass


    def find_element(self, path):
        time.sleep(random.uniform(2.2, 3.9))
        elements = self.driver.find_elements_by_xpath(path)
        tries = 4
        while len(elements) == 0:
            time.sleep(random.uniform(0.9, 2.1))
            try:
                elements = self.driver.find_elements_by_xpath(path)
                tries -= 1
                if tries <= 0:
                    fake_element = self.driver.find_element_by_xpath('/html/body/div[1]/section/footer/div/div[2]/div[2]/div')
                    return fake_element
            except:
                tries -= 1
                if tries <= 0:
                    fake_element = self.driver.find_element_by_xpath('/html/body/div[1]/section/footer/div/div[2]/div[2]/div')
                    return fake_element
                print("Nie znaleziono elementu")
                if len(self.driver.find_elements_by_xpath('/html/body/div[1]/section/div/div/div[2]/form/span/button')) == 1:
                    self.if_ban()

        return elements[0]
    
    def likeorcomment_follow(self):
        self.driver.back()
        time.sleep(3)
        if self.follows <= 60:
            self.find_element("/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button").click()
            self.follows += 1

        if self.likes <= 60:
            self.find_element("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
            self.likes += 1

        if self.comments <= 60:
            self.find_element("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button").click()
            self.find_element("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea").send_keys(random.choice(comments))
            self.find_element('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button[2]').click()
            self.comments += 1
  


    def check_profile(self, link):

        # if len(self.driver.find_elemnts_by_xpath('/html/body/div/div[1]/div/div/h2')) == 1:
        #     self.info_chars("BłĄd")
        #     time.sleep(600)

        self.driver.get(link)
        nick = self.find_element('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a').get_attribute('innerText')

        if nick not in self.scanned:
            self.find_element('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a').click()
            followers = self.find_element('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')
            following = self.find_element('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').get_attribute('innerText')
            followers = followers.replace(" ", "")
            following = following.replace(" ", "")
            if int(followers) > min_followers and int(followers) < max_followers and int(following) > min_following and int(following) < max_following:
                self.info_chars('U5er: '+nick+" | F0LL0werS: "+str(followers)+" | F0LL0winG: "+str(following)+" | [+]")
                self.likeorcomment_follow()
                self.followed_persons.append(nick)
            else:
                self.info_chars('U5er: '+nick+" | F0LL0werS: "+str(followers)+" | F0LL0winG: "+str(following)+" | [-]")
            self.scanned.append(nick)
        
        
    def save_to_file(self):

        with open('followed_persons.txt', 'w') as followed_persons_file:
            for line in self.followed_persons:
                followed_persons_file.write(line)
                followed_persons_file.write('\n')

        with open('scanned_links.txt', 'w') as scanned_links_file:
            for line in self.scanned:
                scanned_links_file.write(line)
                scanned_links_file.write('\n')

    def find_and_scan(self):

        actual_time = time.time()
        target_time = time.time() + 600
        self.likes = 0
        self.follows = 0
        self.comments = 0

        hashtag = random.choice(self.hashtags)
        self.hashtags.remove(hashtag)

        while actual_time < target_time:

            print(self.info_chars('SC4NNiNg P0sT5 o Ha$GT4Gu: ' + hashtag))
            self.find_element('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(hashtag)
            self.find_element('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div/div[2]/div[1]/div/div').click()

            def condition(link):
                return ".com/p/" in link.get_attribute("href")

            while len(self.scanned_links) < 500:
                try:
                    time.sleep(random.uniform(2.2, 3.4))
                    new_links = self.driver.find_elements_by_tag_name("a")
                    valid_links = list(filter(condition, new_links))

                    for link in valid_links:
                        if link not in self.scanned_links:
                            self.scanned_links.append(link.get_attribute('href'))
                    self.info_chars("Zeskanowane posty: " + str(len(self.scanned_links)))

                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except:
                    pass

            for _ in range(3):
                random.shuffle(self.scanned_links)

            for i in range(len(self.scanned_links)):
                actual_time = time.time()
                link = self.scanned_links[i]
                self.scanned_links.pop(i)
                try:
                    self.check_profile(link)
                except:
                    pass
                if i >= 500:
                    self.find_and_scan()
                elif actual_time > target_time:
                    target_time = time.time() + 600
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    self.target_time = time.time() + 600
                    self.info_chars("Od godz1nY | "+self.current_time + " | d0 g0dz1ny | " + current_time + " | B0t zD0Był " +str(self.likes)+ " LIKE, " + str(self.follows) + " FOLLOWS, " + str(self.comments) + " COMMENTS")
                    self.info_chars("PROF1L3 SP3ŁNI4JĄC3 WYMAG4N1A: " + str(self.follows) + "/" + str(len(self.scanned)))
                    self.save_to_file()
                    self.likes = 0
                    self.follows = 0
                    self.comments = 0

        self.save_to_file()
        self.find_and_scan()

    def login(self):

        self.username = self.config['username']
        self.password = self.config['password']
        print(self.info_chars('L0G0w4nie /\ 3Z4S : ' + self.current_time))
        self.driver.get('https://www.instagram.com/')
        try:
            self.find_element('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
        except:
            self.find_element('/html/body/div[2]/div/div/button[1]').click()
        self.find_element('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.find_element('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input').send_keys(self.password)
        self.find_element('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div').click()
        self.find_element('/html/body/div[1]/section/main/div/div/div/div/button').click()
        time.sleep(3)
        try:
            self.driver.find_element_by_css_selector('button.aOOlW:nth-child(2)').click()
        except:
            pass
        print(self.info_chars('L0G0w4ni3 Z4K0ńCz0n3'))
        self.find_and_scan()


def main():

    bot = Bot()

if __name__ == '__main__':

    main()