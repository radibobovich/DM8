import tkinter.messagebox
from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
from netgraph import Graph
root = Tk()

# Add node fields
prevnodeLabel = Label(root, text='Предыдущая вершина')
prevnodeLabel.pack()
prevnodeEntry = Entry(root, width=50)
prevnodeEntry.pack()
weightAddByNodeEntryLabel = Label(root, text='Вес дуги')
weightAddByNodeEntryLabel.pack()
weightAddByNodeEntry = Entry(root, width=50)
weightAddByNodeEntry.pack()

prevnodeEntry.insert(END, 0)
weightAddByNodeEntry.insert(END, 10)
lastNode = 0

mx = [[-99]] # adjacency matrix with weights
lmx = [] # lambda matrix
nmx = [] # previous nodes matrix
# lambda matrix contains in each cell: 1) value, 2) list of previous nodes (usually one node in list)
def expandMatrix():
    global mx
    global lmx
    global lastNode

    # expand ajacency matrix
    mx.append([-99] * (lastNode + 1))#    add a new line
    for i in range(len(mx)):    #   elongation of each line by one element
        mx[i].append(-99)

recursionDepth = 0
ways = []

def getmydata(waylist):
    global finishNode, lmx
    waysMessage = 'Максимальные пути: \n'
    for i in range(len(ways)):
        ways[i].reverse()
        waysMessage = waysMessage + str(ways[i]) + ", длина: " + str(lmx[finishNode][findLimit(finishNode)])+'\n'

    tkinter.messagebox.showinfo(message=waysMessage, title='Максимальный путь')


def getwaylist(col, fn, waylist): # recurrent function that should print several ways if there are
    global mx, lmx, nmx, recursionDepth, ways, length
    if fn == 0:
        if waylist:
            print(waylist)
            ways.append(waylist)
            getmydata(ways)
        return 0
    else:
        for i in range(len(nmx[fn][col])):
            if recursionDepth == 0:
                waylist.append(fn)
            waylist.append(nmx[fn][col][i])


            recursionDepth += 1
            getwaylist(findLimit(nmx[fn][col][i]), nmx[fn][col][i], waylist)    #call self to write way from previous node
            recursionDepth -= 1
            #waylist.clear()


def findLimit(finishNode):  #in lambda mx find column from which value stops increasing
    global mx, lmx, nmx
    column = 0
    for j in range(1, len(lmx)-1):
        if (lmx[finishNode][j-1] == lmx[finishNode][j]) and (lmx[finishNode][j] > 0):
            column = j - 1
            return column
            break

    getwaylist(column, finishNode, [])
def maxsum(li, lj): # finds max sum (lambda_i ^(k-1) + C_ij)
    global mx, lmx
    maxs = -99
    prevs = []
    for i in range(len(mx)): # finds max sum
        if lmx[i][lj-1] + mx[i][li] > 0 and lmx[i][lj-1] + mx[i][li] > maxs:
            maxs = lmx[i][lj-1] + mx[i][li]

    for i in range(len(mx)):
        if lmx[i][lj-1] + mx[i][li] == maxs: # finds nodes with that sum
            prevs.append(i) # or prevs.append(li)
    return [maxs, prevs]

finishNode = 11
def maxpath():
    global mx, lmx, ways, finishNode, nmx
    lmx.clear()
    nmx.clear()
    #creating clean lambda and prevNodes matrix
    lmx.append([0]*len(mx))
    nmx.append([ [] ]*len(mx))
    for i in range(1, len(mx)):
        lmx.append([-99])
        nmx.append([ [] ]*len(mx))


    #fill lambda matrix
    for lj in range(1, len(mx)): # changing column in lambda
        for li in range(1, len(mx)): # changing line in lambda
            lmx[li].append(-99)
            buff = maxsum(li, lj)   # buffer contains max sum at [0] and list of prev nodes at [1]
            lmx[li][lj] = buff[0]
            nmx[li][lj] = buff[1]

    # for lj in range(0, len(mx)): # changing column in lambda
    #     for li in range(0, len(mx)): # changing line in lambda
    #         if (lj == 0 or li == 0) and len(nmx[li][lj]) == 0:
    #             nmx[li][lj].append(0)
    #         else:
    #             lmx[li].append(-99)
    #             buff = maxsum(li, lj)   # buffer contains max sum at [0] and list of prev nodes at [1]
    #             lmx[li][lj] = buff[0]
    #             nmx[li][lj] = buff[1]


    finishNode = int(finishNodeEntry.get())
    ways.append(getwaylist(findLimit(finishNode), finishNode, []))   #get all ways (sure it cannot display more than two, recursion problems)

    showMatrix()

def showMatrix():
    print()
    for i in range(len(mx)): # adjacency matrix
        for j in range(len(mx[i])):
            print('{:4}'.format(mx[i][j]), end='')
            #print(matrix[i][j], end=' ')
        print()
    print()

    print()
    for i in range(len(lmx)): # lambda matrix
        for j in range(len(lmx[i])):
            print('{:3}'.format(lmx[i][j]), end='')
        print()
    print()

    print()
    for i in range(len(lmx)):  # previous nodes matrix
        for j in range(len(lmx[i])):
            print(nmx[i][j], end='')
        print()
    print()
def AddNode():
    global lastNode
    G.add_weighted_edges_from([(int(prevnodeEntry.get()), lastNode + 1, int(weightAddByNodeEntry.get()))])
    expandMatrix()
    mx[int(prevnodeEntry.get())][lastNode + 1] = int(weightAddByNodeEntry.get())
    lastNode += 1
    tempprevnode = int(prevnodeEntry.get())
    prevnodeEntry.delete(0, 'end')
    prevnodeEntry.insert(END, tempprevnode + 1)
    weightAddByNodeEntry.delete(0, 'end')
    refreshScreen()

btnAddNode = Button(root, text="Добавить вершину", command=AddNode)
btnAddNode.pack()


node_layout = 'spring'
def setSpringLayout():
    global node_layout
    node_layout = 'spring'
    refreshScreen()

def setCircularLayout():
    global node_layout
    node_layout = 'circular'
    refreshScreen()


# Add edge fields
firstnodeEntry = Entry(root, width=50)
firstnodeEntryLabel = Label(root, text='Первая вершина')
lastnodeEntry = Entry(root, width=50)
lastnodeEntryLabel = Label(root, text='Вторая вершина')
weightEntry = Entry(root, width=50)
weightEntryLabel = Label(root, text='Вес дуги')
firstnodeEntryLabel.pack()
firstnodeEntry.pack()
lastnodeEntryLabel.pack()
lastnodeEntry.pack()
weightEntryLabel.pack()
weightEntry.pack()

def AddEdge():
    global lastNode
    global mx
    if not G.has_node(int(lastnodeEntry.get())):
        print('Created a new node when creating edge')
        expandMatrix()
        lastNode += 1
    G.add_weighted_edges_from([(int(firstnodeEntry.get()), int(lastnodeEntry.get()), int(weightEntry.get()))])  #add edge
    refreshScreen()
    print('Added edge from ', firstnodeEntry.get(), " to ", lastnodeEntry.get(), " with weight ", weightEntry.get())
    mx[int(firstnodeEntry.get())][int(lastnodeEntry.get())] = int(weightEntry.get())    # add a connection in matrix

btnAddEdge = Button(root, text="Добавить дугу", command = AddEdge)
btnAddEdge.pack()

btnShowMatrix = Button(root, text="М-ца смежности (debug)", command = showMatrix)
btnShowMatrix.pack()


# layouts
btnLayoutSpring = Button(root, text="Вид А", command=setSpringLayout)
btnLayoutCircular = Button(root, text="Вид Б", command=setCircularLayout)
btnLayoutSpring.pack()
btnLayoutCircular.pack()


G = nx.DiGraph()    # create an orgraph
G.add_node(0)

def makeTestMatrix():
    global mx
    G.clear()
    mx = [[-99,   3,  11,   4, -99, -99,   8, -99, -99, -99, -99, -99],
          [-99, -99,   7, -99,   9,   7, -99, -99, -99, -99, -99, -99],
          [-99, -99, -99, -99,   2, -99, -99,   3,   3, -99, -99, -99],
          [-99, -99,   9, -99, -99,   4,   2, -99, -99, -99, -99, -99],
          [-99, -99, -99, -99, -99, -99, -99,   5, -99, -99, -99, -99],
          [-99, -99, -99, -99, -99, -99, -99,   4, -99,   8,   5, -99],
          [-99, -99, -99, -99, -99,   5, -99, -99,   8,   9, -99, -99],
          [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99,  11, -99],
          [-99, -99, -99, -99, -99, -99, -99, -99, -99,   4, -99,   5],
          [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99,   4,   3],
          [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,   2],
          [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99]]
    for i in range(len(mx)): # make nodes
        G.add_node(i)
    for i in range(len(mx)): # connect nodes
        for j in range(len(mx[i])):
            if mx[i][j] >= 0:
                G.add_weighted_edges_from([(i, j, mx[i][j])])
    refreshScreen()

btnMakeTestMatrix = Button(root, text="Тестовая матрица", command = makeTestMatrix)
btnMakeTestMatrix.pack()

btnMaxPath = Button(root, text="Максимальный путь", command = maxpath)
btnMaxPath.pack()

finishNodeLabel = Label(root, text="До какой вершины?")
finishNodeLabel.pack()
finishNodeEntry = Entry(root, width=50)
finishNodeEntry.pack()
def refreshScreen():
    global node_layout
    plt.clf()
    edge_labels = nx.get_edge_attributes(G, "weight")
    Graph(G, node_labels=True, edge_labels=edge_labels,
          edge_label_fontdict=dict(size=6, fontweight='bold'),
          node_layout=node_layout, edge_layout='curved',
          node_size=10, edge_width=3, edge_label_position=0.7, arrows=True, scale=(6, 6))

    plt.show()

if G.edges:
    refreshScreen()
# print("Number of nodes =", G.number_of_nodes())
# print("Number of edges =", G.number_of_edges())
#
# print("G.nodes = ", G.nodes)
# print("G.edges = ", G.edges)

root.mainloop()