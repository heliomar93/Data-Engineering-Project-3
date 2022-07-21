import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This function load the data from JSON files into staging tables.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    This function extract, transform and load data from staging tables into the analytics tables.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This function execute the load_staging_tables and insert_tables functions. It means that this function insert the data     into the staging tables and extract, transform and laod the data into the analytics tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(config['CLUSTER']['HOST'],
                                                                                  config['CLUSTER']['DB_NAME'],
                                                                                  config['CLUSTER']['DB_USER'],
                                                                                  config['CLUSTER']['DB_PASSWORD'],
                                                                                  config['CLUSTER']['DB_PORT']))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()