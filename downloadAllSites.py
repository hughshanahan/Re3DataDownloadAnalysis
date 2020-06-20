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
# Set up session so that request looks as if it is from a standard browser
        http = requests.Session()
        http.headers.update({"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
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
            
            
def listJsonRepoFiles(path="./"):
    jsonFiles = []
    for f in os.scandir(path):
        if re.search(r'.json$',f.name):
            jsonFiles.append(f.name)
            
    return(jsonFiles)


        
    
            
        
            
        


        
        
        
        
        
        








    
    