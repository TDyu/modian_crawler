from setuptools import setup, find_packages
 
setup(name='scrapy-mymodule',
  entry_points={
    'scrapy.commands': [
      'crawlall=wdsscrapy_kxy.commands:crawlall',
    ],
  },
 )