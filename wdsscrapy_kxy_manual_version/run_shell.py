#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
# set setting file at first
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'wdsscrapy_kxy.settings')
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

def run_with_log():
	''' Run spider with logger '''
	configure_logging()
	runner = CrawlerRunner(get_project_settings())
	runner.crawl("wds_kxy_spider")
	d = runner.join()
	d.addBoth(lambda _: reactor.stop())
	reactor.run() # the script will block here until all crawling jobs are finished

def run_without_log():
	''' Run spider without logger '''
	# configure_logging()
	runner = CrawlerRunner(get_project_settings())
	runner.crawl("wds_kxy_spider")
	d = runner.join()
	d.addBoth(lambda _: reactor.stop())
	reactor.run() # the script will block here until all crawling jobs are finished

runner = CrawlerRunner(get_project_settings())
runner.crawl("wds_kxy_spider")
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()