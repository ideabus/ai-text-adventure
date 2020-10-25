from aita.customclass import *
from aita.generator import *
import os
import random
import sys
import time

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH,'..','data')
LANG = 'ko' # TODO: Lang selection

def print_welcome():
    print('-'*80)
    print("AI Text Adventure PROTOTYPE A")

def get_random_initial_prompt():
    plot = open(os.path.join(DATA_PATH,LANG,'plot')).readlines()
    protagonist_explanation = open(os.path.join(DATA_PATH,LANG,'protagonist_explanation')).readlines()
    protagonist_type = open(os.path.join(DATA_PATH,LANG,'protagonist_type')).readlines()
    story_about = open(os.path.join(DATA_PATH,LANG,'story_about')).readlines()
    story_begin = open(os.path.join(DATA_PATH,LANG,'story_begin')).readlines()
    
    plot = random.choice(plot)
    protagonist_explanation = random.choices(protagonist_explanation,k=2)
    protagonist_type = random.choices(protagonist_type,k=2)
    story_about = random.choice(story_about)
    story_begin = random.choice(story_begin)
    
    actor_string = f"이 이야기는 {protagonist_explanation[0]}한 {protagonist_type[0]}와 {protagonist_explanation[1]}한 {protagonist_type[1]}의 이야기이다."
    story_start_string = f"{story_about}에 대해 {plot}하며 {story_begin}(으)로 시작한다."

    return str(actor_string + story_start_string)

def run_adventure():
    # Initial config
    print("1) 수동으로 새 게임 만들기\n2) 자동으로 새 게임 만들기\n3) 불러오기")
    
    supported_fantasy_types = ["영웅","역사","중세","소드 앤 소서리","코믹","서사시","다크","디스토피아","현실주의적"]
    
    print("")
    
    # Loop
    '''
    while True:
        time.sleep(1)
    '''

def main():
    print_welcome()
    try:
        run_adventure()
    except KeyboardInterrupt:
        print("\nBye.")
        sys.exit()
    
main()