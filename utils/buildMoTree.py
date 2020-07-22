import json
import copy
import sys
# pip install anytree
from anytree import Node, RenderTree

def buildContains(filename):
    global contains
    global isConfigurable
    global identifiedBy
    global props
    contains = {}
    # isConfigurable = {}
    identifiedBy = {}
    props = {}
    with open(filename) as json_file:
        data = json.load(json_file)
        mos = data['classes']
        # print(json.dumps(mos, indent=4, sort_keys=True))
        for mo in mos:
            modata = data['classes'][mo]
            contains[mo] = modata['contains'].keys()
            # isConfigurable[mo] = modata['isConfigurable']
            identifiedBy[mo] = modata['identifiedBy']
            props[mo] = modata['properties']

def getCorrectMo(mo):
    for key in contains:
        if mo in [x.lower() for x in contains[key]]:
            for each in contains[key]:
                if mo == each.lower():
                    return each

def getChild(mo):
    try:
        return contains[mo.name]
    except KeyError:
        print('not found')
        sys.exit(1)

def getParents(mo):
    plist = []
    for key in contains:
        if mo in contains[key]:
            plist.append(key)
    return plist

def recurc(mo):
    clist = getChild(mo)
    if not clist:
        return
    for c in clist:
        if identifiedBy[c]:
            child = Node(c, parent=mo, id=identifiedBy[c])
        else:
            child = Node(c, parent=mo)
        recurc(child)

def recurp(mo):
    plist = getParents(mo.name)
    if not plist:
        for pre, fill, node in RenderTree(mo):
            try:
                print("%s%s %s" % (pre, node.name, node.id))
            except AttributeError:
                print("%s%s" % (pre, node.name))
        return
    for p in plist:
        if p == 'topSystem':
            rmos.append(copy.deepcopy(mo))
            return
        if identifiedBy[p]:
            po = Node(p, id=identifiedBy[p])
        else:
            po = Node(p)
        mo.parent=po
        recurp(po)

if  __name__ == "__main__":
    if len(sys.argv) < 3:
        print('please provide dme json file and MO name')
        print('ex: python buildMoTree ./dme-9.3.5-meta.json snmpLocalUser')
        sys.exit(1)
    filename = sys.argv[1]
    mo = sys.argv[2]
    sys.setrecursionlimit(10**6)
    buildContains(filename)
    mo = mo.lower()
    mo = getCorrectMo(mo)
    if not mo:
        print("bad MO")
        sys.exit(1)
    global origmo
    global rmos
    global ts
    rmos = []
    if identifiedBy[mo]:
        origmo = Node(mo, id=identifiedBy[mo])
    else:
        origmo = Node(mo)
    ts = Node("topSystem")
    print("parents:\n")
    recurp(origmo)
    for each in rmos:
        each.parent=ts
    if rmos:
        for pre, fill, node in RenderTree(ts):
            try:
                print("%s%s %s" % (pre, node.name, node.id))
            except AttributeError:
                print("%s%s" % (pre, node.name))
    print("\n")
    print('properties of '+mo+':')
    print(sorted([*props[mo]]))
    print("\n")
    if mo == 'topSystem' or mo == 'regressIf' or mo == 'syntheticSwTLTestObj':
        print('too many children: unable to print')
        sys.exit(0)
    recurc(origmo)
    print("children:\n")
    for pre, fill, node in RenderTree(origmo):
        try:
            print("%s%s %s" % (pre, node.name, node.id))
        except AttributeError:
            print("%s%s" % (pre, node.name))
