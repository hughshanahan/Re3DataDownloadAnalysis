#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 09:38:07 2020

@author: upac004
"""

import downloadAllSites as das
import json
from pathlib import Path
import os
import iso3166
import sys
import getopt

    
"""
   input country - two letter code ISO 3160 standard
         path - path to directory 
   output nothing
   side-effect - 
                 new directory with full run done for the country
                 
"""    
def runCountry(country,path):
    
    das.myConfig = das.getConfigData()

    countryPath = os.path.join(path,country)

    newCountryPath = os.path.join(path,country,"Rerun"+str(i))

    nPort = das.openPort(country)

    print("Country = "+das.countryForPort(nPort))

    pData = das.proxyData(nPort)
    das.makeDir(countryPath,removeOldEntries=True)
                                                                            
    portDataFn = os.path.join(countryPath,"portData.json") 
    with open(portDataFn,"w") as pDataOutFile:
        pDataOutFile.write(json.dumps(pData))
    
    das.getWebPage(failedRepos,countryPath)

    das.closePort(nPort)    

    return()

"""
   input filename (default analysedCountries.json)
   output list with countries stored in filename. If filename doesn't exist,
   return an empty list
"""
def findAnalysedCountries(filename="analysedCountries.json"):

    if Path(filename).exists():
        with open(filename, 'r') as openfile:
            json_object = json.load(openfile)
        return(json_object)
    else:
        return([])

"""
   input: doneCountries, filename
   output: save doneCountries to filename
"""
def updateDoneCountries(doneCountries, filename = "analysedCountries.json"):
    with open(filename,'w') as wfile:
        json.dump(doneCountries,wfile)
    

def main():

    countries = []
    for c in iso3166.countries_by_alpha2.keys():
        countries.append(c.lower())

    doneCountries = findAnalysedCountries()
    
    path = "../GlobalRun"

    for c in countries:
        if not c in doneCountries:
            print("Starting run on " + c)
            runCountry(country,path)
            print("Finished run on " + c)
            doneCountries.append(c)
            updateDoneCountries(doneCountries)
        
if __name__ == "__main__":
    main()





