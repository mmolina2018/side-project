from database.psql import _get_db_targets

def BaseSuccess(result):
    return result
def BaseError(error):
    raise Exception("BaseError")

def get_targets(
    pos,
    object_id,
    radius,
    database,
    handle_success: BaseSuccess,
    handle_error: BaseError,
) -> dict[str, list]:
       

    result = _get_db_targets(pos,radius)  # probablementes aca se manejen las excepciones, agregar ademas el id del objeto a la salida.


    return result


