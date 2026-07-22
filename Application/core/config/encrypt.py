import win32crypt

def encrypt_data(data: bytes) -> bytes:
    """Encrypts raw bytes using Windows DPAPI."""
    if not isinstance(data, bytes):
        raise TypeError("Input must be bytes")
        
    encrypted_bytes = win32crypt.CryptProtectData(data, "", None, None, None, 0)
    return encrypted_bytes

def decrypt_data(encrypted_data: bytes) -> bytes:
    """Decrypts DPAPI-encrypted bytes."""
    if not isinstance(encrypted_data, bytes):
        raise TypeError("Input must be bytes")
        
    _, decrypted = win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)
    return decrypted