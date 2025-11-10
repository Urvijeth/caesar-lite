

def read_text(filepath: str) -> str:
    """
    Read text from a file using UTF-8, fallback to Latin-1 if needed.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="latin-1") as f:
            return f.read()


def write_text(filepath: str, data: str) -> None:
    """
    Write text safely to a file using UTF-8 encoding.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)
