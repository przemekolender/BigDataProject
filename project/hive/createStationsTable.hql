CREATE EXTERNAL TABLE stations (
    Id INT
    ,ICAO STRING
    ,Country STRING
    ,Latitude STRING
    ,Longitude STRING
    ,Altitude INT
    ,Notes STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\073'
LINES TERMINATED BY '\n'
STORED AS ORC
LOCATION '/user/project/stations';
LOAD DATA INPATH '/user/project/nifi_out/station.orc' INTO TABLE stations;
