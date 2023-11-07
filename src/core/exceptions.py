class DatabaseError(BaseException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Database Error"

class UserIdError(BaseException):
    def __init__(self, user_id) -> None:
        super().__init__()
        self.user_id = user_id

    def __str__(self) -> str:
        return f"Can't retrieve matches, user_id not recognized {self.user_id}"
    
class InvalidTokenError(BaseException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Your token isn't valid"    

class TokenNoAutorizado(BaseException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "You shall not pass"