"""runner.py

Convenience stuff for running a scraper in a daemon-ish mode
"""

from bmr_statbot.scraper import BMRScraper
from bmr_statbot import config

from time import sleep

from requests.exceptions import RequestException

scraper = None

def run_scraper(post=True, logger=None):
    scraper = BMRScraper(post)
    
    while True:
        try:
            scraper.scrape_posts_up(post)
        except RequestException as e:
            if logger is not None:
                logger.error('HTTP problem while scraping: {0}'.format(e))
            else:
                raise 
            
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
       
    run_scraper(True, logger)
