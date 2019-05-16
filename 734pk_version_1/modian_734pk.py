#!/user/bin/env python3
# coding=utf-8
# -*- coding: utf -*-
# 
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import string
import datetime

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# URL
URL_KXY = 'https://wds.modian.com/show_weidashang_pro/5228'
URL_TAKO = 'https://wds.modian.com/show_weidashang_pro/5229'
URL_DM = 'https://wds.modian.com/show_weidashang_pro/5230'
URL_KIKI = 'https://wds.modian.com/show_weidashang_pro/5225'
URL = (URL_KXY, URL_TAKO, URL_DM, URL_KIKI)

# NAME
NAME = ("    消音     ", "    TAKO     ", "    戴萌     ", "    Kiki     ")

# Send Message
MESSAGE_TITLE = "排名   姓名     金額           人數"

def get_web_page(url):
	''' 
	get the data of the web
	'''
	time.sleep(0.5) # delay to avoid being kill
	# get_more_data(url, MORE_TIMES, MORE_SLEEP_TIME)
	
	# return WEB_DRIVER.page_source
	response = requests.get(url)
	if response.status_code != 200:
		print('Invalid url:', response.url)
		return None
	else:
		return response.text # string

def get_info_key(text, pre_div, next_div, skip=0):
	''' 
	get the info key
	'''
	start_index = text.find(pre_div)
	return text[start_index + skip : text.find(next_div, start_index)]

def get_key(response):
	''' 
	get the key
	'''
	# get the all soup
	soup = BeautifulSoup(response, 'lxml')

	# get current total money
	total_money = get_info_key(str(soup.find('div', 'mon current')), '/em>', '<', 4)
	# get current total people
	current_people = get_info_key(str(soup.find('div', 'b')), 'n>', '<', 2)
	return total_money, current_people

def info_update(PK_member):
	BG_money = 0
	DT_money = 0
	for i in range(0, 4):
		PK_member[i].name = NAME[i]
		current_page = get_web_page(URL[i])
		info_key = get_key(current_page)
		total_money = info_key[0]
		money = ''.join(re.split(',', total_money))
		money = float(money)
		if i == 0 or i == 1:
			BG_money += money
		else:
			DT_money += money
		current_people = info_key[1]
		PK_member[i].update_money_people(total_money, current_people)

	PK_member.sort(key=rank_key, reverse = True)

	print(MESSAGE_TITLE)
	for i in range(0, 4):
		print(" %d%s" % (i + 1, PK_member[i].print_info()))

	print("\nB格 :" + str("%.2f" % BG_money))
	print("呆駝:" + str("%.2f" % DT_money))
	print("差距:" + str("%.2f" % (BG_money - DT_money)))
	print("===================================")

def rank_key(x):
	money = ''.join(re.split('\.|,', x.money))
	return int(money)

class PK:
	def __init__(self, name, money=0, people=0):
		self.name = name
		self.money = int(money)
		self.people = int(people)

	def print_info(self):
		return self.name + str(self.money) + "       " + str(self.people)

	def update_money_people(self, money, people):
		self.money = money
		self.people = people

PK_member = [PK(NAME[0]), PK(NAME[1]), PK(NAME[2]), PK(NAME[3])]

if __name__ == '__main__':
	while True:
		now_time = datetime.datetime.now()
		print("%s/%s/%s  %s:%s:%s" % (now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute, now_time.second))
		info_update(PK_member)
		cin = input("Update? (Y/N)")
		if cin == 'Y' or cin == 'y':
			print("---update---")
			continue
		elif cin == 'N' or cin == 'n':
			break
		else:
			print("Error")
			break
	
	print("===END===")