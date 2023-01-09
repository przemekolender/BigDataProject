CREATE TABLE
stacje_slownik
(
    INDEX INT
    ,ICAO STRING
    ,Country STRING
    ,Latitude STRING
    ,Longitude STRING
    ,Altitude INT
    ,Notes STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\;'
LINES TERMINATED BY '\n';
