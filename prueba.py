from database.psql import session
from api.result_handler import handle_error, handle_success
from core.service import get_targets

salida = get_targets(
    user_id="1", session=session, handle_success=handle_success, handle_error=handle_error
)
print(salida)
