from aita.customclass import *
from aita.generator import *
from aita.constants import *
import os
import random
import sys
import time
import click

DATA_PATH = os.path.join(SCRIPT_PATH,'data')
LANG = 'ko' # TODO: Lang selection

def print_welcome():
    print('-'*80)
    print("AI Text Adventure PROTOTYPE A")

def get_choice(choices, skip_newline = False):
    choice_num = 0
    while True:
        for i, choice in enumerate(choices):
            if i == choice_num:
                print(f" ⇨ {i+1}. {choice}", end='')
            else:
                print(f"   {i+1}. {choice}", end='')
            if not skip_newline:
                print('')
        rawinput = click.getchar()
        if rawinput == '\x0D':
            break
        if rawinput == '\x1b[B': # DOWN
            choice_num += 1
            if choice_num >= len(choices):
                choice_num = len(choices) - 1
        elif rawinput == '\x1b[A': # UP
            choice_num -= 1
            if choice_num < 0:
                choice_num = 0
        for _ in choices:
            sys.stdout.write(CURSOR_UP_ONE) 
            sys.stdout.write(ERASE_LINE) 
    return choices[choice_num]

def get_random_initial_prompt():
    plot = open(os.path.join(DATA_PATH,LANG,'plot')).read().split('\n')
    protagonist_explanation = open(os.path.join(DATA_PATH,LANG,'protagonist_explanation')).read().split('\n')
    protagonist_type = open(os.path.join(DATA_PATH,LANG,'protagonist_type')).read().split('\n')
    story_about = open(os.path.join(DATA_PATH,LANG,'story_about')).read().split('\n')
    story_begin = open(os.path.join(DATA_PATH,LANG,'story_begin')).read().split('\n')
    
    actor_string = f"이 이야기는 {random.choice(protagonist_explanation)}한 {random.choice(protagonist_type)}와 "
    actor_string += f"{random.choice(protagonist_explanation)}한 {random.choice(protagonist_type)}의 이야기이다.\n"
    story_start_string = f"{random.choice(story_about)}에 대해 {random.choice(plot)} {random.choice(story_begin)}(으)로 시작한다."

    return actor_string + story_start_string

def save():
    savefile = os.path.join(DATA_PATH,'savefile')
    with open(savefile,'w') as f:
        f.writelines(history)
    return

def load_save():
    savefile = os.path.join(DATA_PATH,'savefile')
    with open(savefile,'r') as f:
        history = f.readlines()
    return history

def run_adventure():
    # Initial config
    global history
    history = []
    if input("불러오려면 load를 입력해 주세요(건너뛰려면 Enter):") == 'load':
        history = load_save()
    else:
        supported_fantasy_types = ["영웅","역사","중세","소드 앤 소서리","코믹","서사시","다크","디스토피아","현실주의적"]
        
        print("원하는 판타지 종류를 선택해 주세요:")
        story_type = get_choice(supported_fantasy_types)

        print(story_type, '이야기를 시작합니다.')
        print('-'*80,'\n')

        init_prompt = get_random_initial_prompt()
        print(init_prompt)
        print("이제 당신은 이야기의 주인공이자 해설자, 진행자 입니다.")
        print("무슨 이야기가 이루어질지, 써내려 가면서 즐겨보세요.")
    
    print("※ 저장은 save를 입력하시면 됩니다. 프로그램 종료 시에도 저장됩니다.")

    # Loop
    while True:
        user_input = input('> ')
        if user_input == 'save':
            save()
            print('\n저장됨.\n')
            continue
        print("Placeholder for data generated from prompt", user_input)
        history.append(user_input)

def main(flags):
    print_welcome()
    try:
        run_adventure()
    except KeyboardInterrupt:
        print("\n저장 중...")
        save()
        sys.exit()