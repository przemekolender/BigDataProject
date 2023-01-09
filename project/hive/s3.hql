CREATE EXTERNAL TABLE stations (
    INDEX INT
    ,ICAO STRING
    ,Country STRING
    ,Latitude STRING
    ,Longitude STRING
    ,Altitude INT
    ,Notes STRING
)
STORED AS ORC
LOCATION '/user/project/stations';
