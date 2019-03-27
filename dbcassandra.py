# import external libraries
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra.concurrent import execute_concurrent, execute_concurrent_with_args
from cassandra import ConsistencyLevel


# connect to casandra
try:
    cluster = Cluster()
    session = cluster.connect()
    status = "Cassandra Success"
except Exception as e:
    status = "Cassandra Fail"
    print (e.message, e.args)

# initiate keyspace and table names as variables
KEYSPACE = "weather"
TABLENAME = "weatherTable"
# columns to be put on cassandra DB
# will be using csv i/o for improvement
CITYLIST = ['London', 'New York', 'Jakarta', 'Seoul', 'Tokyo', 'Paris']


# check and create keyspace, table
def table_exist():
    # create keyspace if not exist
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true
        """ % KEYSPACE)
    print ("{} has been created".format(KEYSPACE))
    # create table if not exist
    session.execute("""
        CREATE TABLE IF NOT EXISTS {}.{} (
            CityName text PRIMARY KEY,
            )""".format(KEYSPACE, TABLENAME))
    print ("{} has been created".format(TABLENAME))
    return status


# insert columns to DB
def insertData():
    # ---empty table
    session.execute("""
        TRUNCATE {}.{}""".format(KEYSPACE, TABLENAME))
    print ("{} has been emptied".format(TABLENAME))
    # ---inserting default table values
    parameters = [(x,) for x in CITYLIST]
    print(parameters)
    prepared = session.prepare(
        "INSERT INTO weather.weatherTable (CityName) VALUES (?)")
    execute_concurrent_with_args(session, prepared, parameters)
    print("done")


# search and return cityname in DB
def searchCity(citySearch):
    if citySearch == "def":
        print(citySearch)
        # find cityname and return all
        print("""Select * From {}.{}""".format(KEYSPACE, TABLENAME))
        search_stm = "Select * From {}.{}".format(KEYSPACE, TABLENAME)
        rows = session.execute(search_stm)
        list_data = []
        for weather in rows:
            list_data.append(weather.cityname)
        print(list_data)
        return (list_data)
    else:
        print(citySearch)
        # find and return 1 cityname
        print("""Select * From {}.{} where CityName = {}""".format(KEYSPACE,
                                                                   TABLENAME, citySearch))
        search_stm = "Select * From {}.{} where CityName = '{}'".format(
            KEYSPACE, TABLENAME, citySearch)
        rows = session.execute(search_stm)
        print(rows)
        for weather in rows:
            return weather.CityName
    return('<h1>Could not find city!</h1>')
