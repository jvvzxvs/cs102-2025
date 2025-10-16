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


    for char in plaintext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            shift = ord(key[key_idx % len(key)]) - ord('a')
            ciphertext += chr((ord(char) - base + shift) % 26 + base)
            key_idx += 1
        else: ciphertext += char
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

    for char in ciphertext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            shift = ord(key[key_idx % len(key)]) - ord('a')
            plaintext += chr((ord(char) - base - shift) % 26 + base)
            key_idx += 1
        else: plaintext += char
    return plaintext

    return plaintext