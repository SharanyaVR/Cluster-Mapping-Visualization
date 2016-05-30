import pandas
import operator
import numpy as np
import json

listofclustermappingfiles = [["/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/offercluster2attrcluster.txt","O","A"],
                             ["/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/offercluster2servicecluster.txt","O","S"],
                             ["/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/offercluster2webpagecluster.txt","O","P"],
                             ["/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/pagecluser2servicecluster.txt","P","S"],
                             ["/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/pagecluster2attrcluster.txt","P","A"],
                             ["/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/webpagecluster2featurecluster.txt","P","F"],
                             ]

listofClusterDetailAndIndexFiles = [["/home/sharanyavraju/DR/GitHub/dig-coclustering/graph-files/detail/attrdetail.txt", "/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/attrcluster.txt","A"],
                                    ["/home/sharanyavraju/DR/GitHub/dig-coclustering/graph-files/index/wordindex.txt", "/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/featurecluster.txt","F"],
                                    ["/home/sharanyavraju/DR/GitHub/dig-coclustering/graph-files/index/offerindex.txt","/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/offercluster.txt","O"],
                                    ["/home/sharanyavraju/DR/GitHub/dig-coclustering/graph-files/detail/pagedetail.txt","/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/webpagecluster.txt","P"],
                                    ["/home/sharanyavraju/DR/GitHub/dig-coclustering/graph-files/detail/servicedetail.txt","/home/sharanyavraju/DR/GitHub/dig-coclustering/clustering_results/newest_raw_results/cluster-45/servicecluster.txt","S"],
                                    ]

IdValueMapping = {}
DictofPropertyDetails = {}

def getDetailsaAboutCluster(indexfile, clusterfile):
    print indexfile +" ____ " + clusterfile
    with open(indexfile) as clusterdetails:
        for line in clusterdetails:
            word = line.split()
            print str(word) + "---" + str(line)
            IdValueMapping[int(word[0])+1] = word[1]

    ClusterDataFrame = pandas.read_csv(clusterfile, "\t", header=None)
    Detailsdict = {}

    for row in ClusterDataFrame.iterrows():
        clusterid = int(row[1][1])
        propertyId = int(row[1][0])
        if propertyId in IdValueMapping:
            if clusterid in Detailsdict:
                Detailsdict[clusterid].append([IdValueMapping[propertyId], row[1][2]])
            else:
                Detailsdict[clusterid] = []
                Detailsdict[clusterid].append([IdValueMapping[propertyId], row[1][2]])

        for key in Detailsdict:
            templist = sorted(Detailsdict[key], key = lambda x: x[1], reverse=True)
            #print templist
            Detailsdict[key] = templist[:10]
            # print str(Detailsdict[key])

    return Detailsdict

def createNodeLists(filepath, firstprefix, secondprefix):
    linkdictlist = []
    nodedictlist = []

    dataframe = pandas.read_csv(filepath,"\t",header=None)

    property1 = list(dataframe[0])
    # print secondprefix
    # print DictofPropertyDetails[firstprefix][1]
    nodedictlist1 = [{"name":firstprefix+"C-"+str(x), "group":firstprefix+"C", "top10values":DictofPropertyDetails[firstprefix][x]} for x in property1 if x in DictofPropertyDetails[firstprefix]]
    property2 = list(dataframe[1])
    nodedictlist2 = [{"name":secondprefix+"C-"+str(x), "group":secondprefix+"C", "top10values":DictofPropertyDetails[secondprefix][x]} for x in property2 if x in DictofPropertyDetails[secondprefix]]
    nodedictlist = nodedictlist1 + nodedictlist2

    maxedgeweight = max(row[1][2] for row in list(dataframe.iterrows()))

    for row in list(dataframe.iterrows()):
        if int(row[1][0]) in DictofPropertyDetails[firstprefix] and int(row[1][1]) in DictofPropertyDetails[secondprefix]:
            source = firstprefix + "C-"+str(int(row[1][0]))
            target = secondprefix + "C-" +str(int(row[1][1]))
            weight = 1#row[1][2]/maxedgeweight
            linkdict = {"source":source, "target":target, "value":weight}
            linkdictlist.append(linkdict)

    return nodedictlist, linkdictlist

def main():
    listofClusterMappings = []
    nodedictlist = []
    linkdictlist = []

    for indexfile, clusterfile, property in listofClusterDetailAndIndexFiles:
        DictofPropertyDetails[property] = getDetailsaAboutCluster(indexfile, clusterfile)

    with open("logfile", "w") as logfile:
        json.dump(DictofPropertyDetails, logfile)
    for filename, property1, property2 in listofclustermappingfiles:
        nodedictlist1,linkdictlist1 = createNodeLists(filename, property1, property2)
        nodedictlist += nodedictlist1
        linkdictlist += linkdictlist1

    nodedictlist = list(np.unique(np.array(nodedictlist)))
    print str(nodedictlist)

    for dic in linkdictlist:
        dic["source"] = nodedictlist.index([x for x in nodedictlist if x['name'] == dic["source"]][0])
        dic["target"] = nodedictlist.index([x for x in nodedictlist if x['name'] == dic["target"]][0])

    with open("clustermapping.json","w") as f:
        json.dump({"nodes":nodedictlist, "links": linkdictlist}, f)

main()
