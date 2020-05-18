'''
Created on May 24, 2017

@author: Anwar Said
'''
import networkx as nx
import math
import random
from builtins import print
from ReadWrite import ReadWrite
from NetworkMeasures import NetworkMeasures
class GAOperators:
    # VARIABLES INITIALIZATION
    crosGen = 0
    crosRate = 0
    read = ReadWrite()
    globalQ = 0
    g1Nodes = []
    nodeCount = 0
    rList = []
    # PERFORMING CROSSOVER BY SELECTING TOP GENERATIONS BASED CROSSOVER RATE AND TOP_GENERATIONS PARAMETERS
    def performCrossover(self,crossoverRate,uniqueGen,topGen,gSize,nw,mutationRate,simpleMrate,graph):
        # print('---------------CROSSOVER------------------------------------------------------------')
        ga = GAOperators()
        self.globalQ = self.read.retrunTopMod()
        # print('global q :',self.globalQ)
        self.crosGen = math.floor(uniqueGen *topGen)
        if(self.crosGen<10):
            if(uniqueGen>10 & uniqueGen<100):
                self.crosGen = 10
            if(uniqueGen>=100):
                self.crosGen = uniqueGen * crossoverRate
            else:
                self.crosGen = uniqueGen
        # print('crosGen :',self.crosGen)
        self.crosRate = math.floor(self.crosGen * crossoverRate)
        if(self.crosRate<2):
            self.crosRate = 2
        # print('crosRate: ', self.crosRate)
        sMrate = math.floor(uniqueGen * simpleMrate)
        Ps = {}
        PsEdgeList = {}
        Ps.clear()
        # ITERATING FOR CROSSOVER RATE
        for i in range(0,self.crosRate):
            # print('crossover upper loop')
            count = 0
            # print('crossover')
            # ITERATING ON TOP GENERATIONS
            while(count<self.crosGen):
                # print('---------------CROSSOVER----------------')
                g1 = nx.Graph()
                g2 = nx.Graph()
                edgeListG1 = []
                edgeListG2 = []
                offspringEdgeList = []
                # GETTING TOP TWO GRAPHS AND HIS EDGELISTS BASED ON MODULARITY VALUE
                g1 = self.read.getGenerations(count)
                g2 = self.read.getGenerations(count+1)
                edgeListG1 = self.read.returnEdgeList(count,nw)
                edgeListG2 =  self.read.returnEdgeList(count+1,nw)
                if(not g1 is None and not  g2 is None):
                   offspringGraph = nx.Graph()
                   # APPLYING CROSSOVER TO GENERATE OFFSPRING
                   graphDic = ga.applyCrossover(g1,g2,graph,edgeListG1,edgeListG2)
                   offspringGraph = nx.Graph()
                   # GET OFFPSRING GRAPH AND EDGELIST
                   for oGraph,offspringList in graphDic.items():
                       offspringGraph = oGraph
                       offspringEdgeList = offspringList
                   # CALCULATING MODULARITY OF NEW GENERATED OFFSPRING GRAPH
                   mod = nw.calculateModularity(offspringGraph)
                   # STORING OFFSPRINGS IN DICTIONARY WITH MODULARITY AS A KEY
                   Ps[mod] = offspringGraph
                   PsEdgeList[mod] = offspringEdgeList
                count += 2
                # break
        # STORING GENEARTIONS IF MODULARITY IS IMPROVED
        for key,val in Ps.items():
            if(key>self.globalQ):
                # print("communities: ",len(nw.communities))
                # print('modularity improved in crossover:',key)
                self.globalQ = key
                edgelist = PsEdgeList.get(key)
                self.read.saveGenerations(key,val,nw,edgelist)

        # PERFORM MUTATION
        # print('--------------------------mutation')
        ga.performMutation(mutationRate,sMrate,graph,nw)

    def applyCrossover(self,g1,g2,graph,edgeListG1,edgeListG2):
#         GENERATING RANDOM BITS
        offspringEdgeList = []
        graphDic = {}
        offspringGraph = nx.Graph()
        # ADDING NODES IN OFFSPRING
        for nn in graph:
            offspringGraph.add_node(nn)
        self.g1Nodes.clear()
        self.nodeCount = g1.number_of_nodes()
        bits = [0,1]
        randBits = []
        randBits.clear()
        g2Nodes = []
        self.g1Nodes = g1.nodes()
        g2Nodes = g2.nodes()
        # GENERATING RANDOM BIT VECTOR TO PERFORM CROSSOVER BASED ON BITS
        for i in range(0,self.nodeCount):
            randBits.append(random.choice(bits))
        # print(randBits)
        for c in range(0,self.nodeCount):
            bit = randBits[c]
            # CHECKING FOR BIT ON NODE INDEX, AND IF BIT IS 1 THEN PARENT 1 EDGE WILL BE SELECTED, OTHERWISE PARENT 2
            if (bit==1):
                node = self.g1Nodes[c]
                eListNode = edgeListG1[c]
                # CHECKING FOR ISOLATED NODES IN THE ORIGINAL GRAPH, IF NODE IS ISOLATED THEN NO OPERATION WILL BE PERFORMED
                if(eListNode =='i'):
                    offspringEdgeList.append(eListNode)
                    continue
                secondNode = eListNode
                offspringGraph.add_edge(node,secondNode)
                offspringEdgeList.append(secondNode)
            else:
                node = g2Nodes[c]
                eListNode = edgeListG2[c]
                if(eListNode =='i'):
                    offspringEdgeList.append(eListNode)
                    continue
                secondNode = eListNode
                offspringGraph.add_edge(node,secondNode)
                offspringEdgeList.append(secondNode)
        # STORING THE OFFSPRING GRAPH AND HIS EDGELIST IN DICTIONARY TO RETURN IT
        graphDic[offspringGraph] = offspringEdgeList
        return graphDic

    def performMutation(self,mutationRate,sMrate,graph,nw):
        g = nx.Graph()
        Pm = {}
        Pe = {}
        mRate = math.floor(self.nodeCount*mutationRate)
        # ITERATING FOR TOP TEN GENERATIONS
        for i in range(0,10):
            # print('----------------------MUTATION------------------')
            g = self.read.getGenerations(i)
            edgeListforMG = []
            eList = self.read.returnEdgeList(i,nw)
            if ( g is None):
                break
            else:
                edgeListForMG = list(eList)
                mGraph = g.copy()
                self.rList.clear()
                # ITERATING ON THE SELECTED GENERATION FOR MUTATION RATE
                for j in range(0,mRate):
                    fNode = self.getRandomNode()
                    # print('first random node',fNode)
                    nodeNeig = None
                    flag = True
                    if(0 in self.g1Nodes):
                        nodeNeig = edgeListForMG[fNode]
                        flag = False
                    else:
                        nodeNeig = edgeListForMG[fNode-1]
                    if((nodeNeig =='i') | (nodeNeig is None)):
                        continue
                    originalNeighbors = graph.neighbors(fNode)
                    # print('originial Neighbors: ',originalNeighbors)
                    # print('existing neighbor: ',nodeNeig)
                    newNeighbor = None
                    newNeighbor = self.getRandomNeighbor(nodeNeig,originalNeighbors)
                    # print('newNeighbor; ',newNeighbor)
                    if (newNeighbor != None):
                        # APPENDING SELECTED NODES IN LIST TO PREVENT SELECTION NEXT TIME
                        self.rList.append(newNeighbor)
                        self.rList.append(nodeNeig)
                        # REMOVING THE EXISTING EDGE
                        mGraph.remove_edge(fNode,nodeNeig)
                        # UPDATING EDGE LIST BY INSERTING NEW NEIGHBOR
                        if(flag==False):
                            edgeListForMG[fNode] = newNeighbor
                            # print('elist is updated: ')
                        else:
                            edgeListForMG[fNode-1] = newNeighbor

                        mGraph.add_edge(fNode,newNeighbor)
                        # CHECKING FNODE IN THE INDEX OF SECOND NODE IN EDGELIST TO PREVENT SECOND NODE FROM ISOLATION
                        checkNode = None
                        if(flag ==False):
                            checkNode = edgeListForMG[nodeNeig]
                        else:
                            checkNode = edgeListForMG[nodeNeig-1]
                        if(checkNode==fNode):
                            uIndex = self.updateNodeIndex(nodeNeig,mGraph,graph)
                            if(uIndex is None):
                            #  NODE HAVE NO NEIGHBOR EXCEPT FIRST NODE
                                # ADDING REVERSE EDGE IN MGRAPH
                                mGraph.addEdge(nodeNeig,fNode)
                                # UPDATING EDGELIST AS WELL
                                if(flag==False):
                                    edgeListForMG[nodeNeig]= fNode
                                    # print('elist is updated for isolated node')
                                else:
                                    edgeListForMG[nodeNeig-1] = fNode
                                    # print('second new neighbor: ',fNode)
                            else:
                                newNeighbor = uIndex
                                mGraph.add_edge(nodeNeig,newNeighbor)
                                if(flag==False):
                                    edgeListForMG[nodeNeig]= newNeighbor
                                    # print('elist is updated for isolated node')
                                else:
                                    edgeListForMG[nodeNeig-1] = newNeighbor
                                    # print('second new neighbor: ',uIndex)


            mod = nw.calculateModularity(mGraph)
            # print('mutated graph modularity: ',mod)
            Pm[mod] = mGraph
            Pe[mod] = edgeListForMG
        topM = self.read.retrunTopMod()
        for key,val in Pm.items():
            if(key>topM):
                # print('modularity improved in mutation:',key)
                # print("communities: ",len(nw.communities))
                edgelist = Pe.get(key)
                self.read.saveGenerations(key,val,nw,edgelist)
        # simpleMrate = math.floor(len(self.g1Nodes)* 0.002)
        # print("simple mutation rate:   ", simpleMrate)
        self.performSimpleMutation(sMrate,graph,nw,self.read);

    def performSimpleMutation(self,mutationRate,graph,nw,read):
        # print("-------------------------------PERFORMING SIMPLE MUTATION------------------------------")
        mSGraph = nx.Graph()
        for i in range(0,10):
            g = self.read.getGenerations(i)
            
            eList = self.read.returnEdgeList(i,nw)
            if ( g is None):
                break
            else:

                edgeListForSMG = list(eList)

            mSGraph = g.copy()
            sMrate = mutationRate;
            nw.createCommunities(mSGraph);
#             print("communities: ",nw.communities)
#             print("edge List: ", edgeListForSMG)
#             print("sMrate: ",sMrate)
            for j in range(0,sMrate):
                if(len(nw.communities)>1):
                    newNeighbor = None
                    commRandomNode = None
                    # currentNeighbor = None
                    while(True):
                        if(len(nw.communities)<2):
                            break
                        randCommNo = random.randrange(start = 0, stop = len(nw.communities))
                        # print("random community Number: ", randCommNo)
                        community = nw.communities[randCommNo]
                        # print("community memebers: ", community)
                        if(len(community)>1):
                            commRandomNode = random.choice(community)
                            # print("random selected node from the selected random community:",commRandomNode)
                            nodeNeighbors = graph.neighbors(commRandomNode)
                            # print("nodeNeighbors: ", nodeNeighbors)
                            externalNeighbors = [x for x in nodeNeighbors if x not in community]
                            # print("external neighbors: ", externalNeighbors)
                            if(len(externalNeighbors)>0):
                                newNeighbor = random.choice(externalNeighbors)
                                break
                            else:
                                break
                    flag = True
                    if(0 in self.g1Nodes):
                        currentNeighbor = edgeListForSMG[commRandomNode]
                        flag = False
                    else:
                        currentNeighbor = edgeListForSMG[commRandomNode-1]
                    # print("Frist node: ",commRandomNode,"newNeighbor: ", newNeighbor,"current neighbor: ", currentNeighbor)
                    if(newNeighbor !=None):
                        mSGraph.add_edge(commRandomNode,newNeighbor)
#                         print("added edge:",commRandomNode, newNeighbor)
                        if(flag == False):
                            edgeListForSMG[commRandomNode] = newNeighbor
                        else:
                            edgeListForSMG[commRandomNode-1] = newNeighbor
                        # print("total edges: ",mSGraph.number_of_edges())
            deltaQ = nw.calculateModularity(mSGraph)
            # print("new Modularity: ", deltaQ)
            topM = read.retrunTopMod()
            # print("edge List: ", edgeListForSMG)
            if(deltaQ>topM):
                # print('modularity improved in simple mutation:',deltaQ)
                # print("communities: ",len(nw.communities))
                read.saveGenerations(deltaQ,mSGraph,nw,edgeListForSMG)

    def updateNodeIndex(self,nodeNeig,mGraph,graph):
        indexNode = nodeNeig
        # RETREIVING EXISTING NEIGHBORS
        neighbors = mGraph.neighbors(nodeNeig)
        # print('neighbors: ',neighbors)
        # RETREIVING ORIGINAL NEIGHBORS
        oNeighbors = graph.neighbors(nodeNeig)
        if(not neighbors):
            if(not oNeighbors):
                return None
            else:
                rNode = random.randrange(start=0,  stop = len(oNeighbors))
                newNeighbor = oNeighbors[rNode]
               # newNeighbor = self.getRandomNeighbor(neighbors,oNeighbors)
                return newNeighbor
        else:
            #EXISTING NEIGHBORS LIST IS NOT EMPTY, SELECTING A RANDOM NEW NEIGHBOR
            if (len(neighbors)>=2):
                newNode = random.randrange(start = 0, stop = len(neighbors))
                # print('random: ',newNode)
                newNeighbor = neighbors[newNode]
                return newNeighbor

            elif (len(neighbors)==1):
                newNeighbor = neighbors[0]
                # print('length of neighbor = 1:')
                return newNeighbor
            else:
                newNeighbor = neighbors
                return newNeighbor

    def connectNode(self,secondNode,mGraph,graph):
        GraphRec = {}
        sNode = secondNode
        # print('chechking of node for isolation: ',sNode)
        eNeig =  mGraph.neighbors(sNode)
        # print('eNeig for isolated node  :',eNeig)
        if(not eNeig):
            # print('node is isolated, checking neighbors to connect')
            oNeig = graph.neighbors(sNode)
            # print('neighbors node for isolated node:',oNeig)
            # rNode = random.randrange(start=0,  stop = len(oNeig))
            newNeighbor = random.choice(oNeig)
            #newNeighbor = self.getRandomNeighbor(eNeig,oNeig)
            if (newNeighbor != None):
                # print('new neighbor of isolated node:',newNeighbor)
                mGraph.add_edge(sNode,newNeighbor)
                # print('added edges : ',sNode,newNeighbor)
        #         STORING THE NEW NEIGHBOR OF ISOLATED NODE IN DICTIONARY TO UPDATE EDGE LIST IN THE PARENT METHOD AS WELL
                GraphRec [newNeighbor]= mGraph
                # print('Graph dictionary is returned for isolated node')
                return GraphRec

        else:
            # print('node is not isolated')
            return mGraph

    # SELECTING RANDOM NODE FROM THE GRAPH TO MUTATE
    def getRandomNode(self):
        # print('Random node selction')
        fNode = None
        while(fNode==None):
            # rNode = random.randrange(start=0,  stop = self.nodeCount)
            fNode = random.choice(self.g1Nodes)
            # print('fNode in random method:',fNode)
            # print('rList: ',self.rList)
            if(fNode in self.rList):
                # print('node in rList, recursion call')
                fNode = None
            else:
                # print('node not in rList, appended')
                self.rList.append(fNode)


        return fNode
    # SELECTING NEW NEIGHBOR FOR NODE
    def getRandomNeighbor(self,gNeighbors,originalNeighbors):
        # print('get Random Neighbor')
        existingNeighbor = gNeighbors
        if(not existingNeighbor):
            existingNeighbor = None
            # print('eNeighbors is not none; ',existingNeighbor)
        oNeighbors = originalNeighbors
        # print('oNeighbors in method: ',oNeighbors)
        if (len(oNeighbors)<1):
            return None
        else:
            if(existingNeighbor !=None):
                # print('e neighbor to be removed from list: ',existingNeighbor)
                # print('original neighbor list; ',oNeighbors)
                oNeighbors.remove(existingNeighbor)
                # print('oneighbors: ',oNeighbors)
                # print('existing neighbor is not none')

            if (len(oNeighbors)>=2):
                # newNode = random.randrange(start = 0, stop = len(oNeighbors))
                # print('random: ',newNode)
                newNeighbor = random.choice(oNeighbors)
                return newNeighbor

            elif (len(oNeighbors)==1):
                newNeighbor = oNeighbors[0]
                # print('lengthe of neighbor = 1:')
                return newNeighbor
            else:
                newNeighbor = existingNeighbor
                # print('existing neighbor is returned')
                return newNeighbor
