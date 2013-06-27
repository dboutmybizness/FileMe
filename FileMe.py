import sys
import os
import re
from static_funcs import *


right_now = get_time()
program_dir = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
gstart, gthres = (0,0)
gmeta = {}


def count_projects():
    data = file_reader('projects.txt')
    c = 0
    if data:
        for i in range(len(data)):
            if re.search('##\w+##', data[i]):
                c += 1
    return str(c)

def init_meta():
    global gmeta
    #update things in meta
    meta = parse_block_return(parse_data_block('meta.txt', 'META'))
    meta['LAST_COMMAND_RUNTIME'] = right_now
    meta['PROJECT_COUNT'] = count_projects()
    lines = dic_to_lines(meta)
    ck_ok = rewrite_file('meta.txt', lines, (gstart, gthres))
    gmeta = meta

def parse_data_block(filename, block_name):
    if not filename or not block_name:
        return 'missing_values'
    
    gfile = file_reader(filename)
    if len(gfile) < 0:
        return 'no_file'

    data = gfile
    start = 0
    finish = 0;
    data_length = len(data)
    block_head = '##'+block_name+'##'
    dic = {}
    for i in range(data_length):
        if start and finish:
            continue
        if start and data[i] == block_head:
            finish = i
            continue
        if data[i] == block_head:
            start = i+1

    if start:
        thres = finish - start
        for i in range(thres):
            str = data[start+i]
            key,val = str.split(':')
            dic[key] = val
        dic['start'] = start
        dic['thres'] = thres
        return dic
    return 'no_meta'

def parse_block_return(dic):
    global gstart, gthres
    gstart = dic['start']
    gthres = dic['thres']
    dic.pop('start', None)
    dic.pop('thres', None)
    return dic


def req_return_meta():
    return 'Projects: '+ gmeta['PROJECT_COUNT']

def process_args(args):
    for i in range(len(args)):
        if args[i].startswith('-'):
            args[i] = args[i][1:]

    success = 0
    data = 'BAD_ARGS'
    a = args[0]
    if len(args) == 1:
        info = ['i','info']
        active = ['a','active']

        if a in info:
            data = 'NO_ARGS'
        elif a in active:
            success = 1
            data = 'SHOW_ACTIVE'
        else:
            pass
    elif len(args) == 2:
        b = args[1]
        creator = ['init']
        if a in creator:
            print 'here'
    return (success,data)

def get_options():
    dic = {}
    args = sys.argv[1:]
    len_args = len(args)

    #if no options print info screen
    if not len_args:
        return (0,'NO_ARGS')
    
    if len_args >=  1:
        if args[0].startswith('-'):
            return process_args(args)
    return (0,'BAD_ARGS')


def do_print(data):
    if data == 'NO_ARGS':
        mess = req_return_meta()
    elif data == 'BAD_ARGS':
        mess = ['FileMe ERRor: invalid arguments','try -h for help']
    return mess 

def line_printer(l):
    lines = []
    if isinstance(l, str):
        print '> %s' % (l)
    elif isinstance(l, (list)):
        for s in l:
            print '> %s' % (s)
    

def _generate(data):
    if data == 'SHOW_ACTIVE':
        if not gmeta['ACTIVE_PROJECT']:
            return 'no active projects, get to work'
        return gmeta['ACTIVE_PROJECT']

def main():
    init_meta()
    success,data = get_options()
    if not success:
        for_screen =  do_print(data)
    else:
        for_screen = _generate(data)
    return line_printer(for_screen)

if __name__ == '__main__':
    main()
else:
    print 'ERroR'
