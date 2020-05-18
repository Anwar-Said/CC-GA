'''
Created on May 24, 2017

@author: Anwar Said
'''
import networkx as nx
import math
import csv
import params
from ReadWrite import  ReadWrite
from NetworkMeasures import NetworkMeasures
from GAOperators import GAOperators
rw = ReadWrite()
# READING PARAMS.PY TO LOAD BASIC PARAMETERS AND DATASETS
parameters = rw.loadParameters()
# SETING PARAMETERS
r = math.floor(parameters[1])
mutationRate = parameters[2]
sMrate =  parameters[3]
crossoverRate = parameters[4]
topGen = parameters[5]
gSize = math.floor(parameters[6])
dataSets = rw.returnDatasets(parameters)
iterations = parameters[7]
print(dataSets)
print('r = {}, mutationRate = {}, simpleMutationRate = {}, crossoverRate = {}, topGenerations = {}, generationSize = {}, iterations = {}'.format(r, mutationRate, sMrate, crossoverRate, topGen, gSize, iterations))
for d in range(0,len(dataSets)):
    rw.keysList.clear()
    rw.searchSpace.clear()
    iterations = parameters[7]
    print('{},'.format(dataSets[d]),end='',flush=True)
    #print('Mutation Rate:',mutationRate)
    # READING DATASET FROM GML
    graph = rw.readfile(dataSets[d])
    if(graph != None):
        total_nodes = graph.number_of_nodes()
        nm = NetworkMeasures(graph)
        cc = nm.calculateCC(graph)
        networkItr = 0
        print('Experiment #,Unique Generations,Initial # Communities,Initial Modularity,It 1,It 2,It 3,')
        for networkItr in range(0,iterations):
            rw.searchSpace.clear()
            rw.keysList.clear()
            print('{},'.format(networkItr),end='',flush=True)
            for itr in range(0,gSize):
                newG = nx.Graph()
                # REBUILD GENERATIONS GRAPHS FROM ORIGINAL GRAPH GRAPH
                newGDic = nm.rebuildGraph (graph)
                for key,val in newGDic.items():
                    newG = key
                    edgeList = val
                    # Calculating modularity of new graph
                    Q = nm.calculateModularity(newG)
                    # SAVING THE GENERATION IN SEARCH SPACE INCLUDING HIS EDGE  LIST AND MODULARITY VALUE
                    searchSpace = rw.saveGenerations(Q, newG,nm,edgeList)
                    break

            uniqueGen = len(rw.searchSpace)
            print('{},'.format(uniqueGen),end='',flush=True)
            globalQ = rw.retrunTopMod()
            finalGraph = nx.Graph();
            finalGraph = rw.searchSpace[globalQ]
            nm.createCommunities(finalGraph)
            print('{},'.format(len(nm.communities)),end='',flush=True)
            print('{0:.4f},'.format(globalQ),end='',flush=True)
            go = GAOperators()
            # GETTING HIGHEST MODULARITY OF THE GENERATIONS
            count = 1
            iterations = 1
            while(True):
                # print('----------------------------')
                go.performCrossover(crossoverRate,uniqueGen,topGen,gSize,nm,mutationRate,sMrate,graph)
                mod = rw.retrunTopMod()
                if(mod <= globalQ):
                    count += 1
                    if(count >= r):
                        break
                    #if(total_nodes>1000):
                    print("{0:.4f},".format(mod), end='', flush=True)
                else:
                    #if(total_nodes>200):
                    print("{0:.4f},".format(mod), end='', flush=True)
                    globalQ = mod
                    count = 0
                iterations +=1
            # print('total generations : ',len(rw.returnGenerations()))
            print('\nHighest Modularity:',globalQ)
            fGraph =nx.Graph()
            fGraph = rw.searchSpace[globalQ]
            roundedGQ =round(globalQ,4)
            nm.createCommunities(fGraph)
            print('Communities: ',len(nm.communities))
            i = 0
            try:
                file = open('../results.csv','a',newline ='')
                writer = csv.writer(file,delimiter = ',', quoting=csv.QUOTE_MINIMAL);
                data = [[dataSets[d],iterations,topGen,crossoverRate,mutationRate,r, globalQ,len(nm.communities)]];
                writer.writerows(data);
                #rw.writeGml(dataSets[d], roundedGQ,cc,nm.communities)
                rw.writeOriginalGML(dataSets[d], roundedGQ, cc, nm.communities,graph)
                # rw.writeText(dataSets[d],mutationRate,globalQ,crossoverRate,i)
                # # print('data inserted in file')
                rw.writeCommunities(dataSets[d],mutationRate,nm,roundedGQ)
                file.close()
                i+=1
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))

            #break
    #break







