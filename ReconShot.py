import os
import time
import argparse
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def parse_nmap_xml(nmap_file):
    """Parses the Nmap XML file and extracts HTTP/HTTPS URLs."""
    tree = ET.parse(nmap_file)
    root = tree.getroot()
    
    urls = []
    for host in root.findall("host"):
        ip = host.find("address").get("addr")
        for port in host.findall("ports/port"):
            port_id = port.get("portid")
            protocol = "https" if port_id == "443" else "http"
            
            service = port.find("service")
            if service is not None and "http" in service.get("name", "").lower():
                urls.append({"url": f"{protocol}://{ip}:{port_id}", "ip": ip, "port": port_id})

    return urls

def take_screenshot(url_data, output_dir):
    """Takes a screenshot of a given URL using a headless Chrome browser."""
    url = url_data["url"]
    ip = url_data["ip"]
    port = url_data["port"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[+] Capturing screenshot for {url}...")

    try:
        # Setup headless Chrome
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        time.sleep(3)  # Allow time for page load
        
        # Save screenshot
        filename = f"{ip}_{port}.png"
        filepath = os.path.join(output_dir, filename)
        driver.save_screenshot(filepath)
        driver.quit()
        
        return {"url": url, "ip": ip, "port": port, "screenshot": filename, "timestamp": timestamp}
    except Exception as e:
        return {"url": url, "ip": ip, "port": port, "screenshot": None, "timestamp": timestamp, "error": str(e)}

def generate_html_report(results, output_dir):
    """Generates an HTML report with screenshots and details."""
    report_file = os.path.join(output_dir, "report.html")
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nmap Web Application Screenshot Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; }
            .container { display: flex; flex-wrap: wrap; justify-content: center; }
            .card { border: 1px solid #ddd; border-radius: 8px; margin: 10px; padding: 10px; width: 320px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
            img { width: 100%; height: auto; border-radius: 5px; }
            .error { color: red; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>Nmap Web Application Screenshot Report</h1>
        <div class="container">
    """

    for result in results:
        html_content += f"""
        <div class="card">
            <h3>{result['url']}</h3>
            <p><strong>IP:</strong> {result['ip']}</p>
            <p><strong>Port:</strong> {result['port']}</p>
            <p><strong>Timestamp:</strong> {result['timestamp']}</p>
        """

        if result["screenshot"]:
            html_content += f'<img src="{result["screenshot"]}" alt="Screenshot">'
        else:
            html_content += f'<p class="error">Failed to capture screenshot: {result.get("error", "Unknown error")}</p>'

        html_content += "</div>"

    html_content += """
        </div>
    </body>
    </html>
    """

    # Write to file
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n[+] HTML report generated: {report_file}")

def main():
    parser = argparse.ArgumentParser(description="Take screenshots of web apps discovered by Nmap and generate a report.")
    parser.add_argument("nmap_xml", help="Path to the Nmap XML file")
    parser.add_argument("output_dir", help="Directory to save screenshots and report")

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Parse Nmap XML and get URLs
    urls = parse_nmap_xml(args.nmap_xml)
    if not urls:
        print("[-] No web applications found in the Nmap scan.")
        return
    
    print(f"[+] Found {len(urls)} web applications. Capturing screenshots...\n")

    results = []
    
    # Logging instead of progress bar
    for url_data in urls:
        result = take_screenshot(url_data, args.output_dir)
        results.append(result)

    # Generate HTML Report
    generate_html_report(results, args.output_dir)

if __name__ == "__main__":
    main()
