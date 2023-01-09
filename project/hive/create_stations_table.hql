CREATE TABLE stations (
    StationIndex INT
    ,ICAO STRING
    ,City STRING 
    ,Country STRING
    ,Latitude STRING
    ,Longitude STRING
    ,Altitude INT
    ,Notes STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\;'
LINES TERMINATED BY '\n';
LOAD DATA INPATH '/user/project/nifi_in/stations.csv' OVERWRITE INTO TABLE stations;
CREATE TABLE stations_orc STORED AS ORC as SELECT * FROM stations;
DROP TABLE stations;
