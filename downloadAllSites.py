#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:18:51 2020

@author: upac004
"""

import os

"""
input fn 
creates a file (filename fn) with a list of repo ids from r3data
"""
def downloadRepos(fn):
    command = 'curl -o r.xml https://www.re3data.org/api/v1/repositories; grep \<id\> r.xml > '+fn+';rm -f r.xml'
    os.system(command)


"""
input repoFn
output list of tuples, each tuple is (repoId, repoURL)
"""
def collateRepoURLs(repoFn):
    repos = []
    with open(repoFn) as f:
        for line in f:
            r = (line.split(r'<id>')[1]).split(r'</id>')[0]
            repos.append(r)
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
input repos - list of repos (tuples (r3dID, url))
downloads web pages corresponding to the list of repos.
"""        
def getWebPage(repos):
    for repo in repos:
        command = 'curl -o r3d/'+repo[0]+'.html '+repo[1]
        os.system(command)

        
        
        
        
        
        








    
    