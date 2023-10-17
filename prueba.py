from database.psql import create_db
from api.result_handler import handle_error, handle_success 
from core.service import get_targets
db_config = {
    "name":"sideproject",
    "user":"myuser",
    "password":"pass",
    "host":"localhost",
    "port":"5432",
}

db = create_db(db_config)

salida = get_targets(user_id="2",database=db,handle_success= handle_success,handle_error= handle_error)
print (salida)