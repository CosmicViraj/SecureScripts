# File Integrity Monitor

A lightweight Python-based File Integrity Monitoring (FIM) tool that uses **SHA-256 hashing** to detect changes to files.

This project creates a trusted baseline of file hashes and compares it with later scans to identify **new, modified, or deleted files**.

It was built as a practical cybersecurity project to understand how file integrity monitoring can be used in a SOC environment.

---

## Features

* Create a trusted file integrity baseline
* Calculate SHA-256 hashes for files
* Detect modified files
* Detect newly created files
* Detect deleted files
* Store baseline hashes in JSON format
* Generate a simple integrity report
* Display scan timestamps
* Uses only Python standard libraries
* Simple command-line interface

---

## How It Works

The tool follows a simple process:

```text
             Files
                |
                v
        Calculate SHA-256
                |
                v
        Create Baseline
                |
                v
        Store File Hashes
                |
          Later Scan
                |
                v
        Calculate Hashes
                |
                v
        Compare With
          Baseline
                |
       +--------+--------+
       |        |        |
       v        v        v
     NEW     MODIFIED  DELETED
     FILE      FILE      FILE
       |        |        |
       +--------+--------+
                |
                v
        Integrity Report
```

If the contents of a file change, its SHA-256 hash changes as well. The tool uses this difference to identify possible file modifications.

---

## Technologies Used

* Python 3
* SHA-256
* JSON
* Command Line Interface
* Python `hashlib`
* Python `os`
* Python `argparse`

No external Python packages are required.

---

## Project Structure

```text
File-Integrity-Monitor/
│
├── file_integrity_monitor.py
├── README.md
├── .gitignore
│
└── test_files/
    └── example.txt
```

The local `file_hashes.json` file is intentionally excluded from Git because it represents the local baseline created during testing.

---

## Requirements

* Python 3.x
* Windows, Linux, or macOS

Check your Python installation:

```bash
python --version
```

On Windows, you can also use:

```cmd
py --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/CosmicViraj/SecureScripts.git
```

Go to the project directory:

```bash
cd SecureScripts/File-Integrity-Monitor
```

No additional packages are required.

---

## Usage

### 1. Create a Test Directory

Create a directory containing the files you want to monitor.

Example:

```text
test_files/
└── example.txt
```

---

### 2. Create the Baseline

Run:

```bash
python file_integrity_monitor.py --init test_files
```

On Windows:

```cmd
py file_integrity_monitor.py --init test_files
```

The program calculates a SHA-256 hash for each file and stores the results in:

```text
file_hashes.json
```

Example output:

```text
Creating baseline for: test_files

Hash database saved to file_hashes.json
Baseline created for 1 files.
```

---

### 3. Check File Integrity

Run:

```bash
python file_integrity_monitor.py --check test_files
```

Or on Windows:

```cmd
py file_integrity_monitor.py --check test_files
```

If nothing has changed:

```text
============================================================
             FILE INTEGRITY REPORT
============================================================

Scan time: 2026-08-11 15:30:00

[OK] No file changes detected.

============================================================
```

---

## Testing File Modification

Open the test file:

```cmd
notepad test_files\example.txt
```

Change its contents and save it.

Run:

```cmd
py file_integrity_monitor.py --check test_files
```

The tool will detect the modification:

```text
[!] MODIFIED FILES
    test_files\example.txt
```

---

## Testing New Files

Create another file:

```cmd
notepad test_files\new_file.txt
```

Then run:

```cmd
py file_integrity_monitor.py --check test_files
```

The tool reports:

```text
[+] NEW FILES
    test_files\new_file.txt
```

---

## Testing Deleted Files

Delete a monitored file:

```cmd
del test_files\example.txt
```

Then run:

```cmd
py file_integrity_monitor.py --check test_files
```

The tool reports:

```text
[-] DELETED FILES
    test_files\example.txt
```

---

## Detection Logic

The tool compares the previous and current file lists.

### New File

A file exists in the latest scan but not in the baseline.

```text
New Files = Current Files - Previous Files
```

### Deleted File

A file exists in the baseline but is missing from the latest scan.

```text
Deleted Files = Previous Files - Current Files
```

### Modified File

A file exists in both scans, but its SHA-256 hash has changed.

```text
Old Hash != New Hash
```

---

## Example Scenario

Suppose the baseline contains:

```text
example.txt
config.txt
database.txt
```

During the next scan:

```text
example.txt       → unchanged
config.txt        → modified
database.txt      → deleted
malware_test.txt  → new
```

The monitor reports:

```text
[+] NEW FILES

    malware_test.txt


[-] DELETED FILES

    database.txt


[!] MODIFIED FILES

    config.txt
```

A SOC analyst can then investigate these events to determine whether the changes are legitimate or suspicious.

---

## SOC Use Case

File Integrity Monitoring is useful in security monitoring because unexpected changes to important files can indicate:

* Unauthorized modifications
* Malware activity
* Configuration changes
* Suspicious file creation
* Possible compromise
* Tampering with system files

In a SOC environment, the results of a FIM tool could be combined with other security telemetry such as endpoint logs, authentication events, network activity, and SIEM alerts.

---

## Future Improvements

Possible improvements for future versions include:

* Real-time file monitoring
* Windows Event Log integration
* Linux audit log integration
* Email alerts
* Wazuh integration
* SIEM integration
* Severity classification
* CSV/JSON incident reports
* File exclusion rules
* Directory-specific monitoring
* Automated incident reports
* Web dashboard
* Scheduled integrity scans

---

## Security Note

This project is intended for **authorized systems and files only**.

The baseline should be created from a trusted state. If the baseline itself is compromised, the integrity results may no longer be reliable.

For real-world deployment, additional protections should be used to protect the baseline database and monitoring process.

---

## Learning Objectives

This project helped me understand:

* How cryptographic hashing works
* SHA-256 file integrity checking
* Baseline-based monitoring
* File change detection
* Security event identification
* Basic SOC investigation concepts
* Python file handling
* Command-line application development

---

## Author

**Viraj Jadhav**

BCA Graduate | Cybersecurity & IT

GitHub:
https://github.com/CosmicViraj

LinkedIn:
https://linkedin.com/in/virajjadhav03

---

## License

This project is intended for educational and cybersecurity learning purposes.
