"""runner.py

Convenience stuff for running a scraper in a daemon-ish mode
"""

from bmr_statbot.scraper import BMRScraper
from bmr_statbot import config

from time import sleep


scraper = None

def run_scraper(post=True):
    scraper = BMRScraper(post)
    
    while True:
        scraper.scrape_posts_up(post, reply=False)
        sleep(config.sleep_time)


if __name__ == '__main__':
    import logging
    
    logger = logging.getLogger('bmrstatbot')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('bmrstatbot.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s : %(message)s') 
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.info('Starting bmr_statbot...')
       
    run_scraper(True)
