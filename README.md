# Re3DataDownloadAnalysis
Python script to bulk download web pages from Re3Data and gather statistics about their download.

Scripts are being updated to incorporate new API changes from BrightData which simplifies the process significantly. 

The update will include
- script(s) to download latest versions from Re3Data,
- scripts to do the downloads from each VPN,
- simple analysis scripts.

The focus here will be on nations in conflict, specifically those affected by the war in Ukraine.


**Getting the latest version of Re3Data**

import downAllSites as das
das.downloadRepos(fn="./repos.xml') #Pulls out Re3Data Ids
repos = das.collateRepoURLs("./repos.xml","./repos.json") #Save a json file of Re3Data Ids and their URLs
 
