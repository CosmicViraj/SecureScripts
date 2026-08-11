# Hash Generator

A lightweight Python command-line tool for generating and verifying cryptographic hashes of text and files.

The project supports multiple hashing algorithms and can be used to verify whether a file has been modified by comparing its current hash with a previously generated hash.

This project was built as part of my cybersecurity learning journey to understand **cryptographic hashing, file integrity, and verification**.

---

## Features

* Generate hashes from text
* Generate hashes from files
* Verify file integrity
* Compare an existing hash with a newly calculated hash
* Supports multiple hashing algorithms
* SHA-256 is used as the default algorithm
* Simple command-line interface
* No external Python packages required

---

## Supported Algorithms

The tool currently supports:

```text
MD5
SHA-1
SHA-224
SHA-256
SHA-384
SHA-512
```

For modern integrity verification, **SHA-256 or SHA-512** is recommended.

MD5 and SHA-1 are included mainly for learning and compatibility purposes and should not be relied upon for modern cryptographic security.

---

## How It Works

The basic process is:

```text
             Input
          /          \
       Text           File
        |               |
        v               v
    Convert to       Read file
      bytes          in chunks
        |               |
        +-------+-------+
                |
                v
          Hash Algorithm
                |
                v
          Hash Calculation
                |
                v
           Hash Output
```

For file verification:

```text
Original Hash
     |
     v
Expected Hash
     |
     |
     v
Current File
     |
     v
Calculate New Hash
     |
     v
Compare Both Hashes
     |
   +---+---+
   |       |
 MATCH   MISMATCH
   |       |
   v       v
  OK    File may have
        been modified
```

---

## Technologies Used

* Python 3
* `hashlib`
* `argparse`
* `pathlib`
* Command Line Interface

The project uses only Python's standard library.

---

## Project Structure

```text
Hash-Generator/
│
├── hash_generator.py
└── README.md
```

Test files such as `test.txt` are used only for local testing and are not required by the application.

---

## Requirements

* Python 3.x
* Windows, Linux, or macOS

Check your Python version:

```bash
python --version
```

On Windows:

```cmd
py --version
```

No additional packages are required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/CosmicViraj/SecureScripts.git
```

Navigate to the project:

```bash
cd SecureScripts/Hash-Generator
```

---

# Usage

## Generate a Hash From Text

The default algorithm is SHA-256.

```cmd
py hash_generator.py --text "Hello Viraj"
```

Example:

```text
============================================================
                 HASH RESULT
============================================================
Source    : Text input
Algorithm : SHA256
Hash      : <generated_hash>
============================================================
```

---

## Select a Different Algorithm

### MD5

```cmd
py hash_generator.py --text "Hello Viraj" --algorithm md5
```

### SHA-1

```cmd
py hash_generator.py --text "Hello Viraj" --algorithm sha1
```

### SHA-256

```cmd
py hash_generator.py --text "Hello Viraj" --algorithm sha256
```

### SHA-512

```cmd
py hash_generator.py --text "Hello Viraj" --algorithm sha512
```

---

# Hash a File

Create a file for testing:

```cmd
notepad test.txt
```

Add some text, save the file, and run:

```cmd
py hash_generator.py --file test.txt
```

The program calculates the SHA-256 hash of the file.

Example:

```text
============================================================
                 HASH RESULT
============================================================
Source    : test.txt
Algorithm : SHA256
Hash      : <generated_hash>
============================================================
```

---

# Verify File Integrity

First calculate the file hash:

```cmd
py hash_generator.py --file test.txt
```

Copy the generated hash.

Then run:

```cmd
py hash_generator.py --file test.txt --verify YOUR_HASH_HERE
```

If the file has not changed:

```text
============================================================
              HASH VERIFICATION
============================================================

File      : test.txt
Algorithm : SHA256
Expected  : <expected_hash>
Actual    : <actual_hash>

Result    : MATCH
The file integrity check passed.

============================================================
```

---

## Detecting a Modified File

First generate the hash:

```cmd
py hash_generator.py --file test.txt
```

Then modify the file:

```cmd
notepad test.txt
```

Save the changes.

Run the verification again:

```cmd
py hash_generator.py --file test.txt --verify YOUR_OLD_HASH_HERE
```

The result will be:

```text
Result    : MISMATCH
The file may have been modified.
```

This demonstrates how cryptographic hashes can be used to detect changes to files.

---

# Why Hashing Is Useful

Hashing produces a fixed-length value based on the contents of the input.

For example:

```text
Original File
     |
     v
 SHA-256
     |
     v
ABC123...
```

If even a small part of the file changes:

```text
Modified File
     |
     v
 SHA-256
     |
     v
XYZ789...
```

The resulting hash will normally be completely different.

This makes hashes useful for:

* File integrity verification
* Software download verification
* Security investigations
* Digital forensics
* Malware analysis
* Password storage systems
* Data integrity checking
* Detecting unauthorized file modifications

---

# Security Notes

This project demonstrates hashing and integrity verification.

Hashing is **not encryption**. A hash is designed to be a one-way representation of data rather than a method for recovering the original data.

For modern security applications, SHA-256 or stronger algorithms should generally be preferred.

MD5 and SHA-1 are included in this project for educational and compatibility purposes, but they are not recommended for security-sensitive integrity or cryptographic applications where collision resistance is important.

---

# Connection With File Integrity Monitoring

This project also provides the foundation for my **File Integrity Monitor** project.

The Hash Generator performs:

```text
File
 ↓
SHA-256
 ↓
Hash
 ↓
Compare
```

A File Integrity Monitor extends this concept:

```text
Files
  ↓
Generate Baseline Hashes
  ↓
Store Hashes
  ↓
Scan Files Later
  ↓
Generate New Hashes
  ↓
Compare With Baseline
  ↓
Detect Changes
```

This is a useful concept in cybersecurity and SOC environments for identifying unexpected file modifications.

---

# Learning Objectives

Through this project, I learned:

* How cryptographic hashing works
* How SHA-256 can be used for file integrity
* How to calculate hashes using Python
* How to read files in binary mode
* How to process large files in chunks
* How to compare hashes
* How to build a Python CLI tool
* How file modification can be detected using hashes

---

# Future Improvements

Possible future improvements include:

* Graphical user interface
* Drag-and-drop file hashing
* Directory hashing
* Recursive directory scanning
* Hash comparison reports
* CSV/JSON output
* Multiple file verification
* Real-time integrity monitoring
* Wazuh/SIEM integration
* Malware hash lookup integration
* Digital forensic investigation mode

---

# Author

**Viraj Jadhav**

BCA Graduate | Cybersecurity & IT

GitHub:
https://github.com/CosmicViraj

LinkedIn:
https://linkedin.com/in/virajjadhav03

---

# License

This project is intended for educational and cybersecurity learning purposes.
