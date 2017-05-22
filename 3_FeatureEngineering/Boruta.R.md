```
library(Boruta)
set.seed(888)
iris.extended<-data.frame(iris,apply(iris[,-5],2,sample))
names(iris.extended)[6:9]<-paste("Nonsense",1:4,sep="")
final.boruta = Boruta(Species~.,data=iris.extended,doTrace=2)
getSelectedAttributes(final.boruta,withTentative = F)
attStats(final.boruta)
```