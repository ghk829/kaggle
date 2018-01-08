#########################################
# 주제: 집값예측
# 최종수정일: 2017.06.26
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
train <- fread("train_2016_v2.csv",header=T)  #거래가 있던 정보들 => 한번에 여러개인건 어떻게 처리? 방조건은 안달라짐
properties <- fread("properties_2016.csv",header=T)
sub <- fread("sample_submission.csv",header=T)
#str(train)
#str(properties)
#str(sub)
#summary(as.factor(train$transactiondate))
#summary(as.factor(train$parcelid))
#summary(as.factor(properties$parcelid))
#train[train$parcelid=="11842707",]
#properties[properties$parcelid=="11842707",]
#sub[sub$ParcelId=="11842707",]

#length(unique(as.factor(train$parcelid))) #90150 -> logerror가 없는 구역id도 있음, 이는 유사한 logerror로 예측해야함
#length(unique(as.factor(properties$parcelid))) #2985217
#length(unique(as.factor(sub$ParcelId))) #2985217

str(properties)
#data 컬럼별 타입 변환
properties$rawcensustractandblock <- as.factor(properties$rawcensustractandblock)
properties$censustractandblock <- as.factor(properties$censustractandblock)
properties$regionidzip <- as.factor(properties$regionidzip)
properties$regionidcounty <- as.factor(properties$regionidcounty)
properties$regionidcity <- as.factor(properties$regionidcity) #1803개 결측
#properties$airconditioningtypeid <- as.factor(properties$airconditioningtypeid)
#properties$architecturalstyletypeid <- as.factor(properties$architecturalstyletypeid)
#properties$buildingqualitytypeid <- as.factor(properties$buildingqualitytypeid)
properties$fips <- as.factor(properties$fips)# Federal Information Processing Standard code
#properties$heatingorsystemtypeid <- as.factor(properties$heatingorsystemtypeid)
properties$propertycountylandusecode <- as.factor(properties$propertycountylandusecode) #코드가 너무 다양 (1)
properties$propertyzoningdesc <- as.factor(properties$propertyzoningdesc)             # 코드가 너무 다양(31962)
properties$propertylandusetypeid <- as.factor(properties$propertylandusetypeid) #결측 x
#properties$typeconstructiontypeid <- as.factor(properties$typeconstructiontypeid)

properties$hashottuborspa <- as.factor(properties$hashottuborspa) #스파여부
properties$fireplaceflag <- as.factor(properties$fireplaceflag) 
properties$taxdelinquencyflag <- as.factor(properties$taxdelinquencyflag) 
#위경도 로그변환
properties$latitude <- log(properties$latitude)
properties$longitude <- log(abs(properties$longitude))

#필요없는 컬럼 제거
properties <- subset(properties,select=c(-assessmentyear))
str(properties)
summary(properties$airconditioningtypeid)


#단일값과 결측값 관계 -> 단일값일때는 log가 안정적이지만, na일때 커지는 것을 확인할 수 있음 (약 9만건) , 차 후 logical로 할지 고민
set <- merge(train, properties, by="parcelid", all.x = T)

boxplot(logerror ~ addNA(storytypeid), set) 
#수영장 관련 
boxplot(logerror ~ addNA(pooltypeid2), set) #32075개 값
boxplot(logerror ~ addNA(pooltypeid10), set) #36941개 값

boxplot(logerror ~ addNA(poolcnt), set) #결측값은 0이라는 의미로 보임, 큰의미가 x로 보임 
boxplot(logerror ~ addNA(pooltypeid7), set) #두개가 비슷함
#
boxplot(logerror ~ addNA(decktypeid), set)
boxplot(logerror ~ addNA(buildingclasstypeid), set)

set$storytypeid[is.na(set$storytypeid)] <- "na"
set$storytypeid <- as.factor(set$storytypeid)
set$pooltypeid2[is.na(set$pooltypeid2)] <- "na"
set$pooltypeid2 <- as.factor(set$pooltypeid2)
set$pooltypeid10[is.na(set$pooltypeid10)] <- "na"
set$pooltypeid10 <- as.factor(set$pooltypeid10)
set$decktypeid[is.na(set$decktypeid)] <- "na"
set$decktypeid <- as.factor(set$decktypeid)
set$buildingclasstypeid[is.na(set$buildingclasstypeid)] <- "na"
set$buildingclasstypeid <- as.factor(set$buildingclasstypeid)

#유의함(결측과 공백 -> 여부에 따라서)
boxplot(logerror ~ addNA(hashottuborspa), set) #true or 공백 (87910)
boxplot(logerror ~ addNA(fireplaceflag), set) #true 222, 공백 90053
boxplot(logerror ~ addNA(taxdelinquencyflag), set)  #Y 1883, 88492


#필요없는 컬럼 제거
set <- subset(set,select=c(-poolcnt, -pooltypeid7))
str(set)
#
boxplot(logerror ~ addNA(airconditioningtypeid), set) #결측값과 1 타입이 변동성이 큼 (61494)
boxplot(logerror ~ addNA(architecturalstyletypeid), set) #결측값 외에는 일정한 편 (90014)
boxplot(logerror ~ addNA(buildingqualitytypeid), set) #1,4,7,10,결측 type (32911)
boxplot(logerror ~ addNA(fips), set)  #결측x, 3개 종류가 있음 
boxplot(logerror ~ addNA(heatingorsystemtypeid), set) # 결측(34195) 다양함
boxplot(logerror ~ addNA(propertylandusetypeid), set) #결측x, 14종류 
boxplot(logerror ~ addNA(typeconstructiontypeid), set) #결측 89976 (4,6,13으로 6만 296 나머지는 2,1개..)
#
set$airconditioningtypeid[is.na(set$airconditioningtypeid)] <- "na"
set$airconditioningtypeid <- as.factor(set$airconditioningtypeid)
set$architecturalstyletypeid[is.na(set$architecturalstyletypeid)] <- "na"
set$architecturalstyletypeid <- as.factor(set$architecturalstyletypeid)
set$buildingqualitytypeid[is.na(set$buildingqualitytypeid)] <- "na"
set$buildingqualitytypeid <- as.factor(set$buildingqualitytypeid)
set$heatingorsystemtypeid[is.na(set$heatingorsystemtypeid)] <- "na"
set$heatingorsystemtypeid <- as.factor(set$heatingorsystemtypeid)
set$typeconstructiontypeid[is.na(set$typeconstructiontypeid)] <- "na"
set$typeconstructiontypeid <- as.factor(set$typeconstructiontypeid)


#수치형 변수
#이상값 결측값 처리 필요 => 데이터에 대한 이해가 동반이 되야함. 논리적인 처리필요

plot(bathroomcnt~logerror,set) #피라미드꼴.. (결측x)
plot(bedroomcnt~logerror,set) #피라미드꼴 (결측x)

plot(roomcnt~logerror,set) #방 0개인것만 에러가 다양함, 나머지는 비슷 (결측x)
summary(set[set$roomcnt == 0 ,]) #방이 0개인게 69700개 (70%): 주거지에 있는 방의 총 갯수임 
#방이 0개인데 화장실, 침실 갯수가 있음... ??
#해당 부동산에 대해 허용 된 토지 용도 (구역 설정)에 대한 설명 (propertyzoningdesc)
summary(as.factor(as.character(set[set$roomcnt == 0 ,]$propertyzoningdesc)))
summary(as.factor(as.character(set[set$roomcnt > 0 ,]$propertyzoningdesc)))
#LARE40 구역 지정 코드는 4,000 s.f마다 1 개의 집을 둘 수 있음을 의미 => 부동산 토지용도 코드 공부도 도움이 될 듯
#실제 예측시, roomcnt가 결측인경우가 종종 있음=> 실제 예측에서 2개의 모델로 분석도 가능하다고는 생각함
set$room_yn <- 0
set$room_yn[set$roomcnt > 0 ] <- 1
set$room_yn <- as.factor(set$room_yn)
boxplot(logerror ~ addNA(room_yn), set)


r0 <- summary(set[set$roomcnt == 0 ,])
r1 <- summary(set[set$roomcnt > 0 ,])
properties
properties[properties$propertyzoningdesc != "" &properties$roomcnt > 0, ] # train, test에 1개씩 값이 존재
set[set$propertyzoningdesc != "" &set$roomcnt > 0, ] #이상값으로 판단
set$propertyzoningdesc[set$propertyzoningdesc != "" & set$roomcnt > 0]  <- ""


for(i in 4:ncol(set)) {
print(colnames(set)[i])
print(data.frame(r0[,i], r1[,i]))
print("---------------------------------")
}

#regionidcounty(부동산위치가 방이 0 개인데는 3101에 다 있고, 3101에는 없음)
#typeconstructiontypeid, fireplaceflag 는 방 1개 이상인 곳만 있음
summary(as.factor(properties[properties$roomcnt == 0, ]$typeconstructiontypeid ))
properties$typeconstructiontypeid[properties$roomcnt == 0 & properties$typeconstructiontypeid =="11" ] <- NA
summary(as.factor(properties[properties$roomcnt == 0, ]$fireplaceflag )) #위에 이상값에 포함됨 => 수정요함
properties$fireplaceflag[properties$roomcnt == 0 & properties$fireplaceflag != "" ] <- ""

summary(properties[is.na(properties$roomcnt),]) #propertyzoningdesc가 있는 것들, regionidcounty가 3101인 것들은 roomcnt = 0으로 처리
#11437개는 거의 매칭되는게 없음 

#결측값에 대한 고민을 해야함
plot(basementsqft~logerror,set) #변동성 적음 (90232) => 제거?
plot(finishedfloor1squarefeet~logerror,set) # 거의 1자임 (물방울?)- (83419) 

plot(finishedsquarefeet12~logerror,set) #Finished living area 피라미드꼴(4679)
plot(finishedsquarefeet13~logerror,set) #Perimeter  living area (90242) #대부분 결측, 1자임
plot(finishedsquarefeet15~logerror,set) #Total area             (86711) #대부분 결측, 피라미드 구조
plot(finishedsquarefeet50~logerror,set) #  Size of the finished living area on the first (entry) floor of the home (83419) #대부분 결측 1자 물방울
plot(finishedsquarefeet6~logerror,set) #Base unfinished and finished area (89854) #대부분 결측, 거의 1자
plot(fireplacecnt~logerror,set) # 대부분결측(80668) #피라미드 구조 

#garagecar cnt
boxplot(logerror ~ addNA(garagecarcnt), set) 
plot(garagecarcnt~logerror,set) # 대부분결측(60338) #피라미드 구조 
plot(garagetotalsqft~logerror,set) # 대부분결측(60338)  #피라미드 구조
#
plot(lotsizesquarefeet~logerror,set) #피라미드 구조(10150)
plot(poolsizesum~logerror,set) #대부분 결측 (89306) #거의 1자
plot(regionidneighborhood~logerror,set) # (54263) #대부분 비슷함 
plot(threequarterbathnbr~logerror,set) #(78266),피라미드... 데이터가 나머지는 적음 
plot(unitcnt~logerror,set) #피라미드...(31922)
plot(yardbuildingsqft17~logerror,set) #거의1자 물방울...(87629)
plot(yardbuildingsqft26~logerror,set) #거의1자...(90180)
plot(yearbuilt~logerror,set) #756, 옛날일 수록 오차가 적고, 나머지는 그냥 그럼
plot(numberofstories~logerror,set) #69705, 1,2,3,4로 있음..





#결측치가 적은 데이터는 예측값으로 대체함 (상관관계가 높은 값들이 많음)
summary(set[set$bathroomcnt==0,]$calculatedbathnbr)
summary(set[is.na(set$calculatedbathnbr),]$bathroomcnt)
plot(fullbathcnt~logerror,set) # 피라미드 구조 (1182) => 1165개는 화장실이 없어서 결측치임 (17개로 줄어듬)
plot(calculatedbathnbr~logerror, tr) #피라미드꼴 (1182) => 1165개는 화장실이 없어서 결측치임 (17개로 줄어듬)
set$calculatedbathnbr[set$bathroomcnt==0] <- 0
set$fullbathcnt[set$bathroomcnt==0] <- 0

plot(calculatedfinishedsquarefeet~logerror,set) #피라미드꼴(661)
plot(structuretaxvaluedollarcnt~logerror,set)#피라미드꼴(380)
plot(taxvaluedollarcnt~logerror,set)#피라미드꼴(1)
plot(landtaxvaluedollarcnt~logerror,set)#피라미드꼴(1)
plot(taxamount~logerror,set) #피라미드꼴.. tax가 작을 수록 변동성이 큼  (6)
set[is.na(set$landtaxvaluedollarcnt),]$taxamount

cor(as.matrix(subset(set, select = c( taxamount, landtaxvaluedollarcnt, taxvaluedollarcnt, structuretaxvaluedollarcnt, 
                                      roomcnt, bedroomcnt, bathroomcnt, calculatedbathnbr, calculatedfinishedsquarefeet
))), use = "complete.obs")


plot(taxdelinquencyyear~logerror,set)#미납 된 재산세 납부시기: 역피라미드꼴(88492) (6~15, 99, 결측)
#미납이 안됬다면 결측이라고 생각
max(set[set$taxdelinquencyyear<50,]$taxdelinquencyyear)
set$taxdelinquencyyear[set$taxdelinquencyyear>50] <- 0
set$taxdelinquencyyear[is.na(set$taxdelinquencyyear)] <- 0
