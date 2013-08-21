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
        scraper.scrape_posts_up(post)
        sleep(config.sleep_time)


if __name__ == '__main__':
    run_scraper(True)