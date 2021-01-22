stringDist <- function(s1,s2){
  require(stringdist)
  l = nchar(s1) + nchar(s2)
  stringdist(s1,s2,method='lcs')
}

cmpLists <- function(l1,l2){
  d = 0
  s1 = ifelse('text' %in% names(l1),l1$text,-1)
  s2 = ifelse('text' %in% names(l2),l2$text,-10) 
  if (typeof(s1) == 'character' && typeof(s2) == 'character'){
      d = stringDist(s1,s2)
  }
  else{
    if ( typeof(s1) == 'character' ){
      d = s2
    }
    else {
      if ( typeof(s2) == 'character' ){
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
  
  results = list()
  for ( f in files ){
    f1 = paste(p1,f,sep="/")
    f2 = paste(p2,f,sep="/")
    results[f] = cmpJsonFiles(f1,f2)
  }
  results
}

