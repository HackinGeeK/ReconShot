

## 📸 Nmap Web Screenshot Reporter

**Nmap Web Screenshot Reporter** is a Python tool that automatically captures screenshots of web applications discovered during an Nmap scan and generates a clean, visual HTML report. Perfect for penetration testers, bug bounty hunters, and network auditors who want a quick visual summary of exposed web interfaces.

### 🔍 Features

* Parses Nmap XML output to detect HTTP/HTTPS services
* Automatically launches a headless Chrome browser to capture screenshots
* Saves screenshots by IP and port
* Generates a responsive HTML report with screenshots, timestamps, and error messages (if any)
* Ideal for recon and reporting phases of engagements

### ⚙️ Requirements

* Python 3.6+
* Google Chrome installed
* Dependencies:

  * `selenium`
  * `webdriver-manager`
  * `argparse`
  * `xml.etree.ElementTree`

Install the dependencies using:

```bash
pip install selenium webdriver-manager
```

### 🚀 Usage

```bash
python nmap_web_screenshot.py path/to/nmap_output.xml path/to/output_dir
```

* `nmap_output.xml`: Your Nmap scan saved in XML format (`-oX scan.xml`)
* `output_dir`: Directory where screenshots and the HTML report will be saved

### 📁 Output Example

* `192.168.1.100_80.png`
* `192.168.1.101_443.png`
* `report.html` — Visual summary of all captured targets

### ✅ Example Nmap Command

```bash
nmap -p80,443 --open -sV -oX webscan.xml 192.168.1.0/24
```

