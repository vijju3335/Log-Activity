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
- [Specifications](#specifications)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Running Documents Locally](#running-documents-locally)
- [References](#references)
- [Bug And Feature Requests](#bug-and-feature-requests)

## Demo

For a demo, check out [Live Demo](#).
## Download
The files for the project, [download](https://github.com/vijju3335/LogsAnalysis/archive/master.zip).

### What's included

Within the download you'll find the following directories and files:

```
LogsAnalysis-master.zip/
|
└── LogActivity.py
|
└── images
|     |
|     └── v1.pjg
|     |
|     └── v2.jpg
|     |
|     └── v3.jpg
|     |
|     └── .....
|
└── README.md
```
### Specifications

- our Project must and should meet these [specifications](https://review.udacity.com/#!/rubrics/277/view)

### Queries Needed
The reporting tool needed to answer the following questions:
1. **What are the most popular three articles of all time?**
 Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. **Who are the most popular article authors of all time?**
 That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted    list with the most popular author at the top.
3. **On which days did more than 1% of requests lead to errors?**
The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.?

### Software Requirements

This project should run on a virutal machine created using Vagrant, ToDo this, follow these steps:
- Vagrant
- Virtual Box
- Python, Psycopg2, Postgresql

## Installation
- Install [Vagrant](#vagrant)
- Install [Virtual Box](#virtual-box)

- First go to disk D and create folder VM_14.04
- open command prompt at VM_14.04 folder 

```D:\VM_14.0.4>```

- There are different vagrant-boxes [here](https://app.vagrantup.com/boxes/search)

```D:\VM_14.0.4>vagrant init ubuntu/trusty64 ```  [live demo](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v1.JPG) 

```D:\VM_14.0.4>vagrant up```  [live demo](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v2.JPG)

```\VM_14.04>vagrant ssh```  [live demo](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v3.JPG)

```
vagrant@vagrant-ubuntu-trusty-64:~$ cd /vagrant
vagrant@vagrant-ubuntu-trusty-64:/vagrant$
```
[live demo](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v4.png)

```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ ls -a
.  ..  .vagrant  Vagrantfile
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ 
```
- we need data base to store data.here we use postgresql.To install **postgresql** use these commands :

```vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo apt-get update```

```vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo apt-get install postgresql```

- To do this project, user of postgresql must be **vagrant** but by default user is **postgres**. First we have to create vagrant user and database named vagrant. To do this :
```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo -i -u postgres
postgres@vagrant-ubuntu-trusty-64:~$ psql
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
postgres@vagrant-ubuntu-trusty-64:~$ exit
logout
vagrant@vagrant-ubuntu-trusty-64:/vagrant$
```
- we have to create database vagrant under vagrant as owner,
```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo -i -u vagrant
vagrant@vagrant-ubuntu-trusty-64:~$ createdb vagrant
vagrant@vagrant-ubuntu-trusty-64:~$ 
vagrant@vagrant-ubuntu-trusty-64:~$ psql
psql (9.3.22)
Type "help" for help.

vagrant=#
```
- Now Download the project database [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

- Unzip the data to get the **newsdata.sql** file.Put the newsdata.sql file into the **vagrant directory** [live demo](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v5.JPG).

- In project, we have to create database named **news** :
```
vagrant=#create database news;
CREATE DATABASE
vagrant=#
vagrant=#\q
vagrant@vagrant-ubuntu-trusty-64:~$ exit
logout
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ ls -a
.  ..  newsdata  .vagrant  Vagrantfile
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ cd newsdata
vagrant@vagrant-ubuntu-trusty-64:/vagrant/newsdata$ psql -d news -f newsdata.sql
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
vagrant@vagrant-ubuntu-trusty-64:/vagrant$sudo apt-get install python-psycopg2
vagrant@vagrant-ubuntu-trusty-64:/vagrant$
```
- To connect data-base use this line, **psycopg2.connect(dbname='news', user='vagrant', host='localhost', port='5432', password='vagrant')**

- Now continue writing [Queries](#queries-needed) to Questions.
- we have use **joins, views, select, where clauses** concept to fetch data from DB.

- Run the [python file](#running-documents-locally).

#### Vagrant
- Download the vagrant setup file for **windows** [Vagrant.exe](https://www.vagrantup.com/downloads.html).
These files configure the virtual machine and install all the tools needed to run this project.

#### Virtual Box
- Download the virtual box setup file for **windows** [VirtualBox.exe](https://download.virtualbox.org/virtualbox/5.2.12/VirtualBox-5.2.12-122591-Win.exe).


## Running Documents Locally
- keep .py files and sql files into [vagrant directory](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v6.JPG)
- use below [commmands](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v7.JPG)
```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ python fileName.py
```
see [Output](https://github.com/vijju3335/LogsAnalysis/blob/master/images/v7.JPG)

## References

- youtube for installation
- stack overflow to errors retriving
- [python documentaion](https://docs.python.org/2/index.html)
- [postgresql documentation](https://www.postgresql.org/docs/9.6/static/index.html)
- [psycopg2 documentation](http://initd.org/psycopg/docs/)
- [views](http://www.postgresqltutorial.com/postgresql-views/) concepts.

---

## Bug And Feature Requests
- Have a bug or a feature request? Please feel free to open an [issue](https://github.com/vijju3335/LogsAnalysis/issues).
