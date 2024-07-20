import sys
import re

suite = ''
test = ''
tab = '    '
res = []
test_lines = []

def cut_graph(pref, substr):
    global res

    try:
        pos = test_lines.index(tab + f"GRAPH({substr})")
    except ValueError:
        raise ValueError(test + ' failed')
    assert test_lines[pos + 1] == tab + '{'
    end = test_lines.index(tab + '}', pos)
    meth = pref.upper() + f'({test}, Graph *graph)'
    print(tab + meth)
    
    res.append(meth)
    res.append('{')
    res.append(tab + "GRAPH(graph)")
    res += test_lines[pos+1:end + 1]
    res.append('}')
    res.append('')

    return pos, end, f"{tab}{pref}::{test}::CREATE({substr});"

def finish_test():
    global res
    if len(test_lines) <= 50:
        res += test_lines
        return
    avaliable_graph_names = [
        "GetGraph()", "graph", "defaultGraph","initialGraph",  "graph1","graphEt", "graph2", "expectedGraph",
        "sunkGraph", "graphCsed", "expected", "graphLsed", "optGraph", "optimizedGraph", "optimizableGraph", 
        "optimizableGraphAfter", "finalGraph", "graphPeepholed", "graphNotOptimizable", 
    ]

    found = False
    for n in avaliable_graph_names:
        try:
            pos_src, end_src, src_creat = cut_graph("src_graph", n)
        except ValueError:
            continue
        avaliable_graph_names.remove(n)
        found = True
        break
    
    if not found:
        raise ValueError()
    
    
    found = False
    for n in avaliable_graph_names:
        try:
            pos_out, end_out, out_creat = cut_graph("out_graph", n)
        except ValueError:
            continue
        avaliable_graph_names.remove(n)
        found = True
        break
    
    if not found:
        res += test_lines[:pos_src]
        res.append(src_creat)
        res += test_lines[end_src + 1:]
    else:
        res += test_lines[:pos_src]
        res.append(src_creat)
        res += test_lines[end_src + 1:pos_out]
        res.append(out_creat)
        res += test_lines[end_out + 1:]


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
