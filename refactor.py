import sys
import re

suite = ''
test = ''
tab = '    '
res = []
test_lines = []

def finish_test():
    global res
    if len(test_lines) <= 50:
        res += test_lines
        return
    try:
        pos = test_lines.index(tab + 'GRAPH(GetGraph())')
    except ValueError:
        res += test_lines
        print(test + ' failed')
        return
    assert test_lines[pos + 1] == tab + '{'
    end = test_lines.index(tab + '}')

    meth = 'BuildGraph' + test + '()'
    print(tab + 'void ' + meth + ';')
    
    res.append('void ' + suite + '::' + meth)
    res.append('{')
    res += test_lines[pos:end + 1]
    res.append('}')
    res.append('')
    res += test_lines[:pos] + [tab + meth + ';'] + test_lines[end + 1:]

with open(sys.argv[1], 'r') as f:
    ls = f.read().split('\n')
    testStart = 0
    for (i, l) in enumerate(ls):
        if l.startswith('TEST_F'):
            m = re.match('TEST_F\((.*), (.*)\)', l)
            suite = m.group(1)
            test = m.group(2)
            # print(test)
        if test == '':
            res.append(l)
        else:
            test_lines.append(l)

        if l.startswith('}') and test:
            finish_test()
            test = ''
            test_lines = []

with open('out.cpp', 'w') as out:
    out.write('\n'.join(res))
