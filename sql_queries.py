import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSON_PATH = config.get("S3", "LOG_JSON_PATH")
SONG_DATA = config.get("S3", "SONG_DATA")
ARN = config.get("IAM_ROLE", "ARN")
REGION = config.get('CLUSTER', 'REGION')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= ("""
 CREATE TABLE IF NOT EXISTS staging_events(
 event_id INTEGER IDENTITY(0,1) PRIMARY KEY,
 artist        VARCHAR(200),
 auth          VARCHAR(200),
 firstName     VARCHAR(200),
 gender        VARCHAR(100),
 itemInSession INT,
 lastName      VARCHAR(200),
 length        FLOAT,
 level         VARCHAR(100),
 location      VARCHAR(200),
 method        VARCHAR(200),
 page          VARCHAR(200),
 registration  VARCHAR(15),
 sessionId     VARCHAR(200),
 song          VARCHAR(200),
 status        INT,
 ts            BIGINT,
 userAgent     VARCHAR(200),
 userId        VARCHAR(200)
 ); 
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
song_id             VARCHAR(100),
title               VARCHAR(200),
duration            FLOAT,
year                SMALLINT,
artist_id           VARCHAR(100),
artist_name         VARCHAR(200),
artist_latitude     REAL,
artist_longitude    REAL,
artist_location     VARCHAR(200),
num_songs           INT,
primary key(song_id)
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay(
songplay_id INTEGER IDENTITY(0, 1) PRIMARY KEY, 
start_time TIMESTAMP sortkey, 
user_id VARCHAR(200) NOT NULL, 
level VARCHAR(100) NOT NULL, 
artist_id VARCHAR(100), 
session_id VARCHAR(200) NOT NULL,  
location VARCHAR(200) NOT NULL, 
user_agent VARCHAR(200) NOT NULL
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id VARCHAR(200) NOT NULL, 
first_name VARCHAR(200) NOT NULL, 
last_name VARCHAR(200) NOT NULL, 
gender VARCHAR(10) NOT NULL, 
level VARCHAR(100) NOT NULL,
PRIMARY KEY (user_id)
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song(
song_id VARCHAR(100), 
title VARCHAR(200), 
artist_id VARCHAR(100), 
year SMALLINT sortkey, 
duration FLOAT4,
PRIMARY KEY(song_id)
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id VARCHAR(100), 
artist_name VARCHAR(200), 
location VARCHAR(200), 
latitude DECIMAL, 
longitude DECIMAL,
PRIMARY KEY(artist_id)
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
start_time TIMESTAMP, 
hour SMALLINT, 
day SMALLINT, 
week SMALLINT, 
month SMALLINT, 
year SMALLINT, 
weekday SMALLINT,
PRIMARY KEY(start_time)
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {}
iam_role {}
REGION {}
FORMAT AS json {};
""").format(LOG_DATA,ARN,REGION,LOG_JSON_PATH)

staging_songs_copy = ("""
COPY staging_songs
FROM {}
iam_role {}
REGION {}
FORMAT AS json 'auto';
""").format(SONG_DATA,ARN,REGION)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplay(start_time,user_id, level, artist_id, session_id, location, user_agent)
SELECT TIMESTAMP 'epoch' + se.ts * INTERVAL '1 Second',
       se.userId,
       se.level,
       ss.artist_id,
       se.sessionId,
       se.location,
       se.userAgent
FROM staging_events se
JOIN staging_songs ss ON se.song = ss.title AND se.artist = ss.artist_name AND se.length = ss.duration
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
WITH uniq_staging_events AS (
SELECT userId, 
        firstName, 
        lastName, 
        gender, 
        level,
        ROW_NUMBER() OVER(PARTITION BY userid ORDER BY ts DESC) AS rank
FROM staging_events
WHERE userid != NULL
    AND page = 'NextSong'
)
SELECT userId, 
        firstName, 
        lastName, 
        gender, 
        level
FROM uniq_staging_events
WHERE rank = 1;
;
""")

song_table_insert = ("""
INSERT INTO song(song_id, title, artist_id, year, duration)
WITH uniq_staging_songs AS (
SELECT song_id,
       title,
       artist_id,
       year,
       duration,
        ROW_NUMBER() OVER(PARTITION BY song_id ORDER BY year DESC) AS rank
FROM staging_songs
)
SELECT song_id,
       title,
       artist_id,
       year,
       duration
FROM uniq_staging_songs
WHERE rank = 1;
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, artist_name, location, latitude, longitude)
WITH uniq_staging_songs AS (
SELECT artist_id,
        artist_name, 
        artist_location, 
        artist_latitude, 
        artist_longitude,
        ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY year DESC) AS rank
FROM staging_songs
)
SELECT artist_id,
        artist_name, 
        artist_location, 
        artist_latitude, 
        artist_longitude
FROM uniq_staging_songs
WHERE rank = 1;
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
SELECT TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second',
        EXTRACT(hour from TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second'),
        EXTRACT(day from TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second'),
        EXTRACT(week from TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second'),
        EXTRACT(month from TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second'),
        EXTRACT(year from TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second'),
        EXTRACT(dayofweek from TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second')
FROM staging_events se;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
