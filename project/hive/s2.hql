CREATE EXTERNAL TABLE stacje (
    INDEX INT
    ,ICAO STRING
    ,Country STRING
    ,Latitude STRING
    ,Longitude STRING
    ,Altitude INT
    ,Notes STRING
)
LOCATION '/user/project/stacje';
LOAD data inpath '/user/project/nifi_out/stations.orc' INTO TABLE stacje;
