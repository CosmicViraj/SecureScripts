# Email Header Analyzer

A lightweight Python-based cybersecurity tool for analyzing email headers and identifying common indicators associated with suspicious or potentially malicious emails.

## Features

* Extracts basic email header information
* Analyzes `From`, `Reply-To`, and `Return-Path`
* Compares sender and reply domains
* Checks SPF, DKIM, and DMARC results
* Extracts IP addresses from `Received` headers
* Displays the email's mail-server path
* Identifies missing or suspicious headers
* Provides a basic risk score
* Assigns a simple risk level: Low, Medium, or High

## Technologies

* Python 3
* Python Standard Library
* Email Header Analysis
* Basic IOC Analysis
* Email Security

## How It Works

```text
Email (.eml)
     |
     v
Header Extraction
     |
     v
Domain Analysis
     |
     +----> From / Reply-To
     |
     +----> Return-Path
     |
     +----> SPF / DKIM / DMARC
     |
     +----> Received Headers
     |
     v
Security Checks
     |
     v
Risk Assessment
```

## Installation

Clone the repository:

```bash
git clone https://github.com/CosmicViraj/SecureScripts.git
```

Move into the project:

```bash
cd SecureScripts/Email-Header-Analyzer
```

No external Python packages are required.

## Usage

Run the analyzer against an `.eml` file:

```bash
python email_header_analyzer.py sample.eml
```

On Windows, you can also use:

```bash
py email_header_analyzer.py sample.eml
```

## Example Investigation

The analyzer can help identify situations such as:

* A `Reply-To` domain that differs from the sender domain
* SPF authentication failures
* DKIM authentication failures
* DMARC failures
* Unexpected mail-server paths
* Missing authentication information

These findings should be treated as investigation indicators rather than automatic proof that an email is malicious.

## Security Use Case

This project is designed as a small SOC-oriented investigation tool. It can be used to practice:

* Email security analysis
* IOC identification
* Header investigation
* Authentication-result analysis
* Initial phishing investigation
* Incident documentation

## Disclaimer

This tool is intended for educational and defensive security research. Analyze only emails and systems that you are authorized to inspect.

## Future Improvements

* IP geolocation
* WHOIS/domain information
* DNS checks
* URL extraction
* URL reputation checks
* VirusTotal integration
* HTML report generation
* Web-based interface
* Automated IOC extraction
* MITRE ATT&CK mapping
