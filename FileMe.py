import sys
import os

from static_funcs import *


right_now = get_time()
program_dir = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
gstart, gthres = (0,0)

def init_meta():
    #update things in meta

    meta = parse_block_return(parse_data_block('meta.txt', 'META'))
    meta['LAST_COMMAND_RUNTIME'] = right_now
    lines = dic_to_lines(meta)
    ck_ok = rewrite_file('meta.txt', lines, (gstart, gthres))
    

def parse_data_block(filename, block_name):
    if not filename or not block_name:
        return 'missing_values'
    
    filename = program_dir +'/'+ filename
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
    init_meta()
    meta = parse_block_return(parse_data_block('meta.txt', 'META'))
    #print meta['PROGRAM_NAME'] + '-' +meta['VERSION'] + ' **** Author: ' + meta['AUTHOR'] 
    #print ''
    print '-->Projects: '+ meta['PROJECT_COUNT']

def legal_switches(switches):
    legals = parse_block_return(parse_data_block('meta.txt', 'SWITCHES'))
    for i in range(len(switches)):
        if switches[i][1:] not in legals:
            return False
    return True

def get_options():
    dic = {}
    args = sys.argv[1:]
    len_args = len(args)
    dic['option_count'] = len_args  #first opt is cwd
    if dic['option_count']:
        
        passed_switches = {}

        for i in range(len_args):
            if args[i].startswith('-'):
                passed_switches[i] = args[i]

        # check which switches I have
        if passed_switches:
            if not legal_switches(passed_switches):
                return 'bad_switches'
            else:
                if process_switches():
                    print 'here'
                else:
                    pass
        else:
            pass
    else:
        req_return_meta()
    return dic

options = get_options()


