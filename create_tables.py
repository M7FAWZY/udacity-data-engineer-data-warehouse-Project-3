import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

#drop tables before recreate

def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

#create fresh tables
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    print('Connecting to redshift')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('Connected to redshift')
    cur = conn.cursor()
    
    print('Dropping existing tables if Exist')
    drop_tables(cur, conn)
    
    print('Creating tables')
    create_tables(cur, conn)
    
    #END of create_tables
    conn.close()
    print('Create table Ended')

if __name__ == "__main__":
    main()