#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:18:51 2020

@author: upac004
"""

import os
import sys
import ssl
import urllib.request
import re
import json
#import string
import time
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import csv
import iso3166



#countriesList = ['ir','cu','sd','ye','iq','ve','sy','mm','ie','za','gb']

#countriesList = ['jp','us','ir','cu','sd','ye','iq','ve','sy','mm','ie','za','gb']
#countriesList = ['kp']
#kp = North Korea?
countriesList=[]
for c in iso3166.countries_by_alpha2.keys():
    countriesList.append(c.lower())


"""
    input : filename
    output : dictionary of private data
"""
def getConfigData(filename='myConfig.json'):
    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)
    return(json_object)

"""
   input: country - must be two letter code in countriesList
   output: urllib opener
   opens a BrightData proxy for a specific country 
  
"""

def openProxy(country):
    ssl._create_default_https_context = ssl._create_unverified_context
    pstr = 'http://'+myConfig[username]+"-country-"+country+":"+myConfig[password]+"@"+myConfig[host]
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': pstr, 'https':pstr}))
    except urllib.error.URLError as e:
        print("downloadAllSite.openProxy : "+e.reason)
    return(opener)
 
"""
    output: return json of proxy data
"""
def proxyData(port):
    
    PROXY = homeIP+":"+str(port)
    proxyDict = { "http":PROXY,"https":PROXY,"ftp":PROXY}
    response = requests.get('http://lumtest.com/myip.json',proxies=proxyDict)
    return(response.json())
        

"""
input fn 
creates a file (filename fn) with a list of repo ids from r3data
"""
def downloadRepos(fn='../repos/repos.txt'):
    command = 'curl -o r.xml https://www.re3data.org/api/v1/repositories; grep \<id\> r.xml > '+fn+';rm -f r.xml'
    os.system(command)


"""
input repoFn,jsonFn
output list of tuples, each tuple is (repoId, repoURL)
If jsonFn is not the default it also saves data as json
"""
def collateRepoURLs(repoFn='../repos/repos.txt',jsonFn=""):
    repos = []
    with open(repoFn) as f:
        for line in f:
            r = (line.split(r'<id>')[1]).split(r'</id>')[0]
            command = 'curl -o r.xml https://www.re3data.org/api/v1/repository/'+r
            os.system(command)
            with open('r.xml', 'r') as fXml:
                for lineXml in fXml.readlines():
                    if 'repositoryURL' in lineXml:
                        x = lineXml.split(r'<r3d:repositoryURL>')
                        if len(x) > 1:
                            url = (x[1]).split(r'</r3d:repositoryURL>')[0]
            repos.append((r,url))

    if jsonFn != "":
        with open(jsonFn,'w') as fo:
            json.dump(repos,fo)

    return(repos)
 
"""
input URLfn - filename of file with URLs
output tuples of form (id,url)
"""   

def collateURLs(URLfn):
    repos = []
    i = 0
    f = open(URLfn,'r')
    x = f.read()
    r = x.split("\n")    
    for url in r:
        repos.append((str(i),url))
        i += 1
    return(repos)
    
"""
input filename
output repos list of tuples of form (r3dID, url)
"""
def readReposList(filename="../repos/repos.json"):
    with open(filename) as f:
        return(json.load(f))
    
"""
input filename, repos list of tuples of form (r3dID, url)
saves repos as a json file
"""    
def writeReposList(repos,filename="../repos/repos.json"):
    with open(filename, 'w') as json_file:
        json.dump(repos,json_file)

"""
input repos - list of repos (tuples (r3dID, url)), opener (proxy)
attempts to download a set of web pages corresponding to the list of repos and returns status messages of that
"""        
def getWebResponse(repos,opener,jsonFnRoot="../r3d/",TIMEOUT=30):
    
    for (r,url) in repos:
        print(r + " " + url)
        responseData = {}
        responseData['url'] = url
        responseData['ID'] = r
# Set up session so that request looks as if it is from a standard browser
        hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}
        req = urllib.request.Request(url, headers=hdr)
        try:
# Try and perform get, if there is an error or timeout, record that information 
            with opener.open(req,timeout=TIMEOUT) as response:
            responseData['status'] = response.code
            responseData['headers'] = dict(response.headers)
        except urllib.error.HTTPError as e:
            responseData['status'] = e.code
            responseData['headers'] = dict(e.headers)    
        
        jsonFn = os.path.join(jsonFnRoot, r + ".json")

        with open(jsonFn, 'w') as json_file:
            json.dump(responseData,json_file)
            
"""
input path - directory name
output jsonFiles - list of files that end in ".json" in the directory
"""            
def listJsonRepoFiles(path="./"):
    jsonFiles = []
    for f in os.scandir(path):
        if re.search(r'.json$',f.name):
            jsonFiles.append(f.name)
            
    return(jsonFiles)

"""
input str1, str2 two strings, clean Boolean to decide to remove stop words and punctuation
output cosine of feature vectors
"""
def computeSimilarity(str1,str2,clean=False):
#    if clean_string:
#        s1 = clean_string(str1)
#        s2 = clean_string(str2)
#    else:
    s1 = str1 
    s2 = str2

    if len(s1) > 0 and len(s2) > 0: 
        strings = [s1,s2]
    
        vectorizer = CountVectorizer().fit_transform(strings)
        vectors = vectorizer.toarray()
        return(cosine_similarity(vectors)[0][1])
    else:
        return(0.0)

"""
input s string
output string with stop words and punctuation removed from s
"""
#def clean_string(s):
#    text = "".join([word for word in s if word not in string.punctuation])
#    text = "".text.lower()
#    text = " ".join([word for word in text.split() if word not in stopwords ])
#    return(text)

"""
input newDir string
      removeOldEntries (optional - default False)
check if newDir already exists as a dir, if it doesn't create it. If removeOldEntries is True then remove all old files in that directory 
"""
def makeDir(newDir,removeOldEntries=False):
# Check if newDir exists otherwise create it
    p = Path(newDir)
    if p.exists():
        if removeOldEntries:
            for f in os.listdir(newDir):
                fp = os.path.join(newDir,f)
                os.remove(fp)
    else:
        os.mkdir(newDir)
    
"""
input oldDir - directory with repo json files
      newDir - directoty where repos that timed out will be rerun and stored
output number of repos that timed out      
"""
def reRunTimeOutRepos(oldDir,newDir):
    # Check if newDir exists otherwise create it
    makeDir(newDir)

    nTimedOut = 0
        
    # Find all json files in oldDir
    allRepos = listJsonRepoFiles(oldDir)
    timedOutReposList = []
    # Loop through the repos and find the ones that had a time out
    for repoFn in allRepos:
        repoPlusPath = os.path.join(oldDir,repoFn)
        repo = readReposList(repoPlusPath)
        if 'Timeout' in repo:
            (r,url) = (repo['ID'],repo['url'])
            timedOutReposList.append((r,url))
            nTimedOut += 1
    
    # Now rerun download attempt with timed out repos
    if nTimedOut > 0:
        getWebPage(timedOutReposList,newDir)

    return(nTimedOut)            


    
"""
input : repo1, repo2 - two dicts carrying summary information on repos
output : cosine similarity between texts

The two repos should be downloaded from the same repository and will produce 
an error if their id's do not match

"""        
def compareRepoTexts(repo1,repo2):
    # Check if they have the same ID, otherwise fail
    if repo1['ID'] != repo2['ID']:
        raise RuntimeError('Repository dictionaries compared do not have the same ID')
        
    if not ( 'text' in repo1 ) and not ( 'text' in repo2 ):
        return(-1)
    elif not ( 'text' in repo1 ) or not ( 'text' in repo2 ):     
        return(0)
    else:
        return(computeSimilarity(repo1['text'],repo2['text']))

"""
  input: dir - directory to read data; storeSummery (default TRUE) - return csv file of summary data; summaryFileName (default "summary.csv") - csv file of summary data
  output: list of filenames that generated an error 
"""

def getSummaryRepoData(dir,storeSummary=True,summaryFileName="summary.csv"):

    headings = ["filename","url","Timeout","HTTPError","otherErr","status_code"]
    listRepos = listJsonRepoFiles(dir)
    summaryData = []
        
    for filename in listRepos:
# Don't include port information json file        
        if filename != "portData.json":
            with open(os.path.join(dir,filename)) as f:
                rd = json.load(f)
# Add empty field to repo dict for any key not there                
                for key in headings[1:]:
                    if not key in rd:
                        rd[key] = ""
                rd["filename"] = filename
                summaryData.append(rd)

    if storeSummary:
        with open(summaryFileName,'w') as fout:
            csvf = csv.writer(fout)
            csvf.writerow(headings)
            for r in summaryData:
                l = []
                for k in headings:
                    l.append(r[k])
                csvf.writerow(l)
        
    return(summaryData)


"""
   input: summaryData list of tuples carrying data about downlaod repo data
   output: list of tuples of form (id, url) - only carrying those urls that had
           problems (time out etc.)
"""
def filterSummaryData(summary):
    fl = []
    for r in summary:
        if r["Timeout"] != "" or r["HTTPError"] != "" or r["otherErr"] != "" or r["status_code"] >= 400:
            id = r["filename"].replace('.json','')
            fl.append((id,r['url']))
    return(fl)

"""
input: repoFn - filename with json file of repo ID tuples
       rootDir - root directory for saving data
ouput: none

repoFn is read and the list of repos downloaded in the root directory in folder 0
pauseLength seconds later the repos that are timed out are rerun in folder 1 and so on until we
get to folder maxIter-1.
"""

    
def fullRun(repoFn,rootDir,maxIter=20,pauseLength=3600):
    repos = readReposList(repoFn)
    iter = 0
    allDone = False
    
    print("Analysing for ",rootDir)
    makeDir(rootDir)

    print("Starting initial run")
    oldDir = os.path.join(rootDir,str(iter))
    makeDir(oldDir)
    
    getWebPage(repos, jsonFnRoot = oldDir)
    
    while  not allDone and iter < maxIter:
        iter += 1
        print("Initial run done - pausing for one hour")
        time.sleep(pauseLength)
        newDir = os.path.join(rootDir,str(iter))
        print("Rerunning on iteration" + str(iter) + "for timed out cases.")
        print("Storing to" + newDir)
        
        nTimedOut = reRunTimeOutRepos(oldDir,newDir)
        print(str(nTimedOut) + " repos timed out on " + oldDir)
        allDone = nTimedOut == 0
        
        
        
            
    
    
            
        
    
    
    






        
    
            
        
            
        


        
        
        
        
        
        








    
    
