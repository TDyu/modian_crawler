# http://www.cnblogs.com/rwxwsblog/p/4578764.html
# https://www.bbsmax.com/A/ZOJPZ4rPdv/

from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerRunner
from scrapy.utils.conf import arglist_to_dict
 
class Command(ScrapyCommand):
 
    requires_project = True
 
    def syntax(self):
        return '[options]'  
 
    def short_desc(self):
        return 'Runs all of the spiders'  
 
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
 
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
 
    def run(self, args, opts):
        #settings = get_project_settings()
 
        spider_loader = self.crawler_process.spider_loader
        for spidername in args or spider_loader.list(): # 主要是用了self.crawler_process.spider_loader.list()方法获取项目下所有的spider
            print("*********cralall spidername************" + spidername) # 教程裡面都是python2 所以這個原本是沒有括號 於是你就被坑了半天了 其實只是沒編譯過關
            self.crawler_process.crawl(spidername, **opts.spargs) # 然后利用self.crawler_process.crawl运行spider
 
        self.crawler_process.start()