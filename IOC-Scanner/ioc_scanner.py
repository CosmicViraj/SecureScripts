import argparse
import hashlib
import ipaddress
import json
import re
from pathlib import Path


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(8192)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, OSError):
        return None


def load_iocs(ioc_file):
    """Load IOC values from a JSON file."""

    try:
        with open(ioc_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "hashes": {
                value.lower()
                for value in data.get("hashes", [])
            },
            "ips": {
                value.lower()
                for value in data.get("ips", [])
            },
            "domains": {
                value.lower()
                for value in data.get("domains", [])
            },
            "urls": {
                value.lower()
                for value in data.get("urls", [])
            }
        }

    except FileNotFoundError:
        print(f"IOC file not found: {ioc_file}")
        return None

    except json.JSONDecodeError:
        print(f"Invalid JSON file: {ioc_file}")
        return None


def find_indicators(text, iocs):
    """Search text for known IPs, domains and URLs."""

    findings = []

    text_lower = text.lower()

    for url in iocs["urls"]:
        if url in text_lower:
            findings.append(("URL", url))

    for domain in iocs["domains"]:
        if domain in text_lower:
            findings.append(("DOMAIN", domain))

    for ip in iocs["ips"]:
        if ip in text_lower:
            findings.append(("IP", ip))

    return findings


def scan_file(file_path, iocs):
    """Scan one file for hash and text-based IOCs."""

    findings = []

    file_hash = calculate_sha256(file_path)

    if file_hash and file_hash.lower() in iocs["hashes"]:
        findings.append(
            ("SHA256", file_hash)
        )

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            content = file.read()

        findings.extend(
            find_indicators(content, iocs)
        )

    except (PermissionError, OSError):
        pass

    return findings


def scan_directory(directory, iocs):
    """Recursively scan files inside a directory."""

    results = []

    directory = Path(directory)

    if not directory.exists():
        print(f"Directory not found: {directory}")
        return results

    for file_path in directory.rglob("*"):

        if not file_path.is_file():
            continue

        findings = scan_file(
            file_path,
            iocs
        )

        if findings:
            results.append(
                {
                    "file": str(file_path),
                    "findings": findings
                }
            )

    return results


def print_results(results):
    """Display scan results."""

    print("\n" + "=" * 65)
    print("                    IOC SCAN REPORT")
    print("=" * 65)

    if not results:
        print("\n[OK] No matching indicators were found.")
        print("=" * 65)
        return

    print(f"\n[!] Suspicious files: {len(results)}")

    for result in results:

        print("\n" + "-" * 65)
        print(f"File: {result['file']}")

        for indicator_type, indicator in result["findings"]:
            print(
                f"  [{indicator_type}] {indicator}"
            )

    print("\n" + "=" * 65)


def save_report(results, output_file):
    """Save scan results as JSON."""

    report = {
        "scanner": "SecureScripts IOC Scanner",
        "files_with_findings": len(results),
        "results": results
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=4
        )

    print(f"\nReport saved to: {output_file}")


def main():

    parser = argparse.ArgumentParser(
        description="Scan files and directories for known IOCs."
    )

    parser.add_argument(
        "--target",
        required=True,
        help="File or directory to scan"
    )

    parser.add_argument(
        "--ioc",
        required=True,
        help="JSON file containing known IOCs"
    )

    parser.add_argument(
        "--output",
        help="Optional JSON report file"
    )

    args = parser.parse_args()

    iocs = load_iocs(args.ioc)

    if iocs is None:
        return

    target = Path(args.target)

    print("\nStarting IOC scan...")
    print(f"Target: {target}")

    if target.is_file():

        findings = scan_file(
            target,
            iocs
        )

        results = []

        if findings:
            results.append(
                {
                    "file": str(target),
                    "findings": findings
                }
            )

    elif target.is_dir():

        results = scan_directory(
            target,
            iocs
        )

    else:
        print(f"Target not found: {target}")
        return

    print_results(results)

    if args.output:
        save_report(
            results,
            args.output
        )


if __name__ == "__main__":
    main()