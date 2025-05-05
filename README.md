# CyberSentry - Advanced Network Intelligence Suite

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

CyberSentry (formerly PySecurity) is a command-line cybersecurity tool that offers various functions in network security and digital forensics. It is designed for security professionals, network administrators, and cybersecurity enthusiasts.

## Features

CyberSentry provides the following features with a modern and user-friendly interface:

### DNS Operations
- **Reverse DNS Lookup:** Query domain names corresponding to IP addresses
- **DNS Lookup:** Query IP addresses corresponding to domain names
- **Zone Transfer:** Test DNS zone transfer
- **DNS Host Records:** List DNS host records for a domain
- **DNS Records:** View all DNS records
- **DNS Security Check:** Perform DNSSEC validation

### Network Operations
- **IP Geolocation:** Identify the geographical location of an IP address
- **Reverse IP Lookup:** List domains associated with an IP address
- **ASN Lookup:** Query Autonomous System Number information
- **Privacy API:** Check IP privacy information
- **IPv6 Proxy Check:** Check if IPv6 addresses are proxies
- **Port Scanner:** Scan for open ports on target systems

### Security Checks
- **Email Validator:** Verify the validity of email addresses
- **Data Breach Check:** Check if an email address has been involved in data breaches
- **DMARC Lookup:** Check domain DMARC records
- **TLS Scan:** Analyze TLS/SSL configuration
- **JS Security Scanner:** Check for JavaScript security issues
- **URL Bypasser:** Identify the real targets of shortened URLs
- **SSL Certificate Info:** Check details of SSL certificates

### Additional Features
- **Batch Scan:** Scan multiple targets at once
- **Scheduled Tasks:** Automatically perform scans at specific time intervals
- **History:** View results of previous scans
- **Export Data:** Export results in HTML, JSON, or TXT format
- **Check for Updates:** Check for the latest version

### System Features
- Modern, arrow key-navigable menu system
- Multilingual support (13 languages including English, Turkish, Russian, Chinese, etc.)
- Fully customizable configuration system
- Report generation in HTML, JSON, and TXT formats
- Concurrent scanning support

## Installation

### Requirements
- Python 3.6 or higher

### Installation Steps

1. Clone the repository:
```
git clone https://github.com/raventrk/CyberSentry.git
cd CyberSentry
```

2. Install required libraries:
```
pip install -r config/requirements.txt
```

3. Start the application:
```
python main.py
```

Windows users can also run the `start.bat` file to start the application.

## Usage

When the application is running, you can navigate the menu using arrow keys and Enter key:

1. Select a category from the main menu (DNS Operations, Network Operations, etc.)
2. Select the desired function from the submenu
3. Enter the requested information (IP, domain, etc.)
4. View your results and report if necessary

### API Keys

Some functions may require API keys:
- `hackertarget`
- `ipinfo`
- `hibp` (Have I Been Pwned)

You can add these API keys to the respective fields in the `config/config.json` file.

## Configuration

You can customize the following settings through the `config/config.json` file:

- Language selection (13 supported languages)
- Report saving options
- Report format (HTML, JSON, TXT)
- Automatic update check
- Concurrent task limit
- Request timeout duration

## Supported Languages

- English
- Turkish
- Russian
- Chinese
- German
- Azerbaijani
- Japanese
- Hindi
- French
- Spanish
- Korean
- Latin
- Greek

To add a new language, you can add translations to the `config/languages.json` file.

## License

This project is licensed under the MIT License.

## Contributors

- [RavenTrk](https://github.com/raventrk)


---

**Note**: CyberSentry (CyberSentry) is designed for educational and testing purposes. The user is responsible for any consequences that may arise from malicious use or misuse. Always use within legal boundaries and with necessary permissions. 