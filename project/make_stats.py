#!/usr/bin/env python
# coding: utf-8

import findspark
findspark.init()
import os
import pandas as pd
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


sc = (
    SparkSession.builder
    .appName("vis")
    .master("local")
    .enableHiveSupport()
    .getOrCreate()
)


month_temp_stats = sc.sql("""
    select
        Rok,
        `Miesiąc`,
        avg(`Średnia temperatura dobowa [°C]`) as avg_temp,
        avg(`Maksymalna temperatura dobowa [°C]`) as max_temp,
        avg(`Minimalna temperatura dobowa [°C]`) as min_temp
    from klimat group by Rok, `Miesiąc`
""").toPandas()
month_temp_stats.to_csv('stats/month_temp.csv')


month_rain_stats = sc.sql("""
    select
        Rok,
        `Miesiąc`,
        sum(`Suma dobowa opadów [mm]`) as sum_rain
    from klimat group by Rok, `Miesiąc`
""").toPandas()
month_rain_stats.to_csv('stats/month_rain.csv')

station_temp_stats = sc.sql("""
    select
        `Nazwa stacji`,
        avg(`Średnia temperatura dobowa [°C]`) as avg_temp
    from klimat
    where Rok > 2010
    group by `Nazwa stacji`
""").toPandas()
station_temp_stats.to_csv('stats/station_temp.csv')


month_synop = sc.sql("""
    select
        Rok,
        `Miesiąc`,
        sum(`Czas trwania opadu deszczu [godziny]`) / sum(case when `Status pomiaru DESZ` = 'brak pomiaru' then 0 else 1 end) as avg_time_deszcz,
        sum(`Czas trwania opadu śniegu [godziny]`) / sum(case when `Status pomiaru SNEG` = 'brak pomiaru' then 0 else 1 end) as avg_time_snieg,
        sum(`Czas trwania opadu deszczu ze śniegiem [godziny]`) / sum(case when `Status pomiaru DISN` = 'brak pomiaru' then 0 else 1 end) as avg_time_deszcz_ze_sniegiem,
        sum(`Czas trwania gradu [godziny]`) / sum(case when `Status pomiaru GRAD` = 'brak pomiaru' then 0 else 1 end) as avg_time_grad,
        sum(`Czas trwania mgły [godziny]`) / sum(case when `Status pomiaru MGLA` = 'brak pomiaru' then 0 else 1 end) as avg_time_mgla,
        sum(`Czas trwania zamglenia`) / sum(case when `Status pomiaru ZMGL` = 'brak pomiaru' then 0 else 1 end) as avg_time_zamglenie,
        sum(`Czas trwania sadzi [godziny]`) / sum(case when `Status pomiaru SADZ` = 'brak pomiaru' then 0 else 1 end) as avg_time_sadz,
        sum(`Czas trwania gołoledzi [godziny]`) / sum(case when `Status pomiaru GOLO` = 'brak pomiaru' then 0 else 1 end) as avg_time_gololedz,
        sum(`Czas trwania zamieci śnieżnej niskiej [godziny]`) / sum(case when `Status pomiaru ZMNI` = 'brak pomiaru' then 0 else 1 end) as avg_time_zamiec_niska,
        sum(`Czas trwania zamieci śnieżnej wysokiej [godziny]`) / sum(case when `Status pomiaru ZMWS` = 'brak pomiaru' then 0 else 1 end) as avg_time_zamiec_wysoka,
        sum(`Czas trwania zmętnienia [godziny]`) / sum(case when `Status pomiaru ZMET` = 'brak pomiaru' then 0 else 1 end) as avg_time_zmetnienie,
        sum(`Czas trwania wiatru >=10m/s [godziny]`) / sum(case when `Status pomiaru FF10` = 'brak pomiaru' then 0 else 1 end) as avg_time_wiatr_10ms,
        sum(`Czas trwania wiatru >15m/s [godziny]`) / sum(case when `Status pomiaru FF15` = 'brak pomiaru' then 0 else 1 end) as avg_time_wiatr_15ms,
        sum(`Czas trwania burzy`) / sum(case when `Status pomiaru BRZA` = 'brak pomiaru' then 0 else 1 end) as avg_time_burza,
        sum(`Czas trwania rosy`) / sum(case when `Status pomiaru ROSA` = 'brak pomiaru' then 0 else 1 end) as avg_time_rosa,
        sum(`Czas trwania szronu [godziny]`) / sum(case when `Status pomiaru SZRO` = 'brak pomiaru' then 0 else 1 end) as avg_time_szron
    from synop_test
    group by Rok, `Miesiąc`
""").toPandas()


month_synop.to_csv('stats/month_synop.csv')



