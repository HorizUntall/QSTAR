import hashlib
from core.config.config import get_data, change_data

def verify_password(pw: str) -> bool:
    entered_password = pw.encode('utf-8')
    _salt = get_data("scrypt_salt")
    _n = get_data("scrypt_n")
    _r = get_data("scrypt_r")
    _p = get_data("scrypt_p")
    
    input_key = hashlib.scrypt(password=entered_password,
                                salt=_salt,
                                n=_n,
                                r=_r,
                                p=_p
                               )
    return input_key == get_data("admin_key")

def change_pass(pw: str) -> None:
    entered_password = pw.encode('utf-8')
    _salt = get_data("scrypt_salt")
    _n = get_data("scrypt_n")
    _r = get_data("scrypt_r")
    _p = get_data("scrypt_p")

    new_key = hashlib.scrypt(password=entered_password,
                            salt=_salt,
                            n=_n,
                            r=_r,
                            p=_p
                            )
    
    change_data("admin_key", new_key)