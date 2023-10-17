import psycopg2
from psycopg2 import pool

def create_db(db_config):
    db_name = db_config["name"]
    db_user = db_config["user"]
    db_pass = db_config["password"]
    db_port = db_config["port"]
    db_host = db_config["host"]

    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        dbname=db_name,
        user=db_user,
        password=db_pass,
        port=db_port,
        host=db_host,
    )
    return connection_pool


def _get_db_targets(user_id, database):
    connection = database.getconn()
    with connection.cursor() as cur:
        cur.execute(
            "SELECT m.match_id, m.target_id, m.info FROM match m JOIN targets t ON m.target_id = t.target_id WHERE t.user_id = %s",
            (user_id,),
        )
        result = cur.fetchall()

    database.putconn(connection)
    return result
