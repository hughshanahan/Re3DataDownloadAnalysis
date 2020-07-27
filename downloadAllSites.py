#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:18:51 2020

@author: upac004
"""

import os
import requests
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
import re
import json
import string
import time
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
#import nltk
#nltk.download('stopwords')
#from nltk.corpus import stopwords
#stopwords = stopwords.word('english')


"""
input fn 
creates a file (filename fn) with a list of repo ids from r3data
"""
def downloadRepos(fn='../repos/repos.txt'):
    command = 'curl -o r.xml https://www.re3data.org/api/v1/repositories; grep \<id\> r.xml > '+fn+';rm -f r.xml'
    os.system(command)


"""
input repoFn
output list of tuples, each tuple is (repoId, repoURL)
"""
def collateRepoURLs(repoFn='../repos/repos.txt'):
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
input repos - list of repos (tuples (r3dID, url))
downloads web pages corresponding to the list of repos.
"""        
def getWebPage(repos,jsonFnRoot="../r3d/",TIMEOUT=30):
    for (r,url) in repos:
        print(r + " " + url)
        responseData = {}
        responseData['url'] = url
        responseData['ID'] = r
# Set up session so that request looks as if it is from a standard browser
        http = requests.Session()
        http.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
})
        try:
# Try and perform get, if there is an error or timeout, record that information            
            response = http.get(url,timeout=TIMEOUT)
            response.raise_for_status()
        except Timeout:
            print("Timeout")
            responseData['Timeout'] = True    
        except HTTPError as http_err:
            responseData['HTTPError'] = str(http_err)
        except Exception as err:
            responseData['otherErr'] = str(err)

            
        else:
            responseData['headers'] = dict(response.headers)
            responseData['text'] = response.text
            responseData['status_code'] = response.status_code
        
        jsonFn = jsonFnRoot + r + ".json"

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
    
    strings = [s1,s2]
    
    vectorizer = CountVectorizer().fit_transform(strings)
    vectors = vectorizer.toarray()
    return(cosine_similarity(vectors)[0][1])

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
check if newDir already exists as a dir, if it doens't create it
"""
def makeDir(newDir):
# Check if newDir exists otherwise create it
    p = Path(newDir)
    if not p.exists():
        os.mkdir(newDir
    
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
        
    if not ( 'text' in repo1 and 'text' in repo2 ):
        raise RuntimeError('Repository dictionary does not have text in it')
    else:
        return(computeSimilarity(repo1['text'],repo2['text']))

"""
input: repoFn - filename with json file of repo ID tuples
       rootDir - root directory for saving data
ouput: none

repoFn is read and the list of repos downloaded in the root directory in folder 0
an hour later the repos that are timed out are rerun in folder 1 and so on until we
get to folder maxIter-1.
"""
    
def fullRun(repoFn,rootDir,maxIter=20):
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
        time.sleep(3600)
        newDir = os.path.join(rootDir,str(iter))
        print("Rerunning on iteration" + str(iter) + "for timed out cases.")
        print("Storing to" + newDir)
        
        nTimedOut = reRunTimeOutRepos(oldDir,newDir)
        print(str(nTimedOut) + " repos timed out on " + oldDir)
        allDone = nTimedOut == 0
        
        
        
            
    
    
            
        
    
    
    






        
    
            
        
            
        


        
        
        
        
        
        








    
    