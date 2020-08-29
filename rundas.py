#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 09:38:07 2020

@author: upac004
"""

import downloadAllSites as das
import json
import os

das.myConfig = das.getConfigData()

country = 'jp'

re3 = das.readReposList("./repos.json")
additional = das.readReposList("./additionalSites.json")

path = "../data"
 
for country in das.countriesList:
    nPort = das.openPort(country)

    print("Country = "+das.countryForPort(nPort))

    pData = das.proxyData(nPort)

    dataPath = os.path.join(path,country)
    print("dataPath = "+dataPath)
    das.makeDir(dataPath)
    
    portDataFn = os.path.join(dataPath,"portData.json") 
    with open(portDataFn,"w") as pDataOutFile:
        pDataOutFile.write(json.dumps(pData))
        
    das.getWebPage(re3,dataPath)
    das.getWebPage(additional,dataPath)    

    das.closePort(nPort)    






