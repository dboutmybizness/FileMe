import sys
import os

program_dir = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

def file_reader(filename, mode='r'):
    content = ''
    fopen = open(filename, mode)
    try:
        content = [line.rstrip('\n') for line in fopen if len(line) > 2]
    finally:
        fopen.close()
    return content


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
        return dic
    return 'no_meta'


def text_spitter(key):
    val = ''
    if key == 'master_head':
        val = '''FileMe \n
                    copyright -- Darnell Lynch
              '''
    return val

def req_return_meta():
    meta = parse_data_block('meta.txt', 'META')
    print meta['PROGRAM_NAME'] + '-' +meta['VERSION'] + ' **** Author: ' + meta['AUTHOR'] 
    print ''
    print '-->Projects: '+ meta['PROJECT_COUNT']

def legal_switches(switches):
    legals = parse_data_block('meta.txt', 'SWITCHES')
    for i in range(len(switches)):
        if switches[i][1:] not in legals:
            return False
    return True

def get_options():
    dic = {}
    dic['option_count'] = len(sys.argv) - 1  #first opt is cwd
    if dic['option_count']:
        args = sys.argv[1:]
        passed_switches = {}

        for i in range(len(args)):
            if args[i].startswith('-'):
                passed_switches[i] = args[i]

        # check which switches I have
        if passed_switches:
            if not legal_switches(passed_switches):
                return 'bad_switches'
            else:
                print 'im right here arent i'
        else:
            pass
    else:
        req_return_meta()
    return dic

options = get_options()
print options

