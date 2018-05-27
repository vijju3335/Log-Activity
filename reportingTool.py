#!/usr/bin/env python
import psycopg2

# Below lines helps us Connect to the PostgreSQL DB if not, rasies exception
connector = psycopg2.connect(
        dbname='news',
        user='vagrant',
        password='vagrant',
        host='localhost',
        port='5432'
        )
cur = connector.cursor()


def report_log_error_percentage():
    # Prints Log errors percentage more than 1%
    '''
    CREATE VIEW log_fail as SELECT Date(time), count(Date(time))
    FROM log
    WHERE status='404 NOT FOUND' GROUP BY Date(time) ORDER BY Date(time);


    '''
    psql = '''
    SELECT log_fail.date ,(log_fail.count*100.00 / log_total.count) AS
    percentage FROM log_fail INNER JOIN log_total
    ON log_fail.date = log_total.date
    AND (log_fail.count*100.00 / log_total.count) >1
    ORDER BY (log_fail.count*100.00 / log_total.count) desc;
    '''
    cur.execute(psql)
    reported = cur.fetchall()
    # Prints report
    print(" \n  3. Days on which more than 1% of requests lead to errors ? ")
    for report in reported:
        print(
            '\n  On ' + str(report[0]) +
            '   ===>   ' + '%.1f' % report[1] +
            '% errors\n'
            )


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
    SELECT authors_name.name AS author,
    sum(log_slug.views) AS views FROM log_slug INNER JOIN authors_name
    ON authors_name.slug=log_slug.slug
    GROUP BY authors_name.name ORDER BY views desc;
    '''
    cur.execute(psql)
    reported = cur.fetchall()
    # Prints report
    print("\n  2. Who are the most popular article authors of all time ? \n")
    for report in reported:
        print('  "{0}"   ===>   {1} views'.format(report[0], report[1]))


def report_most_popular_articles():
    # we get the most popular three articles of all time
    '''
    CREATE VIEW log_slug as SELECT replace(path,'/article/','') AS slug,
    count(*) AS views FROM log
    WHERE path <> '/' AND status ='200 OK' GROUP BY path;
    '''
    psql = ''' SELECT title, views FROM log_slug INNER JOIN articles ON
    articles.slug = log_slug.slug ORDER BY views desc LIMIT 3; '''
    cur.execute(psql)
    res = cur.fetchall()
    # Prints report
    print(" \n  1. What are the most popular three articles of all time ? \n")
    for report in res:
        print('  "{0}"   ===>   {1} views'.format(report[0], report[1]))


report_most_popular_articles()
report_most_popular_authors()
report_log_error_percentage()
cur.close()
connector.close()
