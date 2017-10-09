#########################################
# 주제: 집값예측
# 최종수정일: 2017.09.20
# 작성자: 윤일근
#########################################
#패키지 설치 및 로딩
library(reshape2)
library(data.table)
library(ggplot2)
library(dplyr)
library(caret)
library(e1071)
library(class)
library(h2o)
localH2O=h2o.init()
#2016/01~2016/12월 집값데이터로 2016/10~12월과 2017/10~12월 집값을 예측 (logerror predict)
setwd("C:/Users/il-geun/Desktop/zillow")
train1 <- fread("train_2016_v2.csv",header=T)  #거래가 있던 정보들 => 한번에 여러개인건 어떻게 처리? 방조건은 안달라짐
train2 <- fread("train_2017.csv",header=T)
train <- rbind(train1, train2)

properties1 <- fread("properties_2016.csv", header = T, stringsAsFactors = T)
properties2 <- fread("properties_2017.csv", header = T, stringsAsFactors = T)
properties <- rbind(properties1, properties2)
summary(properties)
#2016년에는 결측이지만 2017년에는 있는거가 많음 -> 보정으로 생각 / 2016년 이후 개조로 바뀌었을 가능성고도 려  

sub <- fread("sample_submission.csv",header=T)

pro_na2 <- properties1[properties1$parcelid %in% properties2[is.na(properties2$latitude),]$parcelid ,]
properties2 <-  rbind(properties2[!is.na(properties2$latitude),], pro_na2)

pro_na1 <- properties2[properties2$parcelid %in% properties1[is.na(properties1$latitude),]$parcelid ,]
properties1 <-  rbind(properties1[!is.na(properties1$latitude),], pro_na1)

properties1$censustractandblock[properties1$censustractandblock == -1] <- NA #3건뿐 => 결측처리
properties2$censustractandblock[properties2$censustractandblock == -1] <- NA 

#summary(properties1$assessmentyear)
#p1 <- properties %>% 
#       group_by(parcelid) %>% 
#       summarise(diff(structuretaxvaluedollarcnt))
#summary(p1)
#diff(c(NA,99))
#properties <- properties[duplicated(properties) == F ,] #5966749

train$year <- as.factor(substr(train$transactiondate,1,4))
train$month <- as.factor(as.numeric(substr(train$transactiondate,6,7)))
#train에 있는 결과값은 모두 sub에 넣기 
colnames(train)[1] <- "ParcelId"
sub <- merge(sub, subset(train[train$year=="2016" & train$month == "10",], select = c("ParcelId", "logerror") ), by = "ParcelId", all.x = T)
colnames(sub)[ncol(sub)] <- "log201610"
sub <- merge(sub, subset(train[train$year=="2016" & train$month == "11",], select = c("ParcelId", "logerror") ), by = "ParcelId", all.x = T)
colnames(sub)[ncol(sub)] <- "log201611"
sub <- merge(sub, subset(train[train$year=="2016" & train$month == "12",], select = c("ParcelId", "logerror") ), by = "ParcelId", all.x = T)
colnames(sub)[ncol(sub)] <- "log201612"

m_y <- train %>%
  group_by(year, month) %>%
  summarise(mm = mean(logerror))
plot(m_y$mm) #경향성이 보임

properties <- properties1

#data 컬럼별 타입 변환
properties$rawcensustractandblock <- as.factor(properties$rawcensustractandblock)
properties$censustractandblock <- as.factor(properties$censustractandblock)
properties$regionidzip <- as.factor(properties$regionidzip)
properties$regionidcounty <- as.factor(properties$regionidcounty)
properties$regionidcity <- as.factor(properties$regionidcity) #1803개 결측
properties$fips <- as.factor(properties$fips)# Federal Information Processing Standard code
properties$propertylandusetypeid <- as.factor(properties$propertylandusetypeid) #결측 x
#properties$propertycountylandusecode <- as.factor(properties$propertycountylandusecode) #코드가 너무 다양 (1)
#properties$propertyzoningdesc <- as.factor(properties$propertyzoningdesc)             # 코드가 너무 다양(31962)


#properties$hashottuborspa <- as.factor(properties$hashottuborspa) #스파여부
#properties$fireplaceflag <- as.factor(properties$fireplaceflag) 
#properties$taxdelinquencyflag <- as.factor(properties$taxdelinquencyflag) 
#위경도 로그변환
properties$latitude <- log(properties$latitude)
properties$longitude <- log(abs(properties$longitude))

#필요없는 컬럼 제거
#properties <- subset(properties,select=c(-assessmentyear))
summary(properties)
properties$storytypeid[is.na(properties$storytypeid)] <- "na"
properties$storytypeid <- as.factor(properties$storytypeid)
properties$pooltypeid2[is.na(properties$pooltypeid2)] <- "na"
properties$pooltypeid2 <- as.factor(properties$pooltypeid2)
properties$pooltypeid7[is.na(properties$pooltypeid7)] <- "na"
properties$pooltypeid7 <- as.factor(properties$pooltypeid7)
properties$pooltypeid10[is.na(properties$pooltypeid10)] <- "na"
properties$pooltypeid10 <- as.factor(properties$pooltypeid10)
properties$decktypeid[is.na(properties$decktypeid)] <- "na"
properties$decktypeid <- as.factor(properties$decktypeid)
properties$buildingclasstypeid[is.na(properties$buildingclasstypeid)] <- "na"
properties$buildingclasstypeid <- as.factor(properties$buildingclasstypeid)

#
properties$airconditioningtypeid[is.na(properties$airconditioningtypeid)] <- "na"
properties$airconditioningtypeid <- as.factor(properties$airconditioningtypeid)
properties$architecturalstyletypeid[is.na(properties$architecturalstyletypeid)] <- "na"
properties$architecturalstyletypeid <- as.factor(properties$architecturalstyletypeid)
properties$buildingqualitytypeid[is.na(properties$buildingqualitytypeid)] <- "na"
properties$buildingqualitytypeid <- as.factor(properties$buildingqualitytypeid)
properties$heatingorsystemtypeid[is.na(properties$heatingorsystemtypeid)] <- "na"
properties$heatingorsystemtypeid <- as.factor(properties$heatingorsystemtypeid)
properties$typeconstructiontypeid[is.na(properties$typeconstructiontypeid)] <- "na"
properties$typeconstructiontypeid <- as.factor(properties$typeconstructiontypeid)


properties$regionidneighborhood[is.na(properties$regionidneighborhood)] <- "na"
properties$regionidneighborhood <- as.factor(properties$regionidneighborhood)
properties$typeconstructiontypeid[is.na(properties$typeconstructiontypeid)] <- "na"
properties$typeconstructiontypeid <- as.factor(properties$typeconstructiontypeid)

#이런건 2를 1로 대체 (지리적 특성은 일치할 것임)
#properties1[is.na(properties1$fips),]
#properties2[is.na(properties2$fips),]

#properties1[is.na(properties1$latitude),]
#properties2[is.na(properties2$latitude),]

summary(properties)
properties$censustractandblock <- as.character(properties$censustractandblock)
properties$censustractandblock[is.na(properties$censustractandblock)] <- "na"
properties$censustractandblock <- as.factor(properties$censustractandblock)
censustractandblock

#수치형 변수
#이상값 결측값 처리 필요 => 데이터에 대한 이해가 동반이 되야함. 논리적인 처리필요


#regionidcounty(부동산위치가 방이 0 개인데는 3101에 다 있고, 3101에는 없음)
#typeconstructiontypeid, fireplaceflag 는 방 1개 이상인 곳만 있음
summary(as.factor(properties[properties$roomcnt == 0, ]$typeconstructiontypeid ))
properties$typeconstructiontypeid[properties$roomcnt == 0 & properties$typeconstructiontypeid =="11" ] <- NA
summary(as.factor(properties[properties$roomcnt == 0, ]$fireplaceflag )) #위에 이상값에 포함됨 => 수정요함
properties$fireplaceflag[properties$roomcnt == 0 & properties$fireplaceflag != "" ] <- ""


#결측값에 대한 고민을 해야함
plot(basementsqft~logerror,set) #변동성 적음 (90232) => 0처리(없다고 가정)
properties$basementsqft[is.na(properties$basementsqft)] <- 0

#calcul이랑 모두 하위 개념 (6,12,13,15) - cor 1 => 여부로 바꾸는게 좋을듯
plot(calculatedfinishedsquarefeet~logerror,set) #피라미드꼴(661)
plot(finishedsquarefeet6~logerror,set) #Base unfinished and finished area (89854) #대부분 결측, 거의 1자
plot(finishedsquarefeet12~logerror,set) #Finished living area 피라미드꼴(4679)
plot(finishedsquarefeet13~logerror,set) #Perimeter  living area (90242) #대부분 결측, 1자임
plot(finishedsquarefeet15~logerror,set) #Total area             (86711) #대부분 결측, 피라미드 구조
cor(properties[,c(12,17)],use ="complete.obs")
cor(properties[,c(12,13)],use ="complete.obs")
cor(properties[,c(12,14)],use ="complete.obs")
cor(properties[,c(12,15)],use ="complete.obs")
properties$finishedsquarefeet6[!is.na(properties$finishedsquarefeet6)] <- 1
properties$finishedsquarefeet6[is.na(properties$finishedsquarefeet6)] <- 0
properties$finishedsquarefeet6 <- as.factor(properties$finishedsquarefeet6)

properties$finishedsquarefeet12[!is.na(properties$finishedsquarefeet12)] <- 1
properties$finishedsquarefeet12[is.na(properties$finishedsquarefeet12)] <- 0
properties$finishedsquarefeet12 <- as.factor(properties$finishedsquarefeet12)

properties$finishedsquarefeet13[!is.na(properties$finishedsquarefeet13)] <- 1
properties$finishedsquarefeet13[is.na(properties$finishedsquarefeet13)] <- 0
properties$finishedsquarefeet13 <- as.factor(properties$finishedsquarefeet13)

properties$finishedsquarefeet15[!is.na(properties$finishedsquarefeet15)] <- 1
properties$finishedsquarefeet15[is.na(properties$finishedsquarefeet15)] <- 0
properties$finishedsquarefeet15 <- as.factor(properties$finishedsquarefeet15)

plot(finishedfloor1squarefeet~logerror,set) # 거의 1자임 (물방울?)- (83419) 
plot(finishedsquarefeet50~logerror,set) #  Size of the finished living area on the first (entry) floor of the home (83419) #대부분 결측 1자 물방울
cor(properties[,c(11,16)],use ="complete.obs")
properties$finishedfloor1squarefeet[is.na(properties$finishedfloor1squarefeet)] <- 0
properties <- subset(properties, select= -c(finishedsquarefeet50))

#garagecar cnt => 없으면 평방미터도 0임 => 결측값은 -999로 통일
boxplot(logerror ~ addNA(garagecarcnt), set) 
plot(garagecarcnt~logerror,set) # 대부분결측(60338) #피라미드 구조 
plot(garagetotalsqft~logerror,set) # 대부분결측(60338)  #피라미드 구조
properties$garagecarcnt[is.na(properties$garagecarcnt)] <- -999
properties$garagetotalsqft[is.na(properties$garagetotalsqft)] <- -999


#summary(properties$fireplaceflag) ,nrow(properties[!is.na(properties$fireplacecnt),]) #왜 벽난로여부랑, 갯수랑 안맞을까?
plot(fireplacecnt~logerror,set) # 대부분결측(80668) #피라미드 구조 #벽난로 갯수 결측값은 0으로 
properties$fireplacecnt[is.na(properties$fireplacecnt)] <- 0

#수영장 관련변수(대부분 무의미하긴 함)
summary(properties[,28:32])
summary(properties[is.na(properties$poolcnt)]$poolsizesum)
plot(poolsizesum~logerror,set) #대부분 결측 (89306) #거의 1자
properties$poolsizesum[is.na(properties$poolcnt)] <- 0
properties$poolcnt[is.na(properties$poolcnt)] <- 0

#마당, 저장고 야적장 => 결측은 0으로 추정 
summary(properties[,46:47])
cor(properties[,c(46:47)],use ="complete.obs")
which(colnames(properties) == "yardbuildingsqft26")
plot(yardbuildingsqft17~logerror,set) #거의1자 물방울...(87629) 마당안뜰
plot(yardbuildingsqft26~logerror,set) #거의1자...(90180) 저장고/야적장
properties$yardbuildingsqft17[is.na(properties$yardbuildingsqft17)] <- 0
properties$yardbuildingsqft26[is.na(properties$yardbuildingsqft26)] <- 0


#plot(regionidneighborhood~logerror,set) # (54263) #대부분 비슷함  -> 부동신 위치동네임 (필요없을것으로 사료)
#summary(as.factor(properties$regionidneighborhood))

plot(unitcnt~logerror,set) #피라미드...(31922)
plot(numberofstories~logerror,set) #69705, 1,2,3,4로 있음..
plot(lotsizesquarefeet~logerror,set) #피라미드 구조(10150) 미스테리 
properties$unitcnt[is.na(properties$unitcnt)] <- 0
properties$numberofstories[is.na(properties$numberofstories)] <- 0
properties$lotsizesquarefeet[is.na(properties$lotsizesquarefeet)] <- 0

summary(set[is.na(set$calculatedbathnbr),]$bathroomcnt)
plot(threequarterbathnbr~logerror,set) #(78266),피라미드... 데이터가 나머지는 적음 (샤워+세면대+샤워실) => 1부터 있으니 없는건 0 으로 추정
properties$threequarterbathnbr[is.na(properties$threequarterbathnbr)] <- 0
plot(fullbathcnt~logerror,set) # 피라미드 구조 (1182) => 1165개는 화장실이 없어서 결측치임 (17개로 줄어듬)
plot(calculatedbathnbr~logerror, tr) #피라미드꼴 (1182) => 1165개는 화장실이 없어서 결측치임 (17개로 줄어듬)
properties$calculatedbathnbr[properties$bathroomcnt==0] <- 0
properties$fullbathcnt[properties$bathroomcnt==0] <- 0

plot(yearbuilt~logerror,set) #756, 옛날일 수록 오차가 적고, 나머지는 그냥 그럼
boxplot(logerror ~ addNA(yearbuilt), set) #중앙값 처리가 좋을듯
properties$yearbuilt[is.na(properties$yearbuilt)] <- median(properties$yearbuilt, na.rm=T)

#미납이 결측이라고 생각
plot(taxdelinquencyyear~logerror,set)#미납 된 재산세 납부시기: 역피라미드꼴(88492) (6~15, 99, 결측)
max(properties[properties$taxdelinquencyyear<50,]$taxdelinquencyyear)
properties$taxdelinquencyyear[properties$taxdelinquencyyear>50] <- 0
properties$taxdelinquencyyear[is.na(properties$taxdelinquencyyear)] <- 0

summary(properties)
#99% no match data process
summary(properties[is.na(properties$roomcnt),]) #propertyzoningdesc가 있는 것들, regionidcounty가 3101인 것들은 roomcnt = 0으로 처리
properties <- as.data.frame(properties)
for(i in c(2:which(colnames(properties)=="roomcnt")-1, (which(colnames(properties)=="roomcnt")+1):ncol(properties))) {
  if(is.numeric(properties[,i])) {
    properties[,i][is.na(properties$roomcnt)] <- median(unlist(properties[,i]), na.rm = T)
  }
}

for(i in c(2:which(colnames(properties)=="roomcnt")-1, (which(colnames(properties)=="roomcnt")+1):ncol(properties))) {
  if(is.factor(properties[,i])) {
    properties[,i] <- as.character(properties[,i])
    properties[,i][is.na(properties$roomcnt)] <- "na"  
    properties[,i] <- as.factor(properties[,i])
  }
}
properties$roomcnt[is.na(properties$roomcnt)] <- median(properties$roomcnt, na.rm = T)

#결측치가 적은 데이터는 예측값으로 대체함 (상관관계가 높은 값들이 많음)
cor(as.matrix(subset(set, select = c( taxamount, landtaxvaluedollarcnt, taxvaluedollarcnt, structuretaxvaluedollarcnt))), use = "complete.obs")
plot(calculatedfinishedsquarefeet~logerror,set) #피라미드꼴(661)
plot(structuretaxvaluedollarcnt~logerror,set)#피라미드꼴(380)
plot(taxvaluedollarcnt~logerror,set)#피라미드꼴(1)
plot(landtaxvaluedollarcnt~logerror,set)#피라미드꼴(1)
plot(taxamount~logerror,set) #피라미드꼴.. tax가 작을 수록 변동성이 큼  (6)




library(DMwR)
imp <- knnImputation(subset(properties, select = c(calculatedbathnbr, calculatedfinishedsquarefeet,fullbathcnt,poolsizesum,
                                                   taxamount, landtaxvaluedollarcnt, taxvaluedollarcnt, structuretaxvaluedollarcnt)))



real_set <- merge(train, properties, by="parcelid", all.x = T) 