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

numErrors <- function(data){
  c1 <- length(which(data$data < -0.9 & data$data > -1.1))
  c2 <- length(which(data$data < -9 & data$data > -11))
  v <- c(c1,c2)
  v
}

numDifferent <- function(data){
  length(which(data$data > 0.2))
}

getSummary <- function(c1,c2){
  load(paste("geoblock_",c1,"_",c2,".Rdata",sep=""))
  c(numDifferent(thisData),numErrors(thisData))
}

plotExcess <- function(fn=NULL){
 require(ggplot2)
 B <- c("cu","ir","iq","kp","sd","sy","ve","ye","mm")
 Bl <- c("Cuba","Iran","Iraq","NorthKorea","Sudan","Syria","Venezuela","Yemen","Myanmar")
 NB <- c("ie","gb","jp","za")
 NBl <- c("Ireland","UK","Japan","SouthAfrica") 
 Cs <- c(B,NB)
 Csl <- c(Bl,NBl)
 l <- c(rep("Test",length(B)),rep("Control",length(NB)))
 xs <- sapply(Cs,
              function(c){
                v <- getSummary(c,"us")
                v[2] / v[3]
                }
              )
 xs <- unname(unlist(xs))
 print(xs)
 df <- data.frame(Country=Csl,Excess=xs,Status=l)
 print(df)
 p<-ggplot(data=df,aes(x=Country,y=Excess,fill=Status)) + 
   geom_bar(stat="identity") + 
   scale_x_discrete(limits=Csl) + 
   theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
 p
 if (!is.null(fn)){
   ggsave(fn)
 }
}