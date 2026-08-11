import argparse
import hashlib
import sys
from pathlib import Path


SUPPORTED_ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
}


def get_hash(data, algorithm):
    """Generate a hash from bytes."""

    hash_function = SUPPORTED_ALGORITHMS.get(algorithm.lower())

    if hash_function is None:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    return hash_function(data).hexdigest()


def hash_text(text, algorithm):
    """Generate a hash from text."""

    data = text.encode("utf-8")

    return get_hash(data, algorithm)


def hash_file(file_path, algorithm):
    """Generate a hash from a file."""

    hash_function = SUPPORTED_ALGORITHMS.get(algorithm.lower())

    if hash_function is None:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    hasher = hash_function()

    try:
        with open(file_path, "rb") as file:

            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                hasher.update(chunk)

        return hasher.hexdigest()

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")


def verify_hash(file_path, expected_hash, algorithm):
    """Compare a file hash with an expected hash."""

    actual_hash = hash_file(file_path, algorithm)

    return actual_hash.lower() == expected_hash.lower()


def show_hash(value, algorithm, source):
    """Display the generated hash."""

    print("\n" + "=" * 60)
    print("                 HASH RESULT")
    print("=" * 60)

    print(f"Source    : {source}")
    print(f"Algorithm : {algorithm.upper()}")
    print(f"Hash      : {value}")

    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="Generate and verify cryptographic hashes."
    )

    parser.add_argument(
        "--text",
        help="Text to hash"
    )

    parser.add_argument(
        "--file",
        help="File to hash"
    )

    parser.add_argument(
        "--algorithm",
        default="sha256",
        choices=SUPPORTED_ALGORITHMS.keys(),
        help="Hashing algorithm"
    )

    parser.add_argument(
        "--verify",
        help="Expected hash for file verification"
    )

    args = parser.parse_args()

    if not args.text and not args.file:
        parser.error("Provide either --text or --file.")

    if args.text and args.file:
        parser.error("Use either --text or --file, not both.")

    try:

        if args.text:

            if args.verify:
                parser.error("--verify can only be used with --file.")

            result = hash_text(
                args.text,
                args.algorithm
            )

            show_hash(
                result,
                args.algorithm,
                "Text input"
            )

        elif args.file:

            file_path = Path(args.file)

            result = hash_file(
                file_path,
                args.algorithm
            )

            if args.verify:

                print("\n" + "=" * 60)
                print("              HASH VERIFICATION")
                print("=" * 60)

                print(f"File      : {file_path}")
                print(f"Algorithm : {args.algorithm.upper()}")
                print(f"Expected  : {args.verify}")
                print(f"Actual    : {result}")

                if result.lower() == args.verify.lower():
                    print("\nResult    : MATCH")
                    print("The file integrity check passed.")
                else:
                    print("\nResult    : MISMATCH")
                    print("The file may have been modified.")

                print("=" * 60)

            else:

                show_hash(
                    result,
                    args.algorithm,
                    str(file_path)
                )

    except (FileNotFoundError, PermissionError, ValueError) as error:

        print(f"\nError: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()