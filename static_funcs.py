import time

def get_time():
    return str(time.time())

def file_reader(filename, mode='r'):
    content = ''
    fopen = open(filename, mode)
    try:
        content = [line.rstrip('\n') for line in fopen if len(line) > 2]
    finally:
        fopen.close()
    return content

def file_write(filename, new_content):
	fopen = open(filename, 'w')
	try:
		fopen.write(new_content)
	finally:
		fopen.close()

def text_spitter(key):
    val = ''
    if key == 'master_head':
        val = '''FileMe \n
                    copyright -- Darnell Lynch
              '''
    return val

def rewrite_file(filename, lines, (s,t)):
	start, thres = (s,t)
	cur_file = file_reader(filename)
	for i in range(thres):
		cur_file[start+i] = lines[i]
	rebuild = rebuild_lines(cur_file)
	file_write(filename, rebuild)	

def dic_to_lines(dic):
	ls = []
	for a,b in dic.iteritems():
		ls.append(a + ':' + b)
	return ls

def rebuild_lines(linelist):
	newlist = ''
	for br in range(len(linelist)):
		newlist += linelist[br]+ '\n'
	return newlist