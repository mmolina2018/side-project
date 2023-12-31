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
        return f"Can't retrieve matches, username not recognized {self.user_id}"


class CredentialsError(BaseException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Credentials Error"

class CreateUserError(BaseException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "This user already exist"
