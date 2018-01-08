
library(reshape2)
library(data.table)
library(ggplot2)
library(dplyr)
library(caret)
library(e1071)
library(class)
library(xgboost)
library(Matrix)
library(Metrics)
library(DiagrammeR)

setwd("C:/Users/il-geun/Desktop/zillow")
p2016 <- fread("properties1.csv",header=T, stringsAsFactors = T)
p2017 <- fread("properties2.csv",header=T, stringsAsFactors = T)

train1 <- fread("train_2016_v2.csv",header=T)  #거래가 있던 정보들 => 한번에 여러개인건 어떻게 처리? 방조건은 안달라짐
train2 <- fread("train_2017.csv",header=T)
train <- rbind(train1, train2)

sub <- fread("sample_submission.csv",header=T)
train$year <- as.factor(substr(train$transactiondate,1,4))
train$month <- as.factor(as.numeric(substr(train$transactiondate,6,7)))

train1$month <- as.factor(as.numeric(substr(train1$transactiondate,6,7)))
train2$month <- as.factor(as.numeric(substr(train2$transactiondate,6,7)))
#train에 있는 결과값은 모두 sub에 넣기 
colnames(train)[1] <- "ParcelId"
sub <- merge(sub, subset(train[train$year=="2016" & train$month == "10",], select = c("ParcelId", "logerror") ), by = "ParcelId", all.x = T)
colnames(sub)[ncol(sub)] <- "log201610"
sub <- merge(sub, subset(train[train$year=="2016" & train$month == "11",], select = c("ParcelId", "logerror") ), by = "ParcelId", all.x = T)
colnames(sub)[ncol(sub)] <- "log201611"
sub <- merge(sub, subset(train[train$year=="2016" & train$month == "12",], select = c("ParcelId", "logerror") ), by = "ParcelId", all.x = T)
colnames(sub)[ncol(sub)] <- "log201612"

train2016 <- merge(train1, p2016, by="parcelid", all.x = T)
train2017 <- merge(train2, p2017, by="parcelid", all.x = T)

train_set <- rbind(train2016, train2017)
train_set$year <- as.factor(substr(train_set$transactiondate,1,4))


set.seed(1004)
train2016 <- train2016[sample(nrow(train2016)),]

train2016 <- subset(train2016, select = -c(rawcensustractandblock, censustractandblock))
set.seed(1004)
ind <- sample(x=2, nrow(train2016), replace=T, prob=c(0.7,0.3))
valid  <- as.data.frame(train2016[ind==2,]) 
train <- as.data.frame(train2016[ind==1,]) 

p2016$logerror <- 0

train.mx <- sparse.model.matrix(logerror~., train[,-c(1,3)])
valid.mx <- sparse.model.matrix(logerror~., valid[,-c(1,3)])
test.mx <- sparse.model.matrix(logerror~., p2016[,-c(1)])

dtrain <- xgb.DMatrix(train.mx, label=train$logerror)
dvalid <- xgb.DMatrix(valid.mx, label=valid$logerror)
dtest <- xgb.DMatrix(test.mx, label=p2016$logerror)

set.seed(1004)
train_xgb <- xgb.train(data = dtrain,
                       max_depth = 12, 
                       subsample = 0.7,
                       colsample_bytree = 0.7,
                       nthread = 1,
                       min_child_weight = 1,
                       eta = 0.1,
                       gamma = 0.9,
                       nrounds = 150, 
                       objective = "reg:linear",
                       nfold = 5,
                       alpha = 0.001, #l1 regul weight
                       lambda = 0.001, #l2 regul weight
                       early_stopping_rounds = 20,
                       eval_metric = "mae",
                       watchlist = list(train = dtrain, test = dvalid))

pred2016 <- data.frame(ParcelId = p2016$parcelid , pred = (predict(train_xgb,newdata=dtest)))

sub <- merge(sub, pred2016, by = "ParcelId")
sub$`201610` <- sub$pred
sub$`201611` <- sub$pred
sub$`201612` <- sub$pred

sub$`201610`[sub$ParcelId %in% sub[!is.na(sub$log201610),]$ParcelId] <- 0
sub$`201611`[sub$ParcelId %in% sub[!is.na(sub$log201611),]$ParcelId] <- 0
sub$`201612`[sub$ParcelId %in% sub[!is.na(sub$log201612),]$ParcelId] <- 0

sub$log201610[is.na(sub$log201610)] <- 0
sub$log201611[is.na(sub$log201611)] <- 0
sub$log201612[is.na(sub$log201612)] <- 0

sub$`201610` <- sub$`201610` + sub$log201610
sub$`201611` <- sub$`201611` + sub$log201611
sub$`201612` <- sub$`201612` + sub$log201612

sub <- subset(sub, select = -c(log201610, log201611, log201612, pred))
write.csv(sub, "sub_2016.csv", row.names= F)


#######################################################################################################
set.seed(1004)
train_set <- train_set[sample(nrow(train_set)),]

train_set <- subset(train_set, select = -c(rawcensustractandblock, censustractandblock))

set.seed(1004)
ind <- sample(x=2, nrow(train_set), replace=T, prob=c(0.7,0.3))
valid  <- as.data.frame(train_set[ind==2,]) 
train <- as.data.frame(train_set[ind==1,]) 

p2017$logerror <- 0

rm(train2017)

train.mx <- sparse.model.matrix(logerror~., train[,-c(1,3)])
valid.mx <- sparse.model.matrix(logerror~., valid[,-c(1,3)])
test.mx <- sparse.model.matrix(logerror~., p2017[,-c(1)])

dtrain <- xgb.DMatrix(train.mx, label=train$logerror)
dvalid <- xgb.DMatrix(valid.mx, label=valid$logerror)
dtest <- xgb.DMatrix(test.mx, label=p2017$logerror)

set.seed(1004)
train_xgb <- xgb.train(data = dtrain,
                       max_depth = 10, 
                       subsample = 0.7,
                       colsample_bytree = 0.7,
                       nthread = 1,
                       min_child_weight = 1,
                       eta = 0.1,
                       gamma = 0.9,
                       nrounds = 150, 
                       objective = "reg:linear",
                       nfold = 5,
                       alpha = 0.001, #l1 regul weight
                       lambda = 0.001, #l2 regul weight
                       early_stopping_rounds = 20,
                       eval_metric = "mae",
                       watchlist = list(train = dtrain, test = dvalid))

pred2017 <- data.frame(ParcelId = p2017$parcelid , pred = (predict(train_xgb,newdata=dtest)))

sub <- merge(sub, pred2017, by = "ParcelId")
sub$`201710` <- sub$pred
sub$`201711` <- sub$pred
sub$`201712` <- sub$pred
sub <- subset(sub, select = -c(pred))
summary(sub)
write.csv(sub, "xgb_sub3.csv", row.names = F)

sub$`201610` <- sub$`201610` - 1
sub$`201611` <- sub$`201611` - 1
sub$`201612` <- sub$`201612` - 1
sub$`201710` <- sub$`201710` - median(sub$`201710`)
sub$`201711` <- sub$`201711` - median(sub$`201711`)
sub$`201712` <- sub$`201712` - median(sub$`201712`)

summary(train2017$logerror)
summary(train2016$logerror)