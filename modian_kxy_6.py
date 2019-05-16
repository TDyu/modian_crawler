#!/user/bin/env python3
# coding=utf-8
# -*- coding: utf -*-
# 
import requests
import time
from bs4 import BeautifulSoup

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = 'https://wds.modian.com/show_weidashang_pro/4319#1'

def get_web_page(url):
	# get the data of the web
	time.sleep(0.5) # delay to avoid being kill
	
	response = requests.get(url)
	if response.status_code != 200:
		print('Invalid url:', response.url)
		return None
	else:
		return response.text

current_page = get_web_page(URL)
print(current_page)