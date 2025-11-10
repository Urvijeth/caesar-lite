# src/cli.py
import argparse
from pathlib import Path
from .caesar import encrypt, decrypt
from .fileio import read_text, write_text

def run_cli(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="caesar-lite",
        description="Encrypt/Decrypt text or a file using the Caesar cipher."
    )
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], required=True,
                        help="Operation to perform.")
    parser.add_argument("--shift", type=int, required=True,
                        help="Shift/key (e.g., 3).")

    src_group = parser.add_mutually_exclusive_group(required=True)
    src_group.add_argument("--text", type=str,
                           help="Plain text to process directly.")
    src_group.add_argument("--in", dest="infile", type=Path,
                           help="Input file path.")

    parser.add_argument("--out", dest="outfile", type=Path,
                        help="Output file path (required if using --in).")

    args = parser.parse_args(argv)

    # choose function
    func = encrypt if args.mode == "encrypt" else decrypt

    if args.text is not None:
        # process direct text and print result
        result = func(args.text, args.shift)
        print(result)
        return 0

    # file mode
    if args.infile and not args.outfile:
        parser.error("--out is required when using --in")

    data = read_text(str(args.infile))
    result = func(data, args.shift)
    write_text(str(args.outfile), result)
    print(f"Written: {args.outfile}")
    return 0

if __name__ == "__main__":
    raise SystemExit(run_cli())
