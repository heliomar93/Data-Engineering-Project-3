<h1>Data Warehouse</h1>

<h2>Introduction</h2>
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, I'm tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to. I needed to test the database and ETL pipeline by running queries given by the analytics team from Sparkify and compare the results with their expected results.

<h2>Project Description</h2>
In this project, I applied what I'd learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, I needed to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

<h2>Data</h2>
The data used in this project is in JSON format. 

<h3>Log data</h3>
On these files, the actions done by the users of Sparkify are are registered, in the format as follows:
~~~~
{"artist":"Hoobastank","auth":"Logged In","firstName":"Cierra","gender":"F","itemInSession":0,"lastName":"Finley","length":241.3971,"level":"free","location":"Richmond, VA","method":"PUT","page":"NextSong","registration":1541013292796.0,"sessionId":132,"song":"Say The Same","status":200,"ts":1541808927796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.77.4 (KHTML, like Gecko) Version\/7.0.5 Safari\/537.77.4\"","userId":"96"}

~~~~

<h3>Song data</h3>
On these files, there are the infos about the songs in this way:
~~~~
{"artist_id":"ARJNIUY12298900C91","artist_latitude":null,"artist_location":"","artist_longitude":null,"artist_name":"Adelitas Way","duration":213.9424,"num_songs":1,"song_id":"SOBLFFE12AF72AA5BA","title":"Scream","year":2009}

~~~~

<h3>Log data json</h3>
The metadata about the log data are saved on this file and help us to deal with the log data.

<h2>Staging tables</h2>
First of all, we save the logs and the songs on the staging tables; staging_events and staging_songs. We saved the data on the way they are, without doing any transformation. 

<h3>Staging events</h3>
The staging events is the database where we insert the data from the data in JSON format. 

| COLUMN | TYPE | 
| ------ | ---- |
|artist|VARCHAR(200)|
|auth|VARCHAR(200)|
|firstName|VARCHAR(200) |
|gender|VARCHAR(100)|
|itemInSession|INT|
|lastName|VARCHAR(200)|
|length|FLOAT|
|level|VARCHAR(100)|
|location|VARCHAR(200)|
|method|VARCHAR(200)|
|page|VARCHAR(200) |
|registration|NUMERIC|
|sessionId|VARCHAR(200)|
|song|VARCHAR(200)|
|status|INT|
|ts|BIGINT|
|userAgent|VARCHAR(200)|
|userId|VARCHAR(200)|

<h3>Staging songs</h3>
THe staging song is the table that we insert the data from song data bucket.

| COLUMN | TYPE | 
| ------ | ---- |
|song_id|VARCHAR(100)|
|title|VARCHAR(200)|
|duration|DECIMAL|
|year|SMALLINT|
|artist_id|VARCHAR(100)|
|artist_name|VARCHAR(200)|
|artist_latitude|REAL|
|artist_longitude|REAL|
|artist_location|VARCHAR(200)|
|num_songs|INT|

<h2>Analytics tables</h2>
After we insert our data in the staging tables, we create table to save the data in the best way to delivry it to the analytics team. To do that, we've made some transformations.

<h3>Songplay table</h3>   
| COLUMN | TYPE | 
| ------ | ---- |
|songplay_id|INTEGER|
|tart_time|BIGINT|
|user_id|VARCHAR(200)|
|level|VARCHAR(100)| 
|artist_id|VARCHAR(100)|
|session_id|VARCHAR(200)|  
|location|VARCHAR(200)| 
|user_agent|VARCHAR(200)|

<h3>Users table</h3>   
| COLUMN | TYPE | 
| ------ | ---- |
|user_id|VARCHAR(200)| 
|first_name|VARCHAR(200)| 
|last_name|VARCHAR(200)| 
|gender|VARCHAR(10)| 
|level|VARCHAR(100)|

<h3>Song table</h3>   
| COLUMN | TYPE | 
| ------ | ---- |
|song_id|VARCHAR(100)| 
|title|VARCHAR(200)| 
|artist_id|VARCHAR(100)| 
|year|SMALLINT| 
|duration|FLOAT4|

<h3>Artists table</h3>   
| COLUMN | TYPE | 
| ------ | ---- |
|artist_id|VARCHAR(100)| 
|artist_name|VARCHAR(200)| 
|location|VARCHAR(200)| 
|latitude|DECIMAL| 
|longitude|DECIMAL|

<h3>Time table</h3>   
| COLUMN | TYPE | 
| ------ | ---- |
|start_time|TIMESTAMP|
|hour|SMALLINT| 
|day|SMALLINT| 
|week|SMALLINT| 
|month|SMALLINT| 
|year|SMALLINT| 
|weekday|SMALLINT|

<h2>Scripts</h2>
The scripts extract, transform and load the data.

<h3>SQL queries</h3>   
In this script, we insert the SQL queries to create and drop tables, insert the data into the tables, transform and load the data.

<h3>Create tables</h3>   
This script create the tables, using the sq_queries.py.

<h3>ETL</h3>   
This file extract, transform and load the data into the tables, previous created by the create_tables.py.