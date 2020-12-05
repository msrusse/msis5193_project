#Read in the data files
movies_data <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\movies_data_combined.csv', header = TRUE)
#Add the month of release in
month_data <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\movies_by_year_month_market.csv', header = TRUE)
movies_data <- merge(movies_data, month_data, all.x = TRUE, by = c('uniqueID'))

#Remove non numerical data
movies_data <- movies_data[ -c(1,2,14,15) ]
movies_data$domesticTotal <- as.numeric(as.character(movies_data$domesticTotal))
movies_data$foreignTotal <- as.numeric(as.character(movies_data$foreignTotal))
movies_data$domesticPercent <- as.numeric(as.character(movies_data$domesticPercent))
movies_data$foreignPercent <- as.numeric(as.character(movies_data$foreignPercent))
movies_data$totalAudienceReviews <- as.numeric(as.character(movies_data$totalAudienceReviews))
movies_data$runtime <- as.numeric(as.character(movies_data$runtime))

#Split the data be decade
movies_data_70s = movies_data[movies_data$year < '1980',]
movies_data_80s = movies_data[movies_data$year > '1979',]
movies_data_80s = movies_data_80s[movies_data_80s$year < '1990',]
movies_data_90s = movies_data[movies_data$year > '1989',]
movies_data_90s = movies_data_90s[movies_data_90s$year < '2000',]
movies_data_00s = movies_data[movies_data$year > '1999',]
movies_data_00s = movies_data_00s[movies_data_00s$year < '2010',]
movies_data_10s = movies_data[movies_data$year > '2009',]
movies_data_10s = movies_data_10s[movies_data_10s$year < '2020',]

#Find basic stats on the 70s
summary_70s = data.frame(colnames(movies_data))
colnames(summary_70s) <- c('variable')
#Mean
mean_70s = data.frame(colMeans(movies_data_70s, na.rm = TRUE))
#Median
median_70s = data.frame(apply(movies_data_70s,2,median,na.rm=TRUE))
#Standard Deviation
sd_70s = data.frame(apply(movies_data_70s,2,sd,na.rm=TRUE))
#Max
max_70s = data.frame(apply(movies_data_70s,2,max,na.rm=TRUE))
#Min
min_70s = data.frame(apply(movies_data_70s,2,min,na.rm=TRUE))
#combine the data
summary_70s["mean"] <- mean_70s
summary_70s["median"] <- median_70s
summary_70s["sd"] <- sd_70s
summary_70s["max"] <- max_70s
summary_70s["min"] <- min_70s

#Find basic stats on the 80s
summary_80s = data.frame(colnames(movies_data))
colnames(summary_80s) <- c('variable')
#Mean
mean_80s = data.frame(colMeans(movies_data_80s, na.rm = TRUE))
#Median
median_80s = data.frame(apply(movies_data_80s,2,median,na.rm=TRUE))
#Standard Deviation
sd_80s = data.frame(apply(movies_data_80s,2,sd,na.rm=TRUE))
#Max
max_80s = data.frame(apply(movies_data_80s,2,max,na.rm=TRUE))
#Min
min_80s = data.frame(apply(movies_data_80s,2,min,na.rm=TRUE))
#combine the data
summary_80s["mean"] <- mean_80s
summary_80s["median"] <- median_80s
summary_80s["sd"] <- sd_80s
summary_80s["max"] <- max_80s
summary_80s["min"] <- min_80s

#Find basic stats on the 90s
summary_90s = data.frame(colnames(movies_data))
colnames(summary_90s) <- c('variable')
#Mean
mean_90s = data.frame(colMeans(movies_data_90s, na.rm = TRUE))
#Median
median_90s = data.frame(apply(movies_data_90s,2,median,na.rm=TRUE))
#Standard Deviation
sd_90s = data.frame(apply(movies_data_90s,2,sd,na.rm=TRUE))
#Max
max_90s = data.frame(apply(movies_data_90s,2,max,na.rm=TRUE))
#Min
min_90s = data.frame(apply(movies_data_90s,2,min,na.rm=TRUE))
#combine the data
summary_90s["mean"] <- mean_90s
summary_90s["median"] <- median_90s
summary_90s["sd"] <- sd_90s
summary_90s["max"] <- max_90s
summary_90s["min"] <- min_90s

#Find basic stats on the 00s
summary_00s = data.frame(colnames(movies_data))
colnames(summary_00s) <- c('variable')
#Mean
mean_00s = data.frame(colMeans(movies_data_00s, na.rm = TRUE))
#Median
median_00s = data.frame(apply(movies_data_00s,2,median,na.rm=TRUE))
#Standard Deviation
sd_00s = data.frame(apply(movies_data_00s,2,sd,na.rm=TRUE))
#Max
max_00s = data.frame(apply(movies_data_00s,2,max,na.rm=TRUE))
#Min
min_00s = data.frame(apply(movies_data_00s,2,min,na.rm=TRUE))
#combine the data
summary_00s["mean"] <- mean_00s
summary_00s["median"] <- median_00s
summary_00s["sd"] <- sd_00s
summary_00s["max"] <- max_00s
summary_00s["min"] <- min_00s

#Find basic stats on the 10s
summary_10s = data.frame(colnames(movies_data))
colnames(summary_10s) <- c('variable')
#Mean
mean_10s = data.frame(colMeans(movies_data_10s, na.rm = TRUE))
#Median
median_10s = data.frame(apply(movies_data_10s,2,median,na.rm=TRUE))
#Standard Deviation
sd_10s = data.frame(apply(movies_data_10s,2,sd,na.rm=TRUE))
#Max
max_10s = data.frame(apply(movies_data_10s,2,max,na.rm=TRUE))
#Min
min_10s = data.frame(apply(movies_data_10s,2,min,na.rm=TRUE))
#combine the data
summary_10s["mean"] <- mean_10s
summary_10s["median"] <- median_10s
summary_10s["sd"] <- sd_10s
summary_10s["max"] <- max_10s
summary_10s["min"] <- min_10s

#Export the summary data
write.csv(summary_70s,'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\summary_70s.csv', row.names = FALSE)
write.csv(summary_80s,'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\summary_80s.csv', row.names = FALSE)
write.csv(summary_90s,'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\summary_90s.csv', row.names = FALSE)
write.csv(summary_00s,'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\summary_00s.csv', row.names = FALSE)
write.csv(summary_10s,'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\summary_10s.csv', row.names = FALSE)


#set up a multiple regression
model <- lm(worldwideTotal ~ monthNumber + runtime + nominations + awards  + bestPicture + foreignRelease + contentRating + totalAudienceReviews + audienceReviewScore + totalCriticsReviews + criticsReviewScore + fantasy + adventure + sci.fi + action + comedy + kids.and.family + drama + horror + animation + crime + mystery.and.trhiller + musical + documentary + sports.and.fitness + anime + foreign + famousActors, data = movies_data_10s)
summary(model)

#Which genre is best
genres = data.frame(colnames(movies_data_10s))
genres = data.frame(genres[-c(1:16, 40:42), ])
genres[,'averageboxOffice'] <- NA
for (i in 1:nrow(genres)){
  c = i + 16
  test_movie = data.frame(movies_data_10s[,c(6, c)])
  test_movie = test_movie[test_movie[,2] == 1,]
  average = mean(test_movie[,1])
  genres[i,2] = average
}
colnames(genres) <- c('genre', 'worldwideboxOffice')
genres = genres[order(genres$worldwideboxOffice, decreasing = TRUE),] 
genres = data.frame(genres[-c(9:40), ])
#make a bar chart
library(ggplot2)
ggplot(data=genres, aes(x = reorder(genre, -worldwideboxOffice), y=worldwideboxOffice)) +
  geom_bar(stat="identity", fill="steelblue")+
  theme_minimal()


#Do famous actors help
famousCount = data.frame(movies_data_10s$famousActors)
famousCount <- unique(famousCount)
colnames(famousCount) <- c('famousCount')
famousCount[,'averageboxOffice'] <- NA
for (i in 1:nrow(famousCount)){
  count = famousCount[i,1]
  test_movie1 = data.frame(movies_data_10s[,c(6, 40)])
  test_movie1 = test_movie1[test_movie1[,2] == count,]
  average = mean(test_movie1[,1])
  famousCount[i,2] = average
}
#make a bar chart
ggplot(data=famousCount, aes(x = reorder(famousCount, -averageboxOffice), y=averageboxOffice)) +
  geom_bar(stat="identity", fill="steelblue")+
  theme_minimal()


#Critic vs audience review
#make the data set smaller to see the trend better
movies_data_10s1 = movies_data_10s[movies_data_10s$worldwideTotal > 100000000,]
#audience
ggplot(movies_data_10s1, aes(x=audienceReviewScore, y=worldwideTotal)) + 
  geom_point(shape=18, color="blue")+
  geom_smooth(method=lm,  linetype="dashed",
              color="darkred", fill="blue")+
  theme_minimal()
#critics
ggplot(movies_data_10s1, aes(x=criticsReviewScore, y=worldwideTotal)) + 
  geom_point(shape=18, color="dark blue")+
  geom_smooth(method=lm,  linetype="dashed",
              color="darkred", fill="blue")+
  theme_minimal()


#content rating
content_ratings_data = data.frame(movies_data_10s[movies_data_10s$contentRating > 0,])
content_ratings_data$contentRating[content_ratings_data$contentRating == 6] <- 'NR'
content_ratings_data$contentRating[content_ratings_data$contentRating == 1] <- 'G'
content_ratings_data$contentRating[content_ratings_data$contentRating == 2] <- 'PG'
content_ratings_data$contentRating[content_ratings_data$contentRating == 3] <- 'PG-13'
content_ratings_data$contentRating[content_ratings_data$contentRating == 4] <- 'NC17'
content_ratings_data$contentRating[content_ratings_data$contentRating == 5] <- 'R'
ratings = data.frame(content_ratings_data$contentRating)
ratings <- unique(ratings)
colnames(ratings) <- c('contentRating')
ratings[,'averageboxOffice'] <- NA
for (i in 1:nrow(ratings)){
  rating = ratings[i,1]
  test_movie2 = data.frame(content_ratings_data[,c(6, 12)])
  test_movie2 = test_movie2[test_movie2[,2] == rating,]
  average = mean(test_movie2[,1])
  ratings[i,2] = average
}
#make a bar chart
ggplot(data=ratings, aes(x = reorder(contentRating, -averageboxOffice), y=averageboxOffice)) +
  geom_bar(stat="identity", fill="steelblue")+
  theme_minimal()


#Month analysis
months = data.frame(movies_data_10s$month)
months <- unique(months)
colnames(months) <- c('month')
months <- na.omit(months) 
months[,'averageboxOffice'] <- NA
for (i in 1:nrow(months)){
  count = months[i,1]
  test_movie1 = data.frame(movies_data_10s[,c(6, 42)])
  test_movie1 = test_movie1[test_movie1[,2] == count,]
  test_movie1 = na.omit(test_movie1)
  average = mean(test_movie1[,1])
  months[i,2] = average
}
#make a bar chart
ggplot(data=months, aes(x = reorder(month, -averageboxOffice), y=averageboxOffice)) +
  geom_bar(stat="identity", fill="steelblue")+
  theme_minimal()


#Runtime analysis
#make the data set smaller to see the trend better
movies_data_10s2 = movies_data_10s[movies_data_10s$runtime > 30,]
movies_data_10s2 = movies_data_10s2[movies_data_10s2$runtime < 300,]
ggplot(movies_data_10s2, aes(x=runtime, y=worldwideTotal)) + 
  geom_point(shape=18, color="dark blue")+
  geom_smooth()+
  theme_minimal()

#Awards analysis
awards = data.frame(movies_data_10s$awards)
awards <- unique(awards)
colnames(awards) <- c('totalAwards')
awards[,'averageboxOffice'] <- NA
for (i in 1:nrow(awards)){
  count = awards[i,1]
  test_movie1 = data.frame(movies_data_10s[,c(3,6)])
  test_movie1 = test_movie1[test_movie1[,1] == count,]
  average = mean(test_movie1[,2])
  awards[i,2] = average
}
#make a bar chart
ggplot(data=awards, aes(x = reorder(totalAwards, -averageboxOffice), y=averageboxOffice)) +
  geom_bar(stat="identity", fill="steelblue")+
  theme_minimal()
