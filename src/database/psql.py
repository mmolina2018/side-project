import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from typing import Optional

db_config = {
    "name": "sideproject",
    "user": "postgres",
    "password": "pass",
    "host": "localhost",
    "port": "5432",
}


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


@contextmanager
def session(DatabaseError, handle_error):
    session = connection_pool.getconn()
    try:
        yield session
    except DatabaseError as e:
        session.rollback()
        return handle_error(e)

    finally:
        connection_pool.putconn(session)


def _get_db_targets(user_id, conn) -> Optional[list]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT m.match_id, m.target_id, m.info FROM match m JOIN targets t ON m.target_id = t.target_id WHERE t.user_id = %s ORDER BY m.target_id",
            (user_id,),
        )
        result = cur.fetchall()

    return result


def _get_db_credentials(user, password, conn) -> Optional[str]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT user_id FROM users WHERE username = %s AND password = %s",
            (user, password),
        )
        result = cur.fetchone()

    return result
