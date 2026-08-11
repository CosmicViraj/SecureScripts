import re
import sys
from email import policy
from email.parser import BytesParser


def read_email_file(file_name):
    """Read an email file and return the parsed message."""
    try:
        with open(file_name, "rb") as file:
            return BytesParser(policy=policy.default).parse(file)
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return None
    except Exception as error:
        print(f"Could not read the email: {error}")
        return None


def get_domain(address):
    """Get the domain part from an email address."""
    if not address:
        return ""

    match = re.search(r"@([\w.-]+)", address)
    if match:
        return match.group(1).lower()

    return ""


def find_ip(text):
    """Find an IPv4 address inside a string."""
    if not text:
        return None

    pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    match = re.search(pattern, text)

    return match.group(0) if match else None


def check_authentication(message):
    """Check SPF, DKIM and DMARC results."""
    auth_result = message.get("Authentication-Results", "")

    results = {
        "SPF": "Not found",
        "DKIM": "Not found",
        "DMARC": "Not found"
    }

    if auth_result:
        auth_lower = auth_result.lower()

        spf = re.search(r"spf=(pass|fail|softfail|neutral|none|temperror|permerror)",
                        auth_lower)
        dkim = re.search(r"dkim=(pass|fail|none|neutral|temperror|permerror)",
                         auth_lower)
        dmarc = re.search(r"dmarc=(pass|fail|none|bestguesspass|temperror|permerror)",
                          auth_lower)

        if spf:
            results["SPF"] = spf.group(1)

        if dkim:
            results["DKIM"] = dkim.group(1)

        if dmarc:
            results["DMARC"] = dmarc.group(1)

    return results


def analyze_received_headers(message):
    """Extract useful information from Received headers."""
    received_headers = message.get_all("Received", [])

    hops = []

    for number, received in enumerate(received_headers, start=1):
        ip = find_ip(received)

        hops.append({
            "hop": number,
            "ip": ip,
            "details": received.strip()
        })

    return hops


def print_header(title, value):
    print(f"{title:<20}: {value}")


def analyze_email(message):
    print("\n" + "=" * 65)
    print("              EMAIL HEADER ANALYZER")
    print("=" * 65)

    from_address = message.get("From", "")
    reply_to = message.get("Reply-To", "")
    return_path = message.get("Return-Path", "")
    subject = message.get("Subject", "")
    message_id = message.get("Message-ID", "")
    date = message.get("Date", "")
    sender = message.get("Sender", "")
    auth_results = message.get("Authentication-Results", "")

    print("\n[ BASIC INFORMATION ]")
    print_header("From", from_address)
    print_header("Reply-To", reply_to)
    print_header("Return-Path", return_path)
    print_header("Sender", sender)
    print_header("Subject", subject)
    print_header("Date", date)
    print_header("Message-ID", message_id)

    print("\n[ DOMAIN INFORMATION ]")

    from_domain = get_domain(from_address)
    reply_domain = get_domain(reply_to)
    return_domain = get_domain(return_path)

    print_header("From Domain", from_domain or "Unknown")
    print_header("Reply-To Domain", reply_domain or "Not present")
    print_header("Return-Path Domain", return_domain or "Unknown")

    print("\n[ AUTHENTICATION ]")

    auth = check_authentication(message)

    print_header("SPF", auth["SPF"])
    print_header("DKIM", auth["DKIM"])
    print_header("DMARC", auth["DMARC"])

    print("\n[ RECEIVED SERVERS ]")

    received = analyze_received_headers(message)

    if not received:
        print("No Received headers found.")
    else:
        for hop in received:
            print(f"\nHop {hop['hop']}")

            if hop["ip"]:
                print(f"IP      : {hop['ip']}")

            print(f"Details : {hop['details']}")

    print("\n[ QUICK CHECKS ]")

    warnings = []

    # Check Reply-To mismatch
    if from_domain and reply_domain:
        if from_domain != reply_domain:
            warnings.append(
                "From and Reply-To domains are different."
            )

    # Check Return-Path mismatch
    if from_domain and return_domain:
        if from_domain != return_domain:
            warnings.append(
                "From and Return-Path domains are different."
            )

    # Authentication checks
    if auth["SPF"] in ["fail", "softfail", "permerror"]:
        warnings.append(f"SPF result is {auth['SPF']}.")

    if auth["DKIM"] in ["fail", "permerror"]:
        warnings.append(f"DKIM result is {auth['DKIM']}.")

    if auth["DMARC"] in ["fail", "permerror"]:
        warnings.append(f"DMARC result is {auth['DMARC']}.")

    if not message_id:
        warnings.append("Message-ID header is missing.")

    if not auth_results:
        warnings.append("Authentication-Results header is missing.")

    if warnings:
        for warning in warnings:
            print(f"[!] {warning}")
    else:
        print("[+] No obvious header problems found.")

    print("\n[ RISK ASSESSMENT ]")

    risk_score = 0

    for warning in warnings:
        if "SPF" in warning:
            risk_score += 2
        elif "DKIM" in warning:
            risk_score += 2
        elif "DMARC" in warning:
            risk_score += 3
        elif "Reply-To" in warning:
            risk_score += 2
        elif "Return-Path" in warning:
            risk_score += 1
        else:
            risk_score += 1

    if risk_score >= 5:
        risk = "HIGH"
    elif risk_score >= 3:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    print_header("Risk Score", risk_score)
    print_header("Risk Level", risk)

    print("\n" + "=" * 65)


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python email_header_analyzer.py email.eml")
        return

    file_name = sys.argv[1]

    message = read_email_file(file_name)

    if message is None:
        return

    analyze_email(message)


if __name__ == "__main__":
    main()