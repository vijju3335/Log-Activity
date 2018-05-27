#!/usr/bin/env python
import psycopg2

# Below lines helps us Connect to the PostgreSQL DB if not, rasies exception
try:
    connect = psycopg2.connect(
        dbname='news',
        user='vagrant',
        password='vagrant',
        host='localhost',
        port='5432'
        )
    cur = connect.cursor()
except Exception as e:
    print(e + "Error in connecting to database")


def report_most_popular_articles():
    # we get the most popular three articles of all time
    ''' CREATE VIEW log_slug as SELECT replace(path,'/article/','') as slug, count(*) as views
     FROM log
     WHERE path <> '/' AND status ='200 OK' GROUP BY path;'''
    psql = ''' select title, views from log_slug INNER JOIN articles on
    articles.slug = log_slug.slug order by views desc limit 3; '''
    cur.execute(psql)
    res = cur.fetchall()
    # Prints report
    print(" \n What are the most popular three articles of all time ? \n")
    for report in res:
        print(' "{0}"   ===>   {1} views'.format(report[0], report[1]))


def report_most_popular_authors():
    # Prints most popular article authors of all time
    '''
    CREATE VIEW authors_name as SELECT authors.name as name,
    articles.slug as slug
    FROM authors INNER JOIN articles
    ON articles.author=authors.id ORDER BY authors.id;

    CREATE VIEW log_slug as SELECT replace(path,'/article/','') as slug,
    count(*) as views
    FROM log
    WHERE path<>'/' AND status ='200 OK' GROUP BY path;
    '''
    psql = '''
    select authors_name.name as author,
    sum(log_slug.views) as views from log_slug join authors_name on
    authors_name.slug=log_slug.slug
    group by authors_name.name order by views desc;
    '''
    cur.execute(psql)
    reported = cur.fetchall()
    # Prints report
    print("\n Who are the most popular article authors of all time ? \n")
    for report in reported:
        print(' "{0}"   ===>   {1} views'.format(report[0], report[1]))


def report_log_error_percentage():
    # Prints Log errors percentage more than 1%
    '''
    CREATE VIEW log_fail as SELECT Date(time), count(Date(time))
    FROM log
    WHERE status='404 NOT FOUND' GROUP BY Date(time) ORDER BY Date(time);

    
    '''
    psql = '''
    select log_fail.date ,(log_fail.count*100.00 / log_total.count) as
    percentage from log_fail inner join log_total on
    log_fail.date = log_total.date
    where (log_fail.count*100.00 / log_total.count) >1
    order by (log_fail.count*100.00 / log_total.count) desc;
    '''
    cur.execute(psql)
    reported = cur.fetchall()
    # Prints report
    print(" \n Days on which more than 1% of requests lead to errors ? ")
    for report in reported:
        print(
            '\n ' + str(report[0]) +
            '   ===>   ' + '%.1f' % report[1] +
            '% errors\n'
            )

report_most_popular_articles()
report_most_popular_authors()
report_log_error_percentage()
cur.close()
connect.close()
