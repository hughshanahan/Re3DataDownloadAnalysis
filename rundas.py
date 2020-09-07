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

das.myConfig = das.getConfigData()

country = 'jp'

re3 = das.readReposList("./repos.json")
additional = das.readReposList("./additionalSites.json")

path = "../data"

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
                
            nPort = das.openPort(country)

            print("Country = "+das.countryForPort(nPort))

            pData = das.proxyData(nPort)

            dataPath = os.path.join(path,country)
            print("dataPath = "+dataPath)
            das.makeDir(dataPath)
    
            portDataFn = os.path.join(dataPath,"portData.json") 
            with open(portDataFn,"w") as pDataOutFile:
                pDataOutFile.write(json.dumps(pData))
    
            das.getWebPage(additional,dataPath)
            das.getWebPage(re3,dataPath)
        

            das.closePort(nPort)    






