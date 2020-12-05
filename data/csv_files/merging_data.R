#Read in the data files
movies_awards <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\academy_award_winning_movies.csv', header = TRUE)
movies_data <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\box_office_movies.csv', header = TRUE)

#Edit movies_awards to match movies_data
movies_awards[829,1] = 'Star Wars: Episode IV - A New Hope'
movies_awards[952,1] = 'Star Wars: Episode V - The Empire Strikes Back'
movies_awards[305,1] = 'E.T. the Extra-Terrestrial'
movies_awards[1255,1] = 'WALL·E'
movies_awards[735,1] =  'Star Wars: Episode VI - Return of the Jedi'
movies_awards[664,1] = 'Once Upon a Time... In Hollywood'
movies_awards[1016,2] = '2008'
movies_awards[142,1] = 'Birdman or (The Unexpected Virtue of Ignorance)'

 
#Merge the two file
movies_data <- merge(movies_awards, movies_data, all.y = TRUE, by = c('movieName','year'))

#Fill in movies with no awards
C
movies_data$awards[is.na(movies_data$awards)] <- 0
movies_data$bestPicture[is.na(movies_data$bestPicture)] <- 'False'
movies_data$bestPicture[movies_data$bestPicture == 'False'] <- 0
movies_data$bestPicture[movies_data$bestPicture == 'True'] <- 1

#Add foreign release
movies_data[,'foreignRelease'] <- NA
movies_data$foreignRelease[movies_data$foreignTotal > 0] <- 1
movies_data$foreignRelease[is.na(movies_data$foreignRelease)] <- 0

#Pull in the other files
movie_summaries <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\movie_summeries.csv', header = TRUE)
movie_actors <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\all_movie_actors.csv', header = TRUE)
#movie_genres <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\all_movie_genres.csv', header = TRUE)
movie_companies <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\all_movie_production_companies.csv', header = TRUE)
movie_ratings <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\all_movie_ratings.csv', header = TRUE)
movie_content_ratings <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\all_movie_content_ratings.csv', header = TRUE)
movie_directors <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\all_movie_directors.csv', header = TRUE)
movie_genres1 <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\movies_with_genre_bool.csv', header = TRUE)

#Merge the files
movies_data <- merge(movies_data, movie_summaries, all.x = TRUE, by = 'uniqueID')
movies_data <- merge(movies_data, movie_companies, all.x = TRUE, by = 'uniqueID')
movies_data <- merge(movies_data, movie_content_ratings, all.x = TRUE, by = 'uniqueID')
movies_data <- merge(movies_data, movie_ratings, all.x = TRUE, by = 'uniqueID')
movies_data <- merge(movies_data, movie_genres1, all.x = TRUE, by = 'uniqueID')

#Fix na in genre
movies_data$fantasy[is.na(movies_data$fantasy)] <- 0
movies_data$adventure[is.na(movies_data$adventure)] <- 0
movies_data$sci.fi[is.na(movies_data$sci.fi)] <- 0
movies_data$action[is.na(movies_data$action)] <- 0
movies_data$comedy[is.na(movies_data$comedy)] <- 0
movies_data$kids.and.family[is.na(movies_data$kids.and.family)] <- 0
movies_data$drama[is.na(movies_data$drama)] <- 0
movies_data$horror[is.na(movies_data$horror)] <- 0
movies_data$animation[is.na(movies_data$animation)] <- 0
movies_data$crime[is.na(movies_data$crime)] <- 0
movies_data$mystery.and.trhiller[is.na(movies_data$mystery.and.trhiller)] <- 0
movies_data$musical[is.na(movies_data$musical)] <- 0
movies_data$romance[is.na(movies_data$romance)] <- 0
movies_data$music[is.na(movies_data$music)] <- 0
movies_data$war[is.na(movies_data$war)] <- 0
movies_data$other[is.na(movies_data$other)] <- 0
movies_data$biography[is.na(movies_data$biography)] <- 0
movies_data$western[is.na(movies_data$western)] <- 0
movies_data$history[is.na(movies_data$history)] <- 0
movies_data$documentary[is.na(movies_data$documentary)] <- 0
movies_data$sports.and.fitness[is.na(movies_data$sports.and.fitness)] <- 0
movies_data$anime[is.na(movies_data$anime)] <- 0
movies_data$foreign[is.na(movies_data$foreign)] <- 0

#movie runtime to the end
library(dplyr)
movies_data = movies_data %>% relocate(runtime, .after = last_col())

#-------All of this is not used anymore due to a more effecient method--------
#Figure out movie genres
#movie_genres1 <- movie_genres[!(movie_genres$genre==""),]
#movie_genres1 <- unique(movie_genres1[c("genre")])
#for (i in 1:nrow(movie_genres1)){
#  movies_data[,movie_genres1[i,1]] <- NA
#}
#fantasy
#count = 0
#for (j in 1:nrow(movies_data)){
#id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'fantasy'){
#        count = count + 1
#      }
#    }
#  movies_data[j,21] = count
#  count = 0
#}
#adventure
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'adventure'){
#        count = count + 1
#      }
#    }
#  movies_data[j,22] = count
#  count = 0
#}   
#sci fi
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'sci fi'){
#        count = count + 1
#      }
#    }
#  movies_data[j,23] = count
#  count = 0
#} 
#action
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'action'){
#        count = count + 1
#      }
#    }
#  movies_data[j,24] = count
#  count = 0
#}     
#comedy
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'comedy'){
#        count = count + 1
#      }
#    }
#  movies_data[j,25] = count
#  count = 0
#}  
#kids and family
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'kids and family'){
#        count = count + 1
#      }
#    }
#  movies_data[j,26] = count
#  count = 0
#}  
#drama
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'drama'){
#        count = count + 1
#      }
#    }
#  movies_data[j,27] = count
#  count = 0
#}  
#horror
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'horror'){
#        count = count + 1
#      }
#    }
#  movies_data[j,28] = count
#  count = 0
#}  
#animation
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'animation'){
#        count = count + 1
#      }
#    }
#  movies_data[j,29] = count
#  count = 0
#}  
#crime
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'crime'){
#        count = count + 1
#      }
#    }
#  movies_data[j,30] = count
#  count = 0
#}  
#mystery and thriller
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'mystery and thriller'){
#        count = count + 1
#      }
#    }
#  movies_data[j,31] = count
#  count = 0
#}
##musical
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'musical'){
#        count = count + 1
#      }
#    }
#  movies_data[j,32] = count
#  count = 0
#}
#romance
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'romance'){
#        count = count + 1
#      }
#    }
#  movies_data[j,33] = count
#  count = 0
#}
##	music
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'music'){
#        count = count + 1
#      }
#    }
#  movies_data[j,34] = count
#  count = 0
#}
##	war
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'war'){
#        count = count + 1
#      }
#    }
#  movies_data[j,35] = count
#  count = 0
#}
##other
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'other'){
#        count = count + 1
#      }
#    }
#  movies_data[j,36] = count
#  count = 0
#}
#biography
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'biography'){
#        count = count + 1
#      }
#    }
#  movies_data[j,37] = count
#  count = 0
#}
#western
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'western'){
#        count = count + 1
#      }
#    }
#  movies_data[j,38] = count
#  count = 0
#}
#history
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'history'){
#        count = count + 1
#      }
#    }
#  movies_data[j,39] = count
#  count = 0
#}
##documentary
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'documentary'){
#        count = count + 1
#      }
#    }
#  movies_data[j,40] = count
#  count = 0
#}
##sports and fitness
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'sports and fitness'){
#        count = count + 1
#      }
#    }
#  movies_data[j,41] = count
#  count = 0
#}
##anime
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
# for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'anime'){
#        count = count + 1
#      }
#    }
#  movies_data[j,42] = count
#  count = 0
#}
##foreign
#count = 0
#for (j in 1:nrow(movies_data)){
#  id = movies_data[j,1]
#  for (k in 1:nrow(movie_genres))
#    if (movie_genres[k,1] == id) {
#      if (movie_genres[k,2] == 'foreign'){
#        count = count + 1
#      }
#    }
#  movies_data[j,43] = count
#  count = 0
#}
#--------------------------------------------------------------------------


#Add categories for content ratings
movies_data$contentRating[is.na(movies_data$contentRating)] <- 0
movies_data$contentRating[movies_data$contentRating == 'NR'] <- 6
movies_data$contentRating[movies_data$contentRating == 'G'] <- 1
movies_data$contentRating[movies_data$contentRating == 'PG'] <- 2
movies_data$contentRating[movies_data$contentRating == 'PG-13'] <- 3
movies_data$contentRating[movies_data$contentRating == 'NC17'] <- 4
movies_data$contentRating[movies_data$contentRating == 'R'] <- 5


#Add in famous actors
oscar_actors <- read.csv(file = 'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\oscar_actors.csv', header = TRUE)
oscar_actors <- unique(oscar_actors[c("actorName")])
movies_data[,'famousActors'] <- NA
movie_actors[,'oscarActor'] <- NA
count = 0
for (i in 1:nrow(movie_actors)){
  actor = movie_actors[i,2]
  for (j in 1:nrow(oscar_actors)){
    if (oscar_actors[j,1] == actor)
      count = count + 1
  }
  movie_actors[i,3] = count
  count = 0
}
for (i in 1:nrow(movies_data)){
  id = movies_data[i,1]
  test_movie = movie_actors[movie_actors$uniqueID == id,]
  count = sum(test_movie$oscarActor)
  movies_data[i,45] = count
}

#movie runtime to the end
movies_data = movies_data %>% relocate(runtime, .after = last_col())
#Export dataframe
write.csv(movies_data,'C:\\Users\\Rrsha\\OneDrive\\Documents\\msis5193_project\\data\\csv_files\\movies_data_combined.csv', row.names = FALSE)



