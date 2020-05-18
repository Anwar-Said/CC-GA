'''
Created on May 24, 2017

@author: Anwar Said
'''
# THIS CLASS CONTAINS METHODS FOR ALL REQUIRED NETWORKS MEASURES
import networkx as nx
import random
class NetworkMeasures:
    # INITIALIZING REQUIRED DATA STRUCTURES
    nodeList = []
    cc = []
    originalGraph = nx.Graph()
    communities = {}
    edgeListDic = {}
    totalEdges = 0;
    # CLASS CONSTRUCTOR TO INITIALIZE GRAPHS
    def __init__(self, graph):
        self.originalGraph = graph
        self.totalEdges = self.originalGraph.number_of_edges()
    # CALCULATING LOCAL CLUSTERING COEFFICIENT FOR EACH NODE
    def calculateCC(self,g):
        self.cc = nx.clustering(g)
        # print('clustering coefficient ');
        # for i in self.cc:
        #     print(self.cc[i])
        return self.cc

    # GENERATING GRAPHS FOR GENERATIONS
    def rebuildGraph(self,graph):
        edgeList = []
        # initializing new graph
        newGraph = nx.Graph()
        for n in graph.nodes_iter(graph):
            newGraph.add_node(*n)
            # self.nodeList.append(n)
        # print('nodes in newGraph :',newGraph.number_of_nodes())
        self.nodeList.clear()
        self.nodeList = newGraph.nodes()
        # print('node list size ',len(self.nodeList))
        # CHECKING NODE AND INITIALIZING CC
        for node in self.nodeList:
            maxCC = -1
            linkedNode = None
            neighbors = []
            # FINDING neighbors of each node
            # neighbors = self.findNeighbors(node);
            neighbors = self.originalGraph.neighbors(node)
            # print('node: ',node,'->',neighbors)

            # TRAVERSING NEIGHBORS
            for nei in neighbors:
                ccOfNode = self.cc.get(nei)
                if (random.random()> 0.5):
                    if(ccOfNode > maxCC):
                        maxCC = ccOfNode
                        linkedNode = nei
                else:
                    if (ccOfNode >= maxCC):
                        maxCC = ccOfNode
                        linkedNode = nei
            if (linkedNode != None):
                newGraph.add_edge(node,linkedNode)

                edgeList.append(linkedNode)
                #print('node:',node,'->',linkedNode)
                # print(node,linkedNode)
            else:
                # 'I' WILL BE APPEND IN EDGELIST IF NODE IS ISOLATED
                edgeList.append('i')
        gDic = {}
        gDic[newGraph] = edgeList
        return gDic

    # FINDING NEIGHBORS OF NODE
    def findNeighbors(self,node):
        return nx.all_neighbors(self.originalGraph,node)
    # CREATING COMMUNITIES FROM THE NEW GENERATED GRAPH REQUIRED TO COMPUTE MODULARITY
    def createCommunities(self,newGraph):
        self.communities.clear()
        for n in newGraph:
            self.traverseNode(n,newGraph)
    # TRAVERING NODE
    def traverseNode(self,n,newGraph):
        # print('traverseNode is called')
        node = n
        nodeNei = []
        nodeNei = newGraph.neighbors(node)
        if(not nodeNei is None):
            myList = self.nodeInList(n)
            if(myList == -1):
                myList = len(self.communities)
                c = []
                c.append(n)
                self.communities[myList] = c

            for nn in nodeNei:
                if(nn in self.communities.get(myList)):
                    continue
                self.communities[myList].append(nn)
                self.traverseNode(nn,newGraph)

    def nodeInList(self,n):
        output =-1
        for i in range(0, len(self.communities)):
            c1 = self.communities.get(i)
            if(n in c1):
                output =i
                break
        return output

    def printCommunities(self):
        print(self.communities)
        # print(self.newGraph.edges())

    def saveEdgeList(self,Q,eList):
        self.edgeListDic[Q] = eList
    def printEdgeDict(self):
        print(self.edgeListDic.keys())
        for key in self.edgeListDic:
            print('key : ',key)
            print('val :',self.edgeListDic[key])
    # METHOD FOR COMPUTING MODULARITY OF THE GRAPHS
    def calculateModularity(self,newGraph):
        self.createCommunities(newGraph)
        # print('calculate modularity')
        # print('this is original graph',self.originalGraph.number_of_edges())
        # print('new graph nodes ',newGraph.number_of_edges())

        modularity = 0

        for i in range(0, len(self.communities)):

            iDegree = 0
            edgesCount = 0

            for n in self.communities[i]:
                for e in nx.all_neighbors(self.originalGraph, n):
                    iDegree += 1

            for n in self.communities[i]:
                for e in nx.all_neighbors(self.originalGraph, n):
                    if (e in self.communities[i]):
                        edgesCount += 1
            edgesCount /= 2

            sqr = iDegree/(self.totalEdges*2)
            modularity += (edgesCount/self.totalEdges)-(sqr*sqr)
        # print(modularity)
        return  modularity
    def findDensity(self,finalGraph):
        self.createCommunities(finalGraph)
        totalEdges = self.originalGraph.number_of_edges()
        density = 0
        averageDensity = 0
        for i in range(0, len(self.communities)):
            edgesCount = 0
            nodesCount = len(self.communities[i])
            for n in self.communities[i]:
                for e in nx.all_neighbors(self.originalGraph, n):
                    if (e in self.communities[i]):
                        edgesCount += 1
            edgesCount /= 2
            if(nodesCount-2 > 0):
                density += edgesCount*(((edgesCount-(nodesCount-1)))/((nodesCount-2)*(nodesCount-1)))
        averageDensity =((2*density)/totalEdges)

        return  averageDensity
