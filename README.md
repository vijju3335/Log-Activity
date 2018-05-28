## Logs Analysis Project
Udacity Full Stack Nano Degree Project #3

The third project of the [Udacity Full Stack Web Developer Nanodegree Program](https://in.udacity.com/course/full-stack-web-developer-nanodegree--nd004) called "Build a Logs Analysis".

## Project Overview

Your task is to create a **Reporting Tool** that prints out reports (in simple text) 
based on the data in the database. This reporting tool is a **Python program 
using the psycopg2 module to connect to the database.**

## Table Of Contents

- [Demo](#demo)
- [Download](#download)
- [Queries Needed](#queries-needed)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Views](#views)
- [Running Documents Locally](#running-documents-locally)
- [References](#references)
- [Bug And Feature Requests](#bug-and-feature-requests)

## Demo

For a demo, check out [Live Demo](#https://github.com/vijju3335/LogsAnalysis/blob/master/images/report.JPG).
## Download
The files for the project, [download](https://github.com/vijju3335/LogsAnalysis/archive/master.zip).

### What's included

Within the download you'll find the following directories and files:

```
LogsAnalysis-master.zip/
|
└── reportingTool.py
|
└── images
|     |
|     └── sql.jpg
|     └── report.jpg
|
└── README.md
```

## Queries Needed

The reporting tool needed to answer the following questions:
1. **What are the most popular three articles of all time?**
 Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
 
2. **Who are the most popular article authors of all time?**
 That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted    list with the most popular author at the top.
 
3. **On which days did more than 1% of requests lead to errors?**
The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.?

## Software Requirements

This project should run on a **Virutal Machine created using Vagrant**, you can get from below.

- [Vagrant Virtual-Machine](https://github.com/vijju3335/Vagrant-Installation).

## Installation
- we need DataBase to store data.To organise, Here we use postgresql.

-To install **postgresql** use below commands :

```vagrant@vagrant:/vagrant$ sudo apt-get update```

```vagrant@vagrant:/vagrant$ sudo apt-get install postgresql```

- To do this project, user of postgresql must be **vagrant** but by default user is **postgres**. First we have to create vagrant user and database named vagrant.To do this use below commands,

But if you installed by downloading [here](#download) you need to Skip,Before this use command  ```vagrant@vagrant:/vagrant$ psql``` then press [continue](#data-base-setup).

```
vagrant@vagrant:/vagrant$ sudo -i -u postgres
postgres@vagrant:~$ psql
psql (9.3.22)
Type "help" for help.

postgres=#
postgres=# create role vagrant with password 'vagrant';
CREATE ROLE
postgres=# alter role vagrant with Superuser;
ALTER ROLE
postgres=# alter role vagrant with createdb;
ALTER ROLE
postgres=# alter role vagrant with createuser;
ALTER ROLE
```
- Now, quit postresql by command :
```
postgres=# \q
```
- Later, logout from user postgres by command : 
```
postgres@vagrant:~$ exit
logout
vagrant@vagrant:/vagrant$
```
- we have to create database vagrant under vagrant as owner,
#### Switch to User Vargant
```
vagrant@vagrant:/vagrant$ sudo -i -u vagrant
vagrant@vagrant:~$ createdb vagrant
vagrant@vagrant:~$ 
vagrant@vagrant:~$ psql
psql (9.3.22)
Type "help" for help.

vagrant=#
```
#### Data Base Setup
- Now Download the project DataBase [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

- Unzip the data to get the **newsdata.sql** file.Put the newsdata.sql file into the **vagrant directory** [live demo](https://github.com/vijju3335/LogsAnalysis/blob/master/images/sql.JPG).

- For this project, we have to create database named **news** :
```
vagrant=#create database news;
CREATE DATABASE
vagrant=#
vagrant=#\q
vagrant@vagrant:~$ exit
logout
vagrant@vagrant:/vagrant$ ls -a
.  ..  newsdata  .vagrant  Vagrantfile
vagrant@vagrant:/vagrant$
vagrant@vagrant:/vagrant/newsdata$ psql -d news -f newsdata.sql
```
- Above command creates 3 tables , use \c to switch DB and data will be fetched from newsdata.Tables are :
```
vagrant=# \c news
You are now connected to database "news" as user "vagrant".
news=# \dt
          List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | articles | table | vagrant
 public | authors  | table | vagrant
 public | log      | table | vagrant
(3 rows)

news=#
```
- Now we have to write [Queries Needed](#queries-needed) using **python-psycopg2**.
- To use python as Back End,we have to install **psycopg2** :
```
vagrant@vagrant:/vagrant$ sudo apt-get install python-psycopg2
vagrant@vagrant:/vagrant$
```
- To connect data-base use this line, **psycopg2.connect(dbname='news', user='vagrant', host='localhost', port='5432', password='vagrant')**

- Now continue writing [Queries](#queries-needed) to Questions.
- we have use **joins, select, where, group by, order by clauses, views is optional** concept to fetch data from DB.

## Views
- we have already seen 3 tables for their schema, use this command,``` news=# \d table-name ```
- In this project, i used following **views** also,Before Running python file,you have to create these views.
     - log_slug
     - authors_name
     - log_fail
     - log_total
- You can directly import all views from views.sql file already attached in this repository, by using this command,

```vagrant@vagrant:/vagrant$ psql -d news -f views.sql``` [see here](https://github.com/vijju3335/LogsAnalysis/blob/master/images/views.JPG)

     #### log_slug
     - replace() is used to place value by other value, syntax **replace(columnName, replace which value, by which value)**.
     - Use below query to create VIEW log_slug,
     
     ```
     CREATE VIEW log_slug as SELECT replace(path,'/article/','') as slug, count(*) as views
     FROM log
     WHERE path <> '/' AND status ='200 OK' GROUP BY path;
     ```
     - This view contains **log-path that has replaced such a way to get slug** as **slug** and their **count** as **views**.
     ```
                slug            | views
     ---------------------------+--------
      goats-eat-googles         |  84906
      so-many-bears             |  84504
      balloon-goons-doomed      |  84557
      media-obsessed-with-bears |  84383
      trouble-for-troubled      |  84810
      candidate-is-jerk         | 338647
      bears-love-berries        | 253801
      bad-things-gone           | 170098
     (8 rows)
     ```
     
     #### authors_name
     - Use below query to create VIEW authors_name,
     
     ```
     CREATE VIEW authors_name as SELECT authors.name as name, articles.slug as slug
     FROM authors INNER JOIN articles
     ON articles.author=authors.id ORDER BY authors.id;
     ```
     - This contains **author-name** as **name** and **articles-slug** as **slug**.
     ```
               name          |           slug
     ------------------------+---------------------------
      Ursula La Multa        | so-many-bears
      Ursula La Multa        | bears-love-berries
      Ursula La Multa        | goats-eat-googles
      Ursula La Multa        | media-obsessed-with-bears
      Rudolf von Treppenwitz | trouble-for-troubled
      Rudolf von Treppenwitz | candidate-is-jerk
      Anonymous Contributor  | bad-things-gone
      Markoff Chaney         | balloon-goons-doomed
    (8 rows)
     ```
     
     #### log_fail
     - Use below query to create VIEW log_fail,
     
     ```
     CREATE VIEW log_fail as SELECT Date(time), count(Date(time))
     FROM log
     WHERE status='404 NOT FOUND' GROUP BY Date(time) ORDER BY Date(time);
     ```
     - This view contains **no.of failed logs**  and their **date**.
     ```
        date    | count
    ------------+-------
     2016-07-01 |   274
     2016-07-02 |   389
     2016-07-03 |   401
     2016-07-04 |   380
     2016-07-05 |   423
     2016-07-06 |   420
     2016-07-07 |   360
     2016-07-08 |   418
     2016-07-09 |   410
     2016-07-10 |   371
     2016-07-11 |   403
     2016-07-12 |   373
     2016-07-13 |   383
     2016-07-14 |   383
     2016-07-15 |   408
     2016-07-16 |   374
     2016-07-17 |  1265
     2016-07-18 |   374
     2016-07-19 |   433
     2016-07-20 |   383
     2016-07-21 |   418
     2016-07-22 |   406
     2016-07-23 |   373
     2016-07-24 |   431
     2016-07-25 |   391
     2016-07-26 |   396
     2016-07-27 |   367
     2016-07-28 |   393
     2016-07-29 |   382
     2016-07-30 |   397
     2016-07-31 |   329
    (31 rows)
     ```
     
     #### log_total
     - Use below query to create VIEW log_total,
     
     ```
     CREATE VIEW log_total as SELECT Date(time), count(Date(time)) 
     FROM log
     GROUP BY Date(time);
     ```
     - This view contains **total no.of logs**  and their **date**.
     ```
        date    | count
    ------------+-------
     2016-07-01 | 38705
     2016-07-02 | 55200
     2016-07-03 | 54866
     2016-07-04 | 54903
     2016-07-05 | 54585
     2016-07-06 | 54774
     2016-07-07 | 54740
     2016-07-08 | 55084
     2016-07-09 | 55236
     2016-07-10 | 54489
     2016-07-11 | 54497
     2016-07-12 | 54839
     2016-07-13 | 55180
     2016-07-14 | 55196
     2016-07-15 | 54962
     2016-07-16 | 54498
     2016-07-17 | 55907
     2016-07-18 | 55589
     2016-07-19 | 55341
     2016-07-20 | 54557
     2016-07-21 | 55241
     2016-07-22 | 55206
     2016-07-23 | 54894
     2016-07-24 | 55100
     2016-07-25 | 54613
     2016-07-26 | 54378
     2016-07-27 | 54489
     2016-07-28 | 54797
     2016-07-29 | 54951
     2016-07-30 | 55073
     2016-07-31 | 45845
    (31 rows)
     ```
     
## Running Documents Locally
- keep .py files and sql files into [VM_Vagrant directory](https://github.com/vijju3335/LogsAnalysis/blob/master/images/sql.JPG).
- use below command to run pyhton file.
```
vagrant@vagrant:/vagrant$ python reportingTool.py
```

## Output
see [Output](https://github.com/vijju3335/LogsAnalysis/blob/master/images/report.JPG)

## References

- youtube for installation.
- stack overflow to errors retriving.
- [python documentaion](https://docs.python.org/2/index.html)
- [postgresql documentation](https://www.postgresql.org/docs/9.6/static/index.html).
- [psycopg2 documentation](http://initd.org/psycopg/docs/).
- [views](http://www.postgresqltutorial.com/postgresql-views/) concepts.
- [python floating format](https://cs.nyu.edu/courses/spring12/CSCI-UA.0002-007/Basic%20Formatting%20in%20Python.pdf)

---

## Bug And Feature Requests
- Have a bug or a feature request? Please feel free to open an [issue](https://github.com/vijju3335/LogsAnalysis/issues).
