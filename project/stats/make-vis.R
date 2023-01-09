library(ggplot2)
library(dplyr)
library(stringr)
library(stringi)
library(tidyr)

df <- read.csv('illigal_klimat.csv')

month_rain <- read.csv('./month_rain.csv')
month_temp <- read.csv('./month_temp.csv')
month_synop <- read.csv('./month_synop.csv')
station_temp <- read.csv('./station_temp.csv')

month_temp %>%
  mutate(Miesiąc = str_pad(Miesiąc, width=2, pad="0")) %>%
  ggplot(aes(x=Rok, y=avg_temp)) + geom_point() + geom_smooth(method="lm") + facet_wrap(~Miesiąc) +
  xlab('Rok') + ylab('Średnia dobowa temperatura') + ggtitle("Średnie dobowe temperatury w podziale na miesiące")
ggsave('month_temp.png', width=8, height=6)

month_temp %>%
  pivot_longer(names_to="agg_type", values_to="temp", cols=ends_with('_temp')) %>%
  group_by(Miesiąc, agg_type) %>%
  mutate(temp = temp - mean(temp)) %>%
  ungroup %>%
  mutate(Miesiąc = str_pad(Miesiąc, width=2, pad="0")) %>%
  ggplot(aes(x=Rok, y=temp, color=agg_type)) + geom_smooth(method="lm", se=FALSE) + facet_wrap(~Miesiąc, nrow=3) +
  xlab('Rok') + ylab('Wycentrowane średnie dobowe temperatury') + ggtitle("Zmiany dobowych temperatur w podziale na miesiące i rodzaj agregacji") +
  scale_color_discrete(name = "Temperatura", labels = c("Średnia dobowa", "Maksymalna dobowa", "Minimalna dobowa"))
ggsave('month_temp_trends.png', width=8, height=6)

month_rain %>%
  group_by(Rok) %>%
  summarise(sum_rain=sum(sum_rain)) %>%
  ggplot(aes(x=Rok, y=sum_rain/1000)) + geom_point() + geom_smooth() +
  xlab('Rok') + ylab('Suma rocznych opadów w m') + ggtitle("Suma rocznych opadów")
ggsave('year_rain.png', width=8, height=6)

month_rain %>%
  mutate(Miesiąc = str_pad(Miesiąc, width=2, pad="0")) %>%
  ggplot(aes(x=Rok, y=sum_rain/1000)) + geom_point() + geom_smooth() + facet_wrap(~Miesiąc) +
  scale_y_continuous(limits=c(0,20)) +
  xlab('Rok') + ylab('Suma miesięcznych opadów w m') + ggtitle("Suma miesięcznych opadów")
ggsave('month_rain.png', width=8, height=6)

station_temp %>%
  arrange(desc(avg_temp)) %>%
  mutate(Nazwa.stacji = factor(Nazwa.stacji, levels=Nazwa.stacji)) %>%
  filter((avg_temp <  quantile(avg_temp, 0.07)) | (avg_temp > quantile(avg_temp, 0.93))) %>%
  mutate(type=ifelse(avg_temp > mean(avg_temp), "Najcieplejsze", "Najzimniejsze")) %>%
  mutate(type=factor(type, levels=c('Najzimniejsze', 'Najcieplejsze'))) %>%
  ggplot(aes(y=Nazwa.stacji, x=avg_temp)) +
  geom_col() + facet_wrap(~type, nrow=2, scales="free_y") +
  ylab('Nazwa stacji') + ggtitle('Najcieplejsze i najziemniejsze miejsca w Polsce') + xlab('Średnia z dobowych temperatur')
ggsave('station_temp_ranking.png', width=8, height=6)

month_synop %>%
  pivot_longer(cols=starts_with('avg_time'), names_to="phenomenon", values_to="time") %>%
  mutate(phenomenon=stri_sub(phenomenon, 10)) %>%
  group_by(Rok, phenomenon) %>%
  summarise(time = mean(time)) %>%
  ggplot(aes(y=time,x=Rok)) + geom_line() + facet_wrap(~phenomenon, scale="free_y") + scale_x_continuous(limits=c(1966, 2025)) + ylab('Średnia dzienna liczba godzin') + xlab('Rok') + geom_smooth(method='lm') + ggtitle('Średnia liczba godzin w ciągu dnia gdy występuje podane zjawisko')
ggsave('month_synop.png', width=8, height=6)
