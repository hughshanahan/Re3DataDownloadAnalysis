import downloadAllSites as das
import json
import pandas as pd
import sys
import os
from collections import defaultdict 

"""
  setup multi-dimensional dict
"""
def multi_dict(K, type): 
    if K == 1: 
        return defaultdict(type) 
    else: 
        return defaultdict(lambda: multi_dict(K-1, type)) 

    
"""
 input directory to read entries from
 output list with tuples of form (filename, url)

"""
def getSites(directory):
    sites = []
    with os.scandir(directory) as it:
        for entry in it:
            if entry.name.endswith('.json') and not entry.name.startswith('portData'):
                fp = open(entry)
                r = json.load(fp)
                sites.append((entry.name,r['url']))
    return(sites)

"""
  input directory
  output return list of entries in directory
"""

def getCountries(directory):
    countries = []
    with os.scandir(directory) as it:
        for entry in it:
            countries.append(entry.name)
    return(countries)

"""
 input list of countries and sites
 output empty pandas dataframe with rows being countries and columns being files 
"""
def setUpDataFrame(countries,sites):
    urls = []
    for s in sites:
        urls.append(s[1])
    df = pd.DataFrame(columns=urls,index=countries)
    return(df)


"""
  input root (to find files) contries, sites
  output dict of form url, country_i, country_j storing similarity
"""
def computeAllSimilarities(root,countries,sites):
   # df = setUpDataFrame(countries,sites)
    similarities = multi_dict(3,float)
    nc = len(countries)
    for i in range(nc):
        ci = countries[i]
        print("First country = "+ci)
        for j in range(i+1,nc):
            cj = countries[j]
            print("Second country = "+cj)
            if i != j:
                for (fn,url) in sites:
                    fi = os.path.join(root,ci,fn)
                    fj = os.path.join(root,cj,fn)
                    fpi = open(fi)
                    ri = json.load(fpi)
                    fpi.close()
                    fpj = open(fj)
                    rj = json.load(fpj)
                    fpj.close()
                    s = das.compareRepoTexts(ri,rj)
#                    print(ci,cj,url,s)
                    if s < 0.9:
                        similarities[url][ci][cj] = s
    return(similarities)

    
countries = getCountries("../data")
sites = getSites("../data/us")

sims = computeAllSimilarities("../data",countries,sites)
with open("./similarities.json","w") as sdump:
    json.dump(sims,sdump)
    
