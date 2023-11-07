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
            changes[curr][0] = line     
        elif curr > -1:
            if line[0] in ['+', '-', ' ']:
                curr += 1
                changes[curr][0] = line     
            else:
                changes[curr][1] = line          

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


def test_print_diffs():
    def test(name, a, b):
        color_print('yellow', name, '\n ', a, '\n ', b)
        print_diffs(a, b)

    print(color('testing print_diffs', 'purple'))

    test('equal (we never use this)',
         'hello there',
         'hello there')
    test('remove',
         'hello there@',
         'hello there')
    test('add',
         'hello there',
         '@hello there')
    test('change',
         'hello there@',
         'hello@@here ')
    test('remove and add',
         'hello there@',
         '@hello there')
    test('remove, add and change',
         'hello there@',
         '@hello@there')


def process_files(new_name_handler, func, *args):
    __main__.fileFound = 0
    __main__.ord = 0
    
    working_dir = (__main__.filesPath)
    no_changes = True
    for file_name in os.listdir(working_dir):
    
        
        name, ext = os.path.splitext(file_name) if not os.path.isdir(file_name) else (file_name, '')
        if file_name == os.path.basename(__main__.__file__):  
            continue
        new_name = func(name, *args)

        if name != new_name:
            new_name_handler(os.path.join(working_dir,file_name), os.path.join(working_dir,new_name+ext))
            no_changes = False
    return no_changes


def execute_no_nome(func, *args):    
    color_print('yellow', '*** Running', func.__name__, *args if args else '')
    no_changes = process_files(print_diffs, func, *args)        
    
    if no_changes:
        color_print('blue', 'Nenhuma mudança ocorreu')
        return 

    color_print('purple', 'Confirma as mudanças ? (y)')
    if input() != 'y':
        color_print('blue', 'Nenhuma mudança confirmada')
    else:        
        process_files(os.rename, func, *args)
        color_print('green', 'Alterado com sucesso')
    print()
    input()


def print_names():
    print('Files:')
    for file_name in os.listdir(__main__.filesPath):
        if file_name == os.path.basename(__main__.__file__):  
            continue
        print(file_name)
    print()

# print_names()