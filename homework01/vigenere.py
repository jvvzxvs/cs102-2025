def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword.lower()
    if not keyword:
        return plaintext
    key_idx = 0
    key_len = len(key)

    for char in plaintext:
        shift = ord(key[key_idx % key_len]) - ord("a")
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            ciphertext += chr((ord(char) - base + shift) % 26 + base)
        else:
            ciphertext += char
        key_idx += 1

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    key = keyword.lower()
    if not keyword:
        return ciphertext
    key_idx = 0
    key_len = len(key)

    for char in ciphertext:
        shift = ord(key[key_idx % key_len]) - ord("a")
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            plaintext += chr((ord(char) - base - shift) % 26 + base)
        else:
            plaintext += char
        key_idx += 1

    return plaintext
