

from typing import Iterable

ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UPPER = ALPHABET_LOWER.upper()
ALPHABET_SIZE = 26

def _shift_char(ch: str, shift: int) -> str:
    """
    Shift a single character by `shift` within A-Z or a-z.
    Non-letters are returned unchanged.
    """
    if 'a' <= ch <= 'z':
        idx = ord(ch) - ord('a')
        return chr(ord('a') + ((idx + shift) % ALPHABET_SIZE))
    if 'A' <= ch <= 'Z':
        idx = ord(ch) - ord('A')
        return chr(ord('A') + ((idx + shift) % ALPHABET_SIZE))
    return ch  # leave digits, spaces, punctuation as-is

def encrypt(text: str, shift: int) -> str:
    """Encrypt text using Caesar cipher with a right shift (positive)."""
    shift = shift % ALPHABET_SIZE
    return "".join(_shift_char(ch, shift) for ch in text)

def decrypt(text: str, shift: int) -> str:
    """Decrypt text by reversing the shift (or just call encrypt with -shift)."""
    return encrypt(text, -shift)

def bruteforce(text: str) -> Iterable[tuple[int, str]]:
    """
    Convenience helper: try all 26 shifts and yield (shift, candidate).
    Useful if someone forgot the key.
    """
    for s in range(ALPHABET_SIZE):
        yield (s, encrypt(text, -s))
