# Basic imports
import os
import time
import json
import logging

# Modules imports
import requests
from bs4 import BeautifulSoup

# Imports from files
from answer import SinglePost
from locators import *


logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')
logger = logging.getLogger('app')


ask_url = 'https://ask.fm' #Base Ask URL


BASE_DIR = os.getcwd()

# List with pending profile links to scrape.
# First link is simply base URL: ask.fm/profile.
# After first visit, if there is "next" button on page (next page)
# Then this link is appended to this array and program continues scraping
_pending_list = []

# Array for each Singlequestion_obj object.
# Singlequestion_obj object contains every answer encapsulated within one question_obj
# With info about question, answer etc.
_question = []

# Retrieving function.
# First loops through profile, and stops looping if there are no more "next" pages left
# If there are none, starts writing text content to drive by iterating through questions array
def retrieve(askfm_nick, dl_img, to_csv, to_json):
    logger.info('Running "retrieve" function.')
    _n = 1
    # Append base Askfm profile link to pending list to be scraped first
    _pending_list.append(ask_url + '/' + askfm_nick)

    # scraping bêdzie trwa³ tak d³ugo, jak istnieje chocia¿ 1 link w liœcie "_pending_list".
    # len = 0 oznacza, ¿e nie ma wiêcej linków



    # Trial of creating folder for downloaded content with user's nickname as name
    try:
        logger.info('Trial of creation of directory for scraping: '+ BASE_DIR)
        os.mkdir(askfm_nick)
    except Exception:
        logger.info('FAIL of creation of directory for scraping: ' + BASE_DIR)
        print('Directory already exists or another error happened. Skipping...')
        pass

    # Loop runs as long as there is some page to scrape.
    # If there was no "next" page, loop ends
    while len(_pending_list) > 0:
        for link in _pending_list:

            print(f'Connecting : {link}')
            logger.info('Establishing connection to: ' + link)

            # Get content of page, parse it with BS4
            try:
                site = requests.get(link).content
                soup = BeautifulSoup(site, 'html.parser')

                # Select each indivifual question on profile
                all_questions = soup.select(SiteLocators.QUESTIONS)
            except Exception:
                print(f'Connection error at: {link}. Retrial in 5 seconds...')
                # logger.info(f'Connection error at: {link}. Retrial in 5 seconds...')
                time.sleep(5)
                continue

            # From array of questions we crate actual objects which will contain
            # Only important data (like question, answer in text etc.)
            # WHich we will perform operations on later
            for question in all_questions:
                question_obj = SinglePost(question)
                _question.append(question_obj)

                logger.info(f'Adding question #{_n}.')

                # If given question had image, we access it and download it
                if question_obj.image:
                    save_one_image(askfm_nick, question_obj)

                _n += 1

            # Remove already scraped profile from pedning list
            _pending_list.remove(link)
            print(f'{link} removed from temp...')
            logger.info(f'{link} removed from temp.')

            # If there is next page, we again start looping
            next_page = soup.select_one(SiteLocators.NEXT)
            logger.info('Retrieving next page link')
            print('Retrieving next page link')

            if next_page:
                _pending_list.append(ask_url + next_page.attrs['href'])
                logger.info(f"Link to next site appended to temp list: {ask_url}{next_page.attrs['href']}")
                print(f"{ask_url}{next_page.attrs['href']} appending successful! Looping back...")
            else:
                logger.info(f'No "Next" link found. Retrieving done.')
                print('No "Next" link found. Retrieving done.')
                perform_file_operations(askfm_nick, dl_img, to_csv, to_json)


# Function dispatching file operations
def perform_file_operations(askfm_nick, dl_img, to_csv, to_json):
    for each in _question:
        if to_csv:
            save_to_csv(askfm_nick)
        if to_json:
            save_to_json(askfm_nick)


def save_to_json(askfm_nick):
    logger.info('Running "save_to_json" function.')
    print('Saving to JSON')

    _list = []
    file_name = f'{askfm_nick}.json'
    with open(os.path.join(BASE_DIR, askfm_nick,file_name), 'w') as file:
        for each in _question:

            json_dict = {
            'question': each.question,
            'answer': each.answer,
            'likes': each.likes,
            'time': each.date,
            'link': each.link,
            'img': f"{askfm_nick}-{each.link.split('/')[-1]}.{each.image_extension}" if each.image else None,
            'asker_url': each.asker
            }

            _list.append(json_dict)

            # if each.image:
            #     save_images(each.image_link, each.image_extension, each.link)

        json.dump(_list, file, indent=4, ensure_ascii=True)
        print(f'Saved to JSON: {file_name}')

def save_to_csv(askfm_nick):
    logger.info('Running "save_to_csv" function.')
    pass


def save_images(askfm_nick):
    logger.info('Running "save_images" function.')
    for each in _question:
        if each.image:

            print('Saving image....')

            _photo_name = f"{askfm_nick}-{each.link.split('/')[-1]}.{each.image_extension}"
            try:
                logger.info('Trial of saving image begins.')
                logger.info('Requesting image from: ' + each.image_link)
                photo_file = requests.get(each.image_link).content

                img_path = os.path.join(BASE_DIR, askfm_nick, _photo_name)

                with open(img_path, 'wb') as f:
                    f.write(photo_file)
                    logger.info('Saving image to: ' + img_path)
                    print(f"Image saved: {_photo_name}")

            except Exception:
                print(f"Could not get image {_photo_name}. Skipping...")
                logger.info('Error with saving image: ' + _photo_name)
                pass


def save_one_image(askfm_nick, question_obj):
    logger.info('Running "save_one_image" function.')
    print('Saving image....')

    _photo_name = f"{askfm_nick}-{question_obj.link.split('/')[-1]}.{question_obj.image_extension}"
    try:
        logger.info('Trial of saving image begins.')
        logger.info('Requesting image from: ' + question_obj.image_link)
        photo_file = requests.get(question_obj.image_link).content

        img_path = os.path.join(BASE_DIR, askfm_nick,_photo_name)

        with open(img_path, 'wb') as f:
            f.write(photo_file)
            logger.info('Saving image to: ' + img_path)
            print(f"Image saved: {_photo_name}")

    except Exception:
        print(f"Could not get image {_photo_name}. Skipping...")
        logger.info('Error with saving image: ' + _photo_name)
        pass

