import logging

from app import *

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')
logger = logging.getLogger('scraping')

# Base values based on which program will scrape data
# img: Scrape images from answers?
# json: Write questions and answers to JSON?
# text:
CONFIG = {'askfm_nick': None, 'dl_img':True, 'to_json':False, 'to_csv':False}

MENU_INPUT = ''
INPUT_NICK = "Input user's nick: "

def change_setting(choice):
    if choice == 'askfm_nick':
        CONFIG[choice] = input(INPUT_NICK)
    else:
        CONFIG[choice] = not CONFIG[choice]
    render_info()


def render_info():
    global MENU_INPUT

    MENU_INPUT = f'''
askfm_nick - Change Nick (Now: {str(CONFIG['askfm_nick'])} )
dl_img - Save all IMGs (Now: {str(CONFIG['dl_img'])} )
to_json - Save to JSON (Now: {str(CONFIG['to_json'])} )
to_csv - Save to TEXT (Now: {str(CONFIG['to_csv'])} )

START - start
q - quit.
Your input?
'''

def menu():
    # Get user's input
    # If chocie is 'q' or 'quit' - quit
    CHOICE = input(MENU_INPUT)
    while CHOICE != 'q' or CHOICE != 'quit' :
        if CHOICE in CONFIG.keys():

            change_setting(CHOICE)
            print(CONFIG)

        # Pass config values as unpacked dict
        elif CHOICE == "start":
            retrieve(**CONFIG)
            break
        else:
            print('Invalid command.')

        CHOICE = input(MENU_INPUT)


print('Ask.fm scrapper')

CONFIG['askfm_nick'] = input(INPUT_NICK)
logger.info('User inputs Ask.fm nick: ' + CONFIG['askfm_nick'])

render_info()

logger.info('Running menu.')
menu()
logger.info('Terminating software.')
