#!/usr/bin/env python
import psycopg2

''' Below lines helps us Connect to the PostgreSQL DB
    if not, rasies exception'''
connector = psycopg2.connect(
        dbname='news',
        user='vagrant',
        password='vagrant',
        host='localhost',
        port='5432'
        )
cur = connector.cursor()

''' YOU SHOULD IMPORT views.sql and newsdata.sql USING
    COMMAND

    psql -d databasename -f filename.sql
'''

''' suggested by udacity reviewer '''


def execute_query(query):
    """
    execute_query takes an SQL query as a parameter,
    executes the query and returns the results as a list of tuples.

    args:
      query - (string) an SQL query statement to be executed.

    returns:
      A list of tuples containing the results of the query.
    """
    try:
        cur.execute(query)
        results = cur.fetchall()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def report_log_error_percentage():
    '''
    Prints Log errors percentage more than 1%
    For this report i used two views,

    log_total, this view contains total no.of logs(success + fail)
        as count  and their dates as date.
    log_fail, this view contains no.of failed logs
        as count and their dates as date.
    '''

    psql = '''
    SELECT log_fail.date ,(log_fail.count*100.00 / log_total.count) AS
    percentage FROM log_fail INNER JOIN log_total
    ON log_fail.date = log_total.date
    AND (log_fail.count*100.00 / log_total.count) >1
    ORDER BY (log_fail.count*100.00 / log_total.count) desc;
    '''

    ''' calling function execute_query(args)
        to excute and fetch data as list in return
    '''
    reported = execute_query(psql)

    '''Prints report'''
    print(" \n  3. Days on which more than 1% of requests lead to errors ? ")
    for report in reported:
        print(
            '\n  On ' + str(report[0]) +
            '   ===>   ' + '%.1f' % report[1] +
            '% errors\n'
            )


def report_most_popular_authors():
    '''
    Prints most popular article authors of all time
    For this report i used two views,

    log_slug, this view contains  log-path that has replaced
        such a way to get slug as slug and their count as views.
    authors_name, this view contains
        author-name as name and articles-slug as slug.
    '''

    psql = '''
    SELECT authors_name.name AS author,
    sum(log_slug.views) AS views FROM log_slug INNER JOIN authors_name
    ON authors_name.slug=log_slug.slug
    GROUP BY authors_name.name ORDER BY views desc;
    '''

    ''' calling function execute_query(args)
        to excute and fetch data as list in return
    '''
    reported = execute_query(psql)

    ''' Prints report '''
    print("\n  2. Who are the most popular article authors of all time ? \n")
    for report in reported:
        print('  "{0}"   ===>   {1} views'.format(report[0], report[1]))


def report_most_popular_articles():
    '''
    we get the most popular three articles of all time
    For this report i used a view,

    log_slug, this view contains  log-path that has replaced
        such a way to get slug as slug and their count as views.
    '''

    psql = ''' SELECT title, views FROM log_slug INNER JOIN articles ON
    articles.slug = log_slug.slug ORDER BY views desc LIMIT 3; '''

    ''' calling function execute_query(args)
        to excute and fetch data as list in return
    '''
    reported = execute_query(psql)

    ''' Prints report '''
    print(" \n  1. What are the most popular three articles of all time ? \n")
    for report in reported:
        print('  "{0}"   ===>   {1} views'.format(report[0], report[1]))

''' suggested by udacity reviewer '''


def main():
    report_most_popular_articles()
    report_most_popular_authors()
    report_log_error_percentage()
    cur.close()
    connector.close()


if __name__ == '__main__':
    main()
