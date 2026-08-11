import hashlib
import json
import os
import sys
from datetime import datetime


HASH_FILE = "file_hashes.json"


def calculate_hash(file_path):
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except (PermissionError, OSError) as error:
        print(f"Could not read {file_path}: {error}")
        return None


def scan_directory(folder):
    """Scan a directory and create a dictionary of file hashes."""

    file_hashes = {}

    for root, directories, files in os.walk(folder):

        # Ignore the hash database itself
        if HASH_FILE in files:
            files.remove(HASH_FILE)

        for file_name in files:

            file_path = os.path.join(root, file_name)

            file_hash = calculate_hash(file_path)

            if file_hash:
                file_hashes[file_path] = file_hash

    return file_hashes


def save_hashes(file_hashes):
    """Save file hashes to a JSON file."""

    with open(HASH_FILE, "w") as file:
        json.dump(file_hashes, file, indent=4)

    print(f"\nHash database saved to {HASH_FILE}")


def load_hashes():
    """Load the previous hash database."""

    if not os.path.exists(HASH_FILE):
        return {}

    try:
        with open(HASH_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Hash database is damaged or invalid.")
        return {}


def compare_hashes(old_hashes, new_hashes):
    """Compare old and new hashes and report changes."""

    old_files = set(old_hashes.keys())
    new_files = set(new_hashes.keys())

    added_files = new_files - old_files
    deleted_files = old_files - new_files

    modified_files = []

    for file_path in old_files.intersection(new_files):

        if old_hashes[file_path] != new_hashes[file_path]:
            modified_files.append(file_path)

    print("\n" + "=" * 60)
    print("             FILE INTEGRITY REPORT")
    print("=" * 60)

    print(f"\nScan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if added_files:
        print("\n[+] NEW FILES")

        for file_path in sorted(added_files):
            print(f"    {file_path}")

    if deleted_files:
        print("\n[-] DELETED FILES")

        for file_path in sorted(deleted_files):
            print(f"    {file_path}")

    if modified_files:
        print("\n[!] MODIFIED FILES")

        for file_path in sorted(modified_files):
            print(f"    {file_path}")

    if not added_files and not deleted_files and not modified_files:
        print("\n[OK] No file changes detected.")

    print("\n" + "=" * 60)


def create_baseline(folder):
    """Create the first trusted file baseline."""

    print(f"\nCreating baseline for: {folder}")

    file_hashes = scan_directory(folder)

    if not file_hashes:
        print("No files were found.")
        return

    save_hashes(file_hashes)

    print(f"Baseline created for {len(file_hashes)} files.")


def check_integrity(folder):
    """Scan the directory and compare it with the saved baseline."""

    old_hashes = load_hashes()

    if not old_hashes:
        print("\nNo baseline found.")
        print("Create one first using:")
        print("python file_integrity_monitor.py --init <folder>")
        return

    print(f"\nScanning: {folder}")

    new_hashes = scan_directory(folder)

    compare_hashes(old_hashes, new_hashes)


def show_help():
    print("""
File Integrity Monitor
----------------------

Create a baseline:
    python file_integrity_monitor.py --init test_files

Check file integrity:
    python file_integrity_monitor.py --check test_files

Examples:

    python file_integrity_monitor.py --init C:\\Users\\Viraj\\Documents\\test

    python file_integrity_monitor.py --check C:\\Users\\Viraj\\Documents\\test
""")


def main():

    if len(sys.argv) != 3:
        show_help()
        return

    command = sys.argv[1]
    folder = sys.argv[2]

    if not os.path.isdir(folder):
        print(f"Directory does not exist: {folder}")
        return

    if command == "--init":

        create_baseline(folder)

    elif command == "--check":

        check_integrity(folder)

    else:

        show_help()


if __name__ == "__main__":
    main()