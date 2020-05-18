'''
Created on May 24, 2017

@author: Anwar Said
'''
import networkx as nx
class ReadWrite:
    searchSpace = {}
    keysList = []
    # READING DATA SET FROM GML FORMAT
    def readfile(self, fName):
        try:
            fType = ".gml"
            fileName1 = fName
            fileName = "".join((fName, fType))
            path = '../networks/'
            cPath = "".join((path, fileName))
            # print(cPath)
            # READING DATASET BY PASSING COMPLETE PATH
            graph = nx.read_gml(cPath, label="id")
            print('Network is successfully loaded with ', graph.number_of_nodes(), 'nodes and ',
                  graph.number_of_edges(), 'edges')
            #             G = nx.Graph()
            #             for u,v,data in graph.edges_iter(data=True):
            #                 w = data
            #                 if not G.has_edge(u,v):
            #                     G.add_edge(u, v, weight=w)
            # #                else:
            # #                    G[u][v]['weight'] += w
            #
            # print('After removing multiple edges       ',G.number_of_nodes(),'nodes and ',G.number_of_edges(),'edges')
            return graph
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            # print('dataset not found')

    # READING PARAMS.PY TO GET PARAMETERS
    def loadParameters(self):
        import params
        fileName = params.fileName
        r = params.r
        mrate = params.mutationRate
        smrate = params.simpleMutationRate
        cRate = params.crossoverRate
        topGen = params.topGenerations
        generationSize = params.generationSize
        iterations = params.iterations
        # APPENDING EACH DATASET IN LIST
        list1 = []
        list1.append(fileName)
        list1.append(r)
        list1.append(mrate)
        list1.append(smrate)
        list1.append(cRate)
        list1.append(topGen)
        list1.append(generationSize)
        list1.append(iterations)
        return list1

    # RETURN DATASET
    def returnDatasets(self, parameters):
        fileNames = []
        for i in parameters:
            if (isinstance(i, float) | (isinstance(i, int))):
                continue
                # print('object is float',i)
                # print(i,'---')
            else:

                for j in i:
                    fileNames.append(j)
        return fileNames

    # SAVING GENERATIONS IN SEARCH SPACE
    def saveGenerations(self, Q, newGraph, nm, edgeList):
        self.searchSpace[Q] = newGraph
        nm.edgeListDic[Q] = edgeList
        if (Q not in self.keysList):
            self.keysList.append(Q)
            sorted(self.keysList)
            self.keysList.sort(reverse=True)
        return self.searchSpace

    # GETTING GENERATION FROM SEARCH SPACE USING INDEX VALUE
    def getGenerations(self, index):
        if (index >= len(self.keysList)):
            return None
        else:
            g = nx.Graph()
            # print('this is sortedKeys',self.keysList)
            q = self.keysList[index]
            # print ('generation modularity:',q)
            g = self.searchSpace.get(q)
            return g

    # GETTING EDGE LIST FOR THE GRAPHS USING INDEX
    def returnEdgeList(self, index, nm):
        if index >= len(self.keysList):
            return None
        q = self.keysList[index]
        # print('ge modularity in EdgeList: ', q)
        eList = nm.edgeListDic.get(q)
        return eList

    # RETURN COMPLETE SEARCH SPACE
    def returnGenerations(self):
        return self.searchSpace

    # PRINTING WHOLE SEARCH SPACE
    def printGen(self):
        print('this is print generation')
        for q, g in self.searchSpace.items():
            print(q)
            if (g is None):
                print('g is empty')
            else:
                print(g.edges())

    # RETURN TOP MODULARITY VALUE FROM THE GENERATIONS
    def retrunTopMod(self):
        if (not self.keysList is None):
            mod = self.keysList[0]
        return mod

    # WRITING GRAPHS IN GML FORMATS
    def writeGml(self, fName, globalQ,CC,communities):
        try:
            topMod = self.retrunTopMod()
            graph = self.searchSpace.get(topMod)
            fType = ".gml"
            fileName1 = fName
            strMRate = fileName1 + str(globalQ)

            path = "../networks/gml/"
            fileName = strMRate + fType
            cPath = "".join((path, fileName))
            # ROUND CLUESTERING COEFFICIENT VALUES ADDING IN GML AS A NODE ATTRIBUTE
            roundedCC = {}
            for i in graph.nodes_iter():
                roundedCC[i] = round(CC[i],4)
            nx.set_node_attributes(graph, "CC", roundedCC)
            # SETTING UP NODES COMMUNITIES AND ADDING IN GML AS A NODE ATTRIBUTE
            nodeCommunities = {}
            index = 0
            for key in roundedCC:
                if(key==1):
                    index =1
                break

            for node in graph.nodes_iter():
                for key,valu in communities.items():
                   if(node in valu):
                        nodeCommunities[index] = key
                        break
                index = index+1
            nx.set_node_attributes(graph,"community",nodeCommunities)
            nx.write_gml(graph, cPath)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    def writeOriginalGML(self, fName, globalQ,CC,communities, OriginalGraph):
        try:
            topMod = self.retrunTopMod()
            graph = OriginalGraph
            fType = ".gml"
            fileName1 = fName
            strMRate = fileName1 + str(globalQ)

            path = "../networks/gml/"
            fileName = strMRate + fType
            cPath = "ORIG".join((path, fileName))
            # ROUNDED CLUESTERING COEFFICIENT VALUES ADDING IN GML AS A NODE ATTRIBUTE
            roundedCC = {}
            for i in graph.nodes_iter():
                roundedCC[i] = round(CC[i],4)
            nx.set_node_attributes(graph, "CC", roundedCC)
            # SETTING OF NODES COMMUNITIES AND ADDING IN GML AS A NODE ATTRIBUTE
            nodeCommunities = {}
            index = 0
            for key in roundedCC:
                if(key==1):
                    index =1
                break

            for node in graph.nodes_iter():
                for key,valu in communities.items():
                   if(node in valu):
                        nodeCommunities[index] = key
                        break
                index = index+1
            nx.set_node_attributes(graph,"community",nodeCommunities)
            nx.write_gml(graph, cPath)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    def writeGmlGraph(self, fName, graph):
        try:
            topMod = self.retrunTopMod()
            newGraph = graph
            fType = ".gml"
            fileName1 = fName

            path = '../gml/'
            fileName = fileName1 + fType
            cPath = "".join((path, fileName))
            # print('cPath: ',cPath)
            nx.write_gml(newGraph, cPath)
        except:
            print('file not printed')

    # WRITING DATASET NAME INCLUDING MUTATIONRATE PARAMETER AND HIS MODULARITY IN TEXT FILE
    def writeText(self, fName, mrate, mod, crossoverRate, density, i):
        try:
            fType = ".txt"
            mutRate = mrate
            Q = mod
            dName = fName
            fileName1 = dName + "_Stat" + str(i) + fType
            path = "../networks/gml/"
            cPath = "".join((path, fileName1))
            file = open(cPath, 'w', newline='')
            file.write("Mutation  Rate:    ")
            file.write(str(mutRate))
            file.write('\n')
            file.write('Crossover Rate:')
            file.write(str(crossoverRate))
            file.write('\n')
            file.write("Maximum Modularity:   ")
            file.write(str(Q))
            file.write('\n')
            file.write('Density:')
            file.write(str(density))

            file.close()
        except:
            print('text file not printed')

    def writeCommunities(self, fileName, mrate, nm, globalQ):
        fName = fileName
        fType = '.txt'
        fileName1 = fName+ str(globalQ) + fType
        path = "../networks/gml/"
        cPath = "".join((path,  fileName1))
        # print('file path : ',path)
        file = open(cPath, 'w', newline='')
        q = self.retrunTopMod()
        graph = self.searchSpace[q]
        nm.createCommunities(graph)
        for c, nodes in nm.communities.items():
            for n in nodes:
                file.write(str(n))
                file.write(' ')

            file.write('\n')

        file.close()
