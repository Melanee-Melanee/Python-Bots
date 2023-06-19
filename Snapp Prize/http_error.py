class VoucherExceededException(Exception):
    def __init__(self, message="Voucher usage limit exceeded"):
        super().__init__(message)

class PhoneInvalidException(Exception):
    def __init__(self, message="not a valid cellphone"):
        super().__init__(message)
