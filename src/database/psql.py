import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from typing import Optional, Tuple

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


def _get_db_targets(username, conn) -> Optional[list]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT m.match_id, m.target_id, m.info FROM match m JOIN targets t ON m.target_id = t.target_id WHERE t.username = %s ORDER BY m.target_id",
            (username,),
        )
        result = cur.fetchall()

    return result


def _get_db_credentials(user, conn) -> Optional[Tuple]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT pass FROM users WHERE username = %s",
            (user,),
        )
        result = cur.fetchone()

    return result

def _create_db_user(user, password, conn, error) -> Optional[str]:
    print([user,password])
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, pass) VALUES (%s, %s);",
                (user, password),
            )
            conn.commit()
            result = f"The user: {user} was successfully created"
        return result
    except:
        raise error