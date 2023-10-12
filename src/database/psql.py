import psycopg2
from psycopg2 import pool
from config import db_config

# crear database

    
db_name = db_config["name"]
db_user = db_config["user"]
db_pass = db_config["password"]
db_port = db_config["port"]

connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=db_name,
    user=db_user,
    password=db_pass,
    port=db_port,
)





def _get_db_targets(pos, radius):

    radius_2 = radius ** 2
    connection = connection_pool.getconn()
    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM objects WHERE ((x - {pos[0]})^2 + (y - {pos[1]})^2) < {radius_2};") # la consulta va a cambiar
        result = cur.fetchall()
    
    connection_pool.putconn(connection)
    return result