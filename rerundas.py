#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 09:38:07 2020

@author: upac004
"""

import downloadAllSites as das
import json
import os
import iso3166
import sys
import getopt

countries = []
for c in iso3166.countries_by_alpha2.keys():
    countries.append(c.lower())

re3 = das.readReposList("./repos.json")
additional = das.readReposList("./additionalSites.json")
path = "../data"
    
"""
   input country - two letter code ISO 3160 standard
         path - path to directory 
         i - integer indicating which attempt being made
   output nothing
   side-effect - summary file
                 new directory with another attempt of repos for those failed. 
                 
"""    
def rerun(country,path,i):
    
    das.myConfig = das.getConfigData()

    print("Doing Rerun "+str(i))
    
    if i == 1:
        countryPath = os.path.join(path,country)
    else:
        countryPath = os.path.join(path,country,"Rerun"+str(i-1))

    newCountryPath = os.path.join(path,country,"Rerun"+str(i))

    summaryData = das.getSummaryData(countryPath,os.path.join(countryPath,"summary.csv")

    failedRepos = das.filterSummaryData(summaryData)
                                     
    nPort = das.openPort(country)

    print("Country = "+das.countryForPort(nPort))

    pData = das.proxyData(nPort)
    das.makeDir(newCountryPath)
                                                                            
    portDataFn = os.path.join(newCountryPath,"portData.json") 
    with open(portDataFn,"w") as pDataOutFile:
        pDataOutFile.write(json.dumps(pData))
    
    das.getWebPage(failedRepos,newCountryPath)

    das.closePort(nPort)    

    return()
                                     

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hc::",["country="])
    except getopt.GetoptError:
        print('rundas.py -c country (two leter code)')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('rundas.py -c country (two leter code)')
            sys.exit()
        elif opt == "-c":

            country = arg
            if not country in countries:
                print('rundas.py: '+country+' must be a valid two letter country code (ISO 3166 standard)')
                sys.exit(1)

            for i in range(1,11):
                rerun(path,country,i)







