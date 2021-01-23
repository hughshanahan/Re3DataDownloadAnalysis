stringDistance <- function(s1,s2){
  require(stringdist)
  l = nchar(s1) + nchar(s2)
  s1pr <- gsub("[[:punct:]]","",s1)
  s2pr <- gsub("[[:punct:]]","",s2)
  stringdist(s1pr,s2pr,method='cosine',q=3)
}

cmpLists <- function(l1,l2){
  d = 0
#  print(l1)
  s1 = ifelse('text' %in% names(l1),l1$text,-1)
  s2 = ifelse('text' %in% names(l2),l2$text,-10) 
  t1 <- typeof(s1) == 'character'
  t2 <- typeof(s2) == 'character'
  if (t1 && t2){
      d = stringDistance(s1,s2)
  }
  else{
    if ( t1  ){
      d = s2
    }
    else {
      if ( t2  ){
        d = s1
      }
      else{
        d = s1 + s2
      }
    }
  }
  d
}

cmpJsonFiles <- function(fn1,fn2){
  require(jsonlite)
  l1 <- fromJSON(fn1)
  l2 <- fromJSON(fn2)
  cmpLists(l1,l2)
}

cmpFolders <- function(p1,p2){
  files1 = dir(path=p1,pattern=".json")
  files2 = dir(path=p2,pattern=".json")
  files = files1[which(files1 %in% files2)]
  
  results = c()
  for ( f in files ){
    f1 = paste(p1,f,sep="/")
    f2 = paste(p2,f,sep="/")
    results = c(results,cmpJsonFiles(f1,f2))
  }
  names(results) <- files
  print(results)
  results
}

runAllFolders <- function(myFolder){
  allFolders <- dir(myFolder)
  N <- length(allFolders)
#  for ( i in seq(1,N-1) ){
#    for ( j in seq(i+1,N) ){
#      fi <- allFolders[i]
#      fj <- allFolders[j]
  for ( fi in allFolders ){
    thisData <- list()
    for ( fj in allFolders ){
      if ( fi != fj ){
        print(c(fi,fj))
        x <- cmpFolders(fi,fj)
        thisData$country1 <- fi
        thisData$country2 <- fj
        thisData$data <- x
        fn <- paste("/Users/upac004/Downloads/geoblock_",fi,"_",fj,".Rdata",sep="")
        save(thisData,file = fn)
      }  
    }
  }
  
}

