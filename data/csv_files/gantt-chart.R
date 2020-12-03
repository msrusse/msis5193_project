library(tidyverse)
  

item <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
activity <- c("Develop Idea", "Business Understanding", "Locating data", "Scrape Box Office Mojo", "Clean/Transform/Concolidate Mojo Data", "Scape Wiki", "Clean/Transform Wiki Data", "Data Consolidation", "Reseach Similar Studies", "Build a Data Dictionary", "Deliverables 1", "Descriptive Analysis", "Predictive Analysis", "Write-up", "video")
start <- c(as.Date("2020-8-21"),as.Date("2020-9-6"), as.Date("2020-9-14"), as.Date("2020-9-21"), as.Date("2020-9-21"), as.Date("2020-10-12"), as.Date("2020-10-12"), as.Date("2020-10-14"), as.Date("2020-10-15"), as.Date("2020-10-15"), as.Date("2020-10-16"), as.Date("2020-11-03"), as.Date("2020-11-03"), as.Date("2020-11-23"), as.Date("2020-11-23"))
end <- c(as.Date("2020-9-6"),as.Date("2020-9-20"), as.Date("2020-10-30"), as.Date("2020-10-23"), as.Date("2020-10-23"), as.Date("2020-10-21"), as.Date("2020-10-21"), as.Date("2020-11-02"), as.Date("2020-10-24"), as.Date("2020-11-09"), as.Date("2020-10-25"), as.Date("2020-11-20"), as.Date("2020-11-20"),as.Date("2020-12-4"),as.Date("2020-12-4"))
person <- c("Everyone","Everyone", "Everyone", "Mason", "Mason", "Ryan", "Ryan", "Mason", "Noah", "Noah", "Everyone", "Noah", "Ryan", "Everyone","Everyone")
schedule <- data.frame(item,start,end,activity, person)


ggplot(schedule, aes(x = start, color = person)) +
  theme_bw()+
  geom_segment(aes(xend = end, y = activity, yend = activity), size = 10) +
  labs(title='Project Schedule', x='Month', y='Activity') +
  facet_grid(item ~ .,scale = "free_y",space = "free_y", drop = TRUE)

