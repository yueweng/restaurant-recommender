import numpy as numpy
import pandas as pd
import time
import copy
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

class RestaurantPageSetup():
  def __init__(self, url):
        self.url = url
        self.path = r'/Users/yuewengmak/Desktop/chromedriver'
        self.driver = webdriver.Chrome(executable_path = self.path)

  def setup_driver(self):

    self.driver.implicitly_wait(30)
    self.driver.get(self.url)