import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    This function drop all the tables, before create any table, in the database.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function create all the tables we'll use, the staging and the analytics ones.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(config['CLUSTER']['HOST'],
                                                                                  config['CLUSTER']['DB_NAME'],
                                                                                  config['CLUSTER']['DB_USER'],
                                                                                  config['CLUSTER']['DB_PASSWORD'],
                                                                                  config['CLUSTER']['DB_PORT']))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()