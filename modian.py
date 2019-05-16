#!/user/bin/env python3
# coding=utf-8
# -*- coding: utf -*-
# 
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# URL
URL_KXY_6 = 'https://wds.modian.com/show_weidashang_pro/4319'
URL_FXD_6 = 'https://wds.modian.com/show_weidashang_pro/4835'
URL = URL_KXY_6

# File name
BACKUP = "backup.txt"
CURRENT = "current.txt"

# Get more
CHROME_PATH = r'D:/Programming/Python/3.6/Learn/crawler/Project/modian/chromedriver.exe'
WEB_DRIVER = webdriver.Chrome(CHROME_PATH)
MORE_TIMES = 8
MORE_SLEEP_TIME = 0

# Send Message
SPONSOR_MESSAGE_FORMAT = "%s刚刚支持了小孔%s元，"
INFO_MESSAGE_FORMAT = "感谢大家对小孔的支持！\nSNH48-孔肖吟2017总选集资应援 第三乐章正在进行中，目前总额%s元，参加人数%s，距离本次活动结束还有%s天。\n1. 在任意集资渠道累计集资满500元，可获赠2017版孔肖吟应援毛巾；\n2. 在任意集资渠道累计集资满800元，可获得夏季应援T恤2017复刻版订购权；\n3. 在任意集资渠道累计集资满1200元，可加入2017集资应援群，并将以单页形势记录于2017年总选纪念册中（自己投票满40票，并把晒票码发给应援会管理确认也可享受此福利）\n微打赏链接：https://wds.modian.com/show_weidashang_pro/4319#1"

def file_write(filename, text):
	''' 
	write file
	'''
	f = open(filename, 'w', encoding='utf-8')
	f.write(text)
	f.close()

def get_more_data(url, times, sleep_time):
	''' 
	get more data by webdriver
	'''
	WEB_DRIVER.get(url)
	for i in range(times):
		# duplicately scroll
		WEB_DRIVER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		time.sleep(sleep_time)

def get_web_page(url):
	''' 
	get the data of the web
	'''
	time.sleep(0.5) # delay to avoid being kill
	get_more_data(url, MORE_TIMES, MORE_SLEEP_TIME)
	
	return WEB_DRIVER.page_source
	
	#if response.status_code != 200:
	#	print('Invalid url:', response.url)
	#	return None
	#else:
	#	return response.text # string


def get_info_key(text, pre_div, next_div, skip=0):
	''' 
	get the info key
	'''
	start_index = text.find(pre_div)
	return text[start_index + skip : text.find(next_div, start_index)]

def get_comment_key(soup_text):
	''' 
	get current comments
	'''
	soup = BeautifulSoup(soup_text, 'lxml')
	nicks_text = soup.find_all('span', 'nick')
	nick_sups_text = soup.find_all('span', 'nick_sup')
	# get current all sponsors {nick, money}
	sponsors = {}
	for nick, money in zip(nicks_text, nick_sups_text):
		start_index = money.string.find('了')
		money = money.string[start_index + 1 : money.string.find('元')]
		sponsors[nick.string] = money
	# backup
	file_write(BACKUP, str(sponsors))
	return sponsors

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
	# get date for end
	end_date = get_info_key(str(soup.find('div', 'right')), 'm>', '<', 2)
	# get current comment
	current_comment = get_comment_key(str(soup.find('ul', id='show_comment_list')))
	# file_write(BACKUP, current_comment)
	return total_money, current_people, end_date, current_comment
'''
def compara_comments(pre_comment, current_comment):
	
	compare pre_comment and current_comment
	
	# check pre_comment
    if pre_comment == None:
    	file = open(BACKUP, 'r')
    	if file != None:
    		pre_comment = eval(file.read())
    		file.close()
    	else:
    		return None

    # compare
'''    

if __name__ == "__main__":
    current_page = get_web_page(URL)
    if current_page != None:
    	info_key = get_key(current_page)
    	total_money = info_key[0]
    	current_people = info_key[1]
    	end_date = info_key[2]
    	pre_comment = None
    	print(pre_comment)
    	current_comment = info_key[3]
    	print(INFO_MESSAGE_FORMAT % (total_money, current_people, end_date))
    	pre_comment = current_comment
    	WEB_DRIVER.close()