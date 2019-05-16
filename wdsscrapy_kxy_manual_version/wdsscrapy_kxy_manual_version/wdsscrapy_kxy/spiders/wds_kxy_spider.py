'''follow the situation of wds
the current total amount
the number of current sposors
the remaining time
the first page of sponsors' name
the corresponding amount to the sponsors in first page
'''

# -*- coding: utf-8 -*-

import scrapy
from wdsscrapy_kxy.items import WdsscrapyKxyItem

class WdsKxySpiderSpider(scrapy.Spider):
    name = 'wds_kxy_spider'
    allowed_domains = ['wds.modian.com']
    start_urls = ['https://wds.modian.com/show_weidashang_pro/5346#1'] # SNH48-孔肖吟2017总选集资应援 终章（前篇）
    custom_settings = {
       "DEFAULT_REQUEST_HEADERS":{
             'authority':'wds.modian.com',
             'accept':'application/json',
             'accept-encoding':'gzip, deflate, br',
             'accept-language':'zh-TW,zh-HK;q=0.8,zh-MO;q=0.6,zh-CN;q=0.4,zh;q=0.2,en-US;q=0.2,en;q=0.2',
             'origin':'https://wds.modian.com',
             'referer':'https://wds.modian.com/show_weidashang_pro/5228',
             'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
             'x-requested-with':'XMLHttpRequest',
             'cookie':'cna=/oN/DGwUYmYCATFN+mKOnP/h; tracknick=adimtxg; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; thw=cn; v=0; cookie2=1b2b42f305311a91800c25231d60f65b; t=1d8c593caba8306c5833e5c8c2815f29; _tb_token_=7e6377338dee7; CNZZDATA30064598=cnzz_eid%3D1220334357-1464871305-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464871305; CNZZDATA30063600=cnzz_eid%3D1139262023-1464874171-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464874171; JSESSIONID=8D5A3266F7A73C643C652F9F2DE1CED8; uc1=cookie14=UoWxNejwFlzlcw%3D%3D; l=Ahoatr-5ycJM6M9x2/4hzZdp6so-pZzm; mt=ci%3D-1_0'
         },
         "ITEM_PIPELINES":{
             'wdsscrapy_kxy.pipelines.WdsscrapyKxyPipeline': 300 # http://hes.logdown.com/posts/256189-scrapy-study-notes-3-pipeline
         },
         'COMMANDS_MODULE':'wdsscrapy_kxy.commands'
     }

    def parse(self, response):
        item = WdsscrapyKxyItem()
        # info
        response_info =  response.css('.project-info .project-wrap')
        item['total_amount'] = response_info.css('.t span::text').extract()[1]
        item['total_people_number'] = response_info.css('.b span::text').extract_first()
        # info_time
        time_text = response_info.css('.right span em::text').extract_first()
        last_text = response_info.css('.right span::text').re('\S')[2:]
        # hour or day
        if len(last_text) == 2:
        	item['remaining_time'] = time_text + last_text[0] + last_text[1]
        else:
        	item['remaining_time'] = time_text + last_text[0]
        # comment
        item['current_sponsors'] = []
        item['current_sponsors_amount'] = []
        response_comment = response.css('.project-comment .list-comment ul li')
        for i in range(0, 5):
        	# sponsor name
        	sponsor_name = response_comment.css('.top .left span.nick::text').extract()[i]
        	item['current_sponsors'].append(sponsor_name)
        	# sponsor money
        	sponsor_money = response_comment.css('.comment span::text').extract()[i]
        	pre_text = sponsor_money[ : sponsor_money.find('了') + 1]
        	money_text = sponsor_money[sponsor_money.find('了') : sponsor_money.find('元') + 1]
        	sponsor_money = '刚刚' + pre_text + '小孔' + money_text
        	item['current_sponsors_amount'].append(sponsor_money)
        yield item
