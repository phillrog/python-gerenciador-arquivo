import time
import os
import os.path
import select
import re
import difflib
from itertools import zip_longest
import __main__


print("Working path:", os.getcwd())


def color(text, which):
    if which == 'test':     
        for i in range(1,100):
            print('\\033['+str(i)+'m' , '\033['+str(i)+'m' + 'xxxxx' + '\033[0m' )
        return

    options = {
       'red'        : '\033[31m',
       'green'      : '\033[32m',
       'yellow'     : '\033[93m',
       'blue'       : '\033[34m',
       'purple'     : '\033[95m',
       'cyan'       : '\033[96m',
       'darkcyan'   : '\033[36m',
       'bold'       : '\033[1m',
       'underline'  : '\033[4m',
       'END'        : '\033[0m',
    }
    return options[which] + text + options['END']


def color_print(c, *args):
    print(*[color(arg, c) for arg in args])


def print_diffs(name, new_name):
   
    d = difflib.Differ()
    result = list(d.compare([name], [new_name]))

    changes = [[name, ''], [new_name, '']]
    curr = -1

    for line in result:
        if curr == -1:
            curr += 1
            changes[curr][0] = line     # salva texto
        elif curr > -1:
            if line[0] in ['+', '-', ' ']:
                curr += 1
                changes[curr][0] = line     # salva texto
            else:
                changes[curr][1] = line          # salva mudança

    for i, change in enumerate(changes):
        ret = []
        for c, dif in zip_longest(change[0][2:], change[1][2:]):
            if c is None:
                c = ''
            if dif == '+' or [dif, i] == ['^', 1]:
                c = color(c, 'green')
            elif dif == '-' or [dif, i] == ['^', 0]:
                c = color(c, 'red')
            ret.append(c)
        print(''.join(ret))
    print()



def print_names():
    print('Files:')
    for file_name in os.listdir(__main__.filesPath):
        if file_name == os.path.basename(__main__.__file__):  # pula arquivo
            continue
        print(file_name)
    print()

def execute_dentro(func, *args):
    __main__.fileFound = 0
    __main__.ord = 0
   

    color_print('yellow', '*** Running', func.__name__, *args if args else '')
    print()
    process_check(print_diffs, func, *args)        
    if __main__.fileFound == 0:
        color_print('green', '*** Todos arquivos estão válidos ***' )
    else:
        print()
        color_print('yellow', '*** Total Arquivos => ', str(__main__.fileFound))
    print()
    input()

def process_check(new_name_handler, func, *args):
   
    working_dir = (__main__.filesPath)
    no_changes = True
    for file_name in os.listdir(working_dir):
            
        new_name = func(file_name, *args)

        if len(new_name) < 5:         
            no_changes = False
            continue

        color_print('red', new_name)

        __main__.fileFound += 1
    return no_changes
