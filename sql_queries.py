import configparser
import psycopg2

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
#config.read_file(open('dwh.cfg'))

#TAKE care of table names in DROP , CREATE , COPY and INSERT
# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
#ts is bigint not timestamp as it will run in aws RedShift Cluster to be divided to smallint for each 
#hour,day,week,year,month,weekday
#make sure attributes in that order FOR staging_events_table_create as it will be ARRANGED in COPY opertion
staging_events_table_create = ("""CREATE TABLE staging_events
    (    
    artist_name VARCHAR(255),
    auth VARCHAR(50),
    user_first_name VARCHAR(255),
    user_gender  VARCHAR(1),
    item_in_session	INTEGER,
    user_last_name VARCHAR(255),
    song_length	DOUBLE PRECISION, 
    user_level VARCHAR(50),
    location VARCHAR(255),	
    method VARCHAR(25),
    page VARCHAR(35),	
    registration VARCHAR(50),	
    session_id	BIGINT,
    song_title VARCHAR(255),
    status INTEGER,  
    ts bigint,
    user_agent TEXT,	
    user_id VARCHAR(100)
    );
""")


staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
    (
        song_id             TEXT,
        title               TEXT,
        duration            FLOAT4,
        year                SMALLINT,
        artist_id           TEXT,
        artist_name         TEXT,
        artist_latitude     REAL,
        artist_longitude    REAL,
        artist_location     TEXT,
        num_songs           INTEGER
    );
""")
#BE CAREFUL with SORTKEY and DISTKEY
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id    BIGINT IDENTITY(1, 1)  PRIMARY KEY,
        start_time     TIMESTAMP NOT NULL SORTKEY,
        user_id        TEXT NOT NULL DISTKEY,
        level          TEXT  NOT NULL,
        song_id        TEXT  NOT NULL,
        artist_id      TEXT  NOT NULL,
        session_id     INTEGER  NOT NULL,
        location       TEXT  NOT NULL,
        user_agent     TEXT  NOT NULL
    ) diststyle key;
""")#LOOK diststyle key is used

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id     TEXT NOT NULL PRIMARY KEY SORTKEY,
        first_name  TEXT NOT NULL,
        last_name   TEXT  NOT NULL,
        gender      TEXT NOT NULL,
        level       TEXT NOT NULL
    ) diststyle all;
""")#LOOK diststyle all is used

song_table_create =("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id     TEXT  NOT NULL PRIMARY KEY SORTKEY,
        title       TEXT,
        artist_id   TEXT NOT NULL DISTKEY,
        year        SMALLINT NOT NULL,
        duration    FLOAT4 NOT NULL
    ) diststyle key;
""")#LOOK diststyle key is used

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id   TEXT PRIMARY KEY SORTKEY,
        name        TEXT NOT NULL,
        location    TEXT ,
        latitude    FLOAT4 ,
        longitude   FLOAT4 
    ) diststyle all;
""")#LOOK diststyle all is used

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
        start_time  TIMESTAMP PRIMARY KEY SORTKEY,
        hour        SMALLINT,
        day         SMALLINT,
        week        SMALLINT,
        month       SMALLINT,
        year        SMALLINT DISTKEY,
        weekday     SMALLINT
    ) diststyle key;
""")#LOOK diststyle key is used

# STAGING TABLES
#automated copy opertion
staging_events_copy = ("""
    COPY {} FROM {}
    IAM_ROLE '{}'
    JSON {} region '{}';
""").format(
    'staging_events',
    config['S3']['LOG_DATA'],
    config['IAM_ROLE']['ARN'],
    config['S3']['LOG_JSONPATH'],
    config['CLUSTER']['REGION']
)


staging_songs_copy = ("""
    COPY {} FROM {}
    IAM_ROLE '{}'
    JSON 'auto' region '{}';
""").format(
    'staging_songs',
    config['S3']['SONG_DATA'],
    config['IAM_ROLE']['ARN'],
    config['CLUSTER']['REGION']
)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) SELECT
        TIMESTAMP 'epoch' + (e.ts/1000 * INTERVAL '1 second'),
        e.user_id,
        e.level,
        s.song_id,
        s.artist_id,
        e.session_id,
        e.location,
        e.user_agent
    FROM stage_event e
    LEFT JOIN stage_song s ON
        e.song = s.title AND
        e.artist = s.artist_name AND
        ABS(e.length - s.duration) < 2
    WHERE
        e.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users SELECT DISTINCT (user_id)
        user_id,
        first_name,
        last_name,
        gender,
        level
    FROM stage_event
""")

song_table_insert = ("""
    INSERT INTO songs SELECT DISTINCT (song_id)
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM stage_song
""")

artist_table_insert = ("""
    INSERT INTO artists SELECT DISTINCT (artist_id)
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM stage_song
""")

time_table_insert = ("""
    INSERT INTO time
        WITH temp_time AS (SELECT TIMESTAMP 'epoch' + (ts/1000 * INTERVAL '1 second') as ts FROM stage_event)
        SELECT DISTINCT
        ts,
        extract(hour from ts),
        extract(day from ts),
        extract(week from ts),
        extract(month from ts),
        extract(year from ts),
        extract(weekday from ts)
        FROM temp_time
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create,  user_table_create, song_table_create,                                  artist_table_create, time_table_create,songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,                                        song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
#[LOG_DATA, LOG_JSONPATH, SONG_DATA] = config['S3'].values()

#ARN = config['IAM_ROLE']['ARN']

#staging_events_copy = ("""copy {} from {} credentials 'aws_iam_role={} 'region 'us-west-2' json {};""").format('staging_events_table', LOG_DATA, ARN, LOG_JSONPATH)