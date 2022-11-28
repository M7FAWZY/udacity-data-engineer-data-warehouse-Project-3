****************************************
TO write better README https://www.udacity.com/course/writing-readmes--ud777
##I Hope to enjoy and Feedback
~~~~~~~~
Schema design: star schema 
------Fact table: songplays :: records in event data associated with song plays i.e. records with page NextSong

--with 4  Dimension tables: 
-----users, songs, artists, time.
~~~~~~~~

|              |                                                                       |
|-------------:|-----------------------------------------------------------------------|
|      users   | users in the app                                                      |
|      songs   | songs in music database                                               |
|      artists | artists in music database                                             |
|      time    | timestamps of records in songplays broken down into specific units    | 

*********************************************
*********************************************
Files
~~~~
~~~~//sql_queries.py
Creating and dropping staging and star schema tables
, partitioned by CREATE, DROP, COPY and INSERT statement.


~~~~//dwh.cfg 
Configure Redshift cluster and data import

~~~~//create_cluster.py
Create IAM role, Redshift cluster, and allow TCP connection from outside VPC
Pass --delete flag to delete resources
create_tables.py Drop and recreate tables   

~~~~//etl.py 
Copy data to staging tables and insert into star schema fact and dimension tables

~~~~//create_tables.py      
Copy JSON data from S3 to Redshift staging tables
Insert data from staging tables to star schema fact and dimension tables

********
********
Run scripts::::
Set environment variables in [AWS] in dwh.cfg AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
set [CLUSTER] in dhw.cfg
Choose DB/DB_PASSWORD in dhw.cfg.
\\\\\\\\\\\
OVER aws website
**Create IAM role, Redshift cluster, and IAM user**
/Create a new IAM user in your AWS account
/Give it AdministratorAccess and Attach policies
/Use access key and secret key to create clients for EC2, S3, IAM, and Redshift.
/Create an IAM Role that makes Redshift able to access S3 bucket (ReadOnly)
/Create a RedShift Cluster and get the DWH_ENDPOIN(Host address) and DWH_ROLE_ARN and fill the config file.
/Create in redshift cluster submenu networks and security settings 
---press publically accessiable enabled(or check mark)
~~~~~~
![This is an image](https://github.com/M7FAWZY/udacity-data-engineer-data-warehouse-Project-3/blob/8bdf86bdb4559cb1a4fe3b4064b66459b49d6cf8/5d395536-8f31-4ce4-aa1c-06133a7dbb80-mobile.png)
~~~~~~

Stage data
$ python create_cluster.py
\\\\\\\\\\\\\
Complete dwh.cfg with outputs from create_cluster.py
CLUSTER/HOST
IAM_ROLE/ARN
\\\\\\\\\\\\\
Drop and recreate tables
$ python create_tables.py
\\\\\\\\\\\\\\
Run ETL pipeline
$ python etl.py
\\\\\\\\\\\\\\\
Delete IAM role and Redshift cluster
$ python create_cluster.py --delete
\\\\\\\\\\\\\\\
*********
GO to aws website RedShift cluster 

*********
~~~~~~
~~~~~~
STEPS to implement 
1- Complete the sql_queries.py script with
Drop all tables

Create all tables

Insert statements for all table

COPY command for copying S3 to staging

2- Create IAM Role Beware step 2,3,4 in the same region

3- Create Security Group

4- Create a Redshift Cluster Using the above IAM role and Security Group,

5- Fill in the dwh.cfg file with

Redshift cluster connection info

HOST

DB_NAME

DB_USER

DB_PASSWORD

DB_PORT

IAM_ROLE

ARN

6- Run Create_table.py and then etl.py scripts

7- Run queries

8- Delete cluster

9- Create ReadMe.md and zip all the scripts (EXCEPTION: clear dwh.cfg file)

10- Submit the project.

https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

##############
#BRAVO #
##############
