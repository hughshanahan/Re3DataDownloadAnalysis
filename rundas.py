#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 09:38:07 2020

@author: upac004
"""

import downloadAllSites as das

das.myConfig = das.getConfigData()

country = 'jp'
nPort = das.openPort(country)

print("Country = "+das.countryForPort(nPort))

pData = das.proxyData(nPort)

print(pData)

das.closePort(nPort)

for country in das.countriesList:
    






