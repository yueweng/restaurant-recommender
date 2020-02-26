import numpy as numpy
import pandas as pd
import time
import copy
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import time

class RestaurantSetup():
    def __init__(self, url):
        self.url = url
        self.request = requests.get(self.url, headers={'user-agent': 'Mozilla/5.0'})

    def get_pag_num(self):
      soup = BeautifulSoup(self.request.content, "html")
      pag_div = soup.find("div", {"class": "pagination-links-container__373c0__1vHLX"})
      sib_div = pag_div.find_next_sibling()
      pag_num = int(sib_div.text.split("of")[-1])

      return pag_num

    def get_restaurant_list(self, pages):
      li = []
      for p in range(pages):
        start = 30*p
        url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San%20Francisco%2C%20CA&ns=1&start=" + str(start)
        print(url)
        r_url = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        rsoup = BeautifulSoup(r_url.content, "html")
        container_div = rsoup.findAll("div", {"class": "container__373c0__ZB8u4"})
        print(container_div)
        for container in container_div:
          ind_rest = {}
          alink = container.find("a", {"class": "lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"})
          image_div = container.find("img", {"class": "lemon--img__373c0__3GQUb photo-box-img__373c0__O0tbt"})
          info_div = container.find("div", {"class": "lemon--div__373c0__1mboc container__373c0__39jSv padding-l2__373c0__1Dr82 border-color--default__373c0__3-ifU text-align--right__373c0__1XDu3"})
          phone_div = info_div.findAll("p", {"class": "lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--right__373c0__1f0KI text-size--small__373c0__3NVWO"})[0]
          address_div = info_div.find("span", {"class": "lemon--span__373c0__3997G raw__373c0__3rcx7"})
          neighborhood_div = info_div.findAll("p", {"class": "lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--right__373c0__1f0KI text-size--small__373c0__3NVWO"})[-1]
          stars_div = container.find("div", {"class": "i-stars__373c0__1T6rz"})
          review_div = container.find("span", {"class": "reviewCount__373c0__2r4xT"})
          price_div = container.find("span", {"class": "priceRange__373c0__2DY87"})
          cuisine_div = container.findAll("a", {"class": "lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--default__373c0__7tls6"})
          cuisines = []
          for c in cuisine_div:
              cuisines.append(c.text)
          ind_rest['title'] = alink.text
          ind_rest['image_url'] = image_div['src']
          ind_rest['url'] = "https://www.yelp.com" + alink['href']
          if price_div:
              ind_rest['price'] = len(price_div.text)
          else:
              ind_rest['price'] = None
          ind_rest['stars'] = float(stars_div['aria-label'].split("star")[0])
          ind_rest['reviewCount'] = int(review_div.text)
          if phone_div and address_div:
            if phone_div.text != address_div.text:
              ind_rest['phone'] = phone_div.text
            else:
              ind_rest['phone'] = None
          else:
              ind_rest['phone'] = None
          if address_div:
            ind_rest['address'] = address_div.text
          else:
            ind_rest['address'] = None
          ind_rest['neighborhood'] = neighborhood_div.text
          ind_rest['cuisines'] = ", ".join(cuisines)
          print(ind_rest)
          li.append(ind_rest)
        print(li)
      return li

    def split_chunks(self, li, restaurants, n=5):
      for i in range(0, len(li), n):
        time.sleep(10)
        print('Start New List beginning with {}'.format(i))
        self.add_new_attributes(li[i:i + n], restaurants)
        break
    
    def add_new_attributes(self, li, restaurants):
      new_att = ['city', 'state', 'zipcode', 'health_score', 'ambience', 
              'reservations', 'take_out', 'apple_pay', 'bike_parking',
              'happy_hour', 'wifi', 'dogs', 'drive_thru', 'vegan_options', 'delivery',
              'credit_cards', 'google_pay', 'parking', 'kids', 
              'outdoor_seating', 'tv', 'waiter_service', 'caters',
               'smoking', 'dancing', 'wheelchair', 'coat',
              'meal', 'groups', 'happy_hour_sp', 'noise_level', 
              'alcohol', 'parking']
      boolean_values = [{'reservations': 'Reservations',
                          'take_out': 'Take-out',
                          'wifi': 'Wi-Fi',
                          'apple_pay': 'Apple Pay',
                          'bike_parking': 'Bike Parking',
                          'happy_hour': 'Good For Happy Hour',
                          'dogs': 'Dogs Allowed',
                          'drive_thru': 'Drive-Thru',
                          'vegan_options': 'Vegan',
                          'delivery': 'Delivery',
                          'credit_cards': 'Credit Cards',
                          'google_pay': 'Google Pay',
                          'tv': 'TV',
                          'waiter_service': 'Waiter',
                          'caters': 'Caters', 
                          'smoking': 'Smoking',
                          'dancing': 'Dancing',
                          'wheelchair': 'Wheelchair',
                          'coat': 'Coat',
                          'groups': 'Good for Groups',
                          'outdoor_seating': 'Outdoor Seating',
                          'happy_hour_sp': 'Happy Hour Specials' }]
      for idx, item in enumerate(li):
        print('Insert {} item'.format(idx))
        for att in new_att:
            item[att] = None
        time.sleep(8)
        rps = RestaurantPageSetup(item['url'])
        rps.setup_driver()
        rps.driver.set_window_position(0,-1000)
        location = rps.driver.find_elements_by_tag_name('address')[-1].find_elements_by_tag_name('p')[-1].text
        if location:
          item['city'] = location.split(",")[0]
          item['state'] = location.split(", ")[1].split(" ")[0]
          item['zipcode'] = location.split(", ")[1].split(" ")[-1]
        business_div = rps.driver.find_elements_by_xpath("//a[contains(text(),'Read more')]")
        attribute_button = rps.driver.find_elements_by_xpath("//p[contains(text(),'Attributes')]")
        if attribute_button:
          attribute_button[0].click()
        
          ambience_div = rps.driver.find_elements_by_xpath("//span[contains(text(),'Ambience')]")
          health_div = rps.driver.find_elements_by_xpath("//a[contains(text(),'Health Score')]")
          meal_div = rps.driver.find_elements_by_xpath("//span[contains(text(),'Good For')]")
          parking_div = rps.driver.find_elements_by_xpath("//span[(contains(text(),'Parking')) and (not(contains(text(), 'Bike')))]")
          noise = rps.driver.find_elements_by_xpath("//span[contains(text(),'Noise Level')]")
          alcohol = rps.driver.find_elements_by_xpath("//span[contains(text(),'Alcohol')]")
          
         
          if ambience_div and ambience_div[0].find_elements_by_xpath("./following-sibling::span"):
              item['ambience'] = ambience_div[0].find_element_by_xpath("./following-sibling::span").text.strip()
          if meal_div and meal_div[0].find_elements_by_xpath("./following-sibling::span"):
              item['meal'] = meal_div[0].find_element_by_xpath("./following-sibling::span").text.strip()
          if health_div and health_div[0].find_elements_by_xpath("../following-sibling::span"):
              item['health_score'] = int(health_div[0].find_element_by_xpath("../following-sibling::span").text.split("out of")[0])
          if noise and noise[0].find_elements_by_xpath("./following-sibling::span"):
              item['noise_level'] = noise[0].find_element_by_xpath("./following-sibling::span").text.strip()
          if alcohol and alcohol[0].find_elements_by_xpath("./following-sibling::span"):
              item['alcohol'] = alcohol[0].find_element_by_xpath("./following-sibling::span").text.strip()
          if parking_div and parking_div[0].find_elements_by_xpath("./following-sibling::span"):
              item['parking'] = parking_div[0].find_element_by_xpath("./following-sibling::span").text.strip()
              
          for value in boolean_values:
              for k, v in value.items():
                  bdiv = rps.driver.find_elements_by_xpath("//span[contains(text(),'" + v + "')]")
                  if bdiv and bdiv[0].find_elements_by_xpath("./following-sibling::span"):
                      item[k] = self.convert_yes_no_to_boolean(bdiv[0].find_element_by_xpath("./following-sibling::span").text.strip())
        item['description'] = ''
        if business_div:
            business_div[0].click()
            specialties_div = rps.driver.find_elements_by_xpath("//h4[contains(text(), 'Specialties')]")
            if specialties_div and specialties_div[0].find_elements_by_xpath("../following-sibling::p"):
                content_div = specialties_div[0].find_elements_by_xpath("../following-sibling::p")
                item['description'] = content_div[0].text
        print("Inserting...")
        restaurants.insert_one(item)

    def create_mongodb(self):
      client = MongoClient('localhost', 27017)
      yelp = client['yelp']
      restaurants = yelp['restaurants']

      return restaurants

    def convert_yes_no_to_boolean(self, string):
      if string == 'Yes':
        return 1
      else:
        return 0
