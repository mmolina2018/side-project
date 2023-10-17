class WrapperException(BaseException):
    def __init__(self, original_e, subcode=None):
        super().__init__()
        self.original_exception = original_e
        self.subcode = subcode

    def __str__(self) -> str:
        return self.original_exception.__str__()


class DatabaseError(WrapperException):
    def __init__(self, original_e, subcode=None):
        super().__init__(original_e, subcode)


class UserIdError(Exception):
    def __init__(self, user_id) -> None:
        super().__init__()
        self.user_id = user_id

    def __str__(self) -> str:
        return f"Can't retrieve matches, user_id not recognized {self.user_id}"
