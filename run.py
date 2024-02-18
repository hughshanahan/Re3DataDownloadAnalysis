
import downloadAllSites as das
myConfig=das.getConfigData()
repos = das.readReposList()

countries = ['ru','ua','by', 'fi', 'ee', 'lv', 'lt', 'md', 'pl', 'sk' , 'hu' , 'ro' , 'bg', 'tr', 'ge', 'am', 'az', 'kz', 'uz', 'tm', 'tj', 'kg', 'cn', 'ir'  ]
for c in countries:
    print("Doing "+c)
    cDir = "../r3d/"+c
    das.makeDir(cDir,removeOldEntries=True)
    opener = das.openProxy(c,myConfig)
    das.getWebResponse(repos,opener,jsonFnRoot=cDir)
