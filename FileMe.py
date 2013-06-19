import sys
import os

def file_reader(filename, mode='r'):
    content = ''
    fopen = open(filename, mode)
    try:
        content = [line.rstrip('\n') for line in fopen if len(line) > 2]
    finally:
        fopen.close()
    return content

def parse_meta():
    return parse_data_block('meta.txt', 'META')


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
        return dic
    return 'no_meta'


def text_spitter(key):
    val = ''
    if key == 'master_head':
        val = '''FileMe \n
                    copyright -- Darnell Lynch
              '''
    return val

def get_options():
    dic = {}
    dic['cwd'] = os.getcwd()
    dic['pwd'] = sys.argv[0]

    args = sys.argv[1:]
    
    
    return dic

options = get_options()
print options
