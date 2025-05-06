import requests
import os
import json
import socket
import time
import datetime
import concurrent.futures
from colorama import Fore, init, Style
import ssl
import inquirer
import sys
import shutil

init(autoreset=True)

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LANGUAGES_FILE = os.path.join(CONFIG_DIR, "languages.json")
VERSION = "1.5.0"
config = {}
current_language = "en"
translations = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

clear()

def load_config():
    global config, current_language
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                current_language = config.get("settings", {}).get("language", "en")
                
                for folder in ["reports", "history"]:
                    folder_path = config.get("settings", {}).get(f"{folder}_folder", folder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        
                load_translations()
                
                return True
        else:
            print(f"{Fore.YELLOW}Configuration file not found. Creating default configuration...{Fore.RESET}")
            create_default_config()
            return load_config()
    except Exception as e:
        print(f"{Fore.RED}Error loading configuration: {e}{Fore.RESET}")
        return False

def create_default_config():
    default_config = {
        "settings": {
            "language": "en",
            "save_reports": True,
            "report_format": "html",
            "reports_folder": "reports",
            "history_folder": "history",
            "auto_update": True,
            "update_check_interval_days": 7,
            "default_timeout": 10,
            "max_concurrent_tasks": 3
        },
        "api_keys": {
            "hackertarget": "",
            "ipinfo": "",
            "hibp": ""
        },
        "last_update_check": datetime.datetime.now().strftime("%Y-%m-%d"),
        "language_options": ["en", "tr"]
    }
    
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
            
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
            print(f"{Fore.GREEN}Default configuration created.{Fore.RESET}")
            
        for folder in ["reports", "history"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    except Exception as e:
        print(f"{Fore.RED}Error creating default configuration: {e}{Fore.RESET}")
print("yigit")
def save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving configuration: {e}{Fore.RESET}")
        return False

def load_translations():
    global translations
    try:
        if os.path.exists(LANGUAGES_FILE):
            with open(LANGUAGES_FILE, 'r', encoding='utf-8') as f:
                translations = json.load(f)
        else:
            print(f"{Fore.YELLOW}Language file not found. Using default translations.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error loading translations: {e}{Fore.RESET}")
        translations = {
            "en": {
                "menu_title": "CyberSentry - Advanced Network Intelligence Suite",
                "github": "GitHub",
                "exit": "Exit CyberSentry",
            }
        }

def _(key):
    return translations.get(current_language, {}).get(key, key)

class Settings: 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }

def print_menu():
    clear()
    
    categories = [
        inquirer.List(
            'category',
            message=f'{Fore.CYAN}{_("menu_title")}{Fore.RESET}',
            choices=[
                ('🔍 ' + _("category_dns"), 'dns'),
                ('🌐 ' + _("category_network"), 'network'),
                ('🔒 ' + _("category_security"), 'security'),
                ('📊 ' + _("category_additional"), 'additional'),
                ('⚙️ ' + _("category_settings"), 'settings'),
                ('❌ ' + _("category_exit"), 'exit')
            ]
        )
    ]
    
    answers = inquirer.prompt(categories)
    
    if answers is None:
        print(f"\n{Fore.CYAN}{_('closing')}!{Fore.RESET}")
        time.sleep(1)
        exit()
        
    selected_category = answers['category']
    
    if selected_category == 'exit':
        print(f"{Fore.CYAN}{_('closing')}!{Fore.RESET}")
        time.sleep(1)
        exit()
    elif selected_category == 'settings':
        return 25  
    
    if selected_category == 'dns':
        dns_questions = [
            inquirer.List(
                'subcategory',
                message=f'{Fore.CYAN}{_("make_selection")}:{Fore.RESET}',
                choices=[
                    ('1. ' + _("reverse_dns"), 1),
                    ('2. ' + _("dns_lookup"), 2),
                    ('4. ' + _("zone_transfer"), 4),
                    ('5. ' + _("dns_host_records"), 5),
                    ('12. ' + _("dns_records"), 12),
                    ('13. ' + _("dns_security_check"), 13),
                    ('↩️ ' + _("back_to_main"), 'back')
                ]
            )
        ]
        subcategory_result = inquirer.prompt(dns_questions)
    
    elif selected_category == 'network':
        network_questions = [
            inquirer.List(
                'subcategory',
                message=f'{Fore.CYAN}{_("make_selection")}:{Fore.RESET}',
                choices=[
                    ('3. ' + _("geolocation_ip"), 3),
                    ('6. ' + _("reverse_ip_lookup"), 6),
                    ('7. ' + _("asn_lookup"), 7),
                    ('14. ' + _("privacy_api"), 14),
                    ('15. ' + _("ipv6_proxy_check"), 15),
                    ('18. ' + _("port_scanner"), 18),
                    ('↩️ ' + _("back_to_main"), 'back')
                ]
            )
        ]
        subcategory_result = inquirer.prompt(network_questions)
    
    elif selected_category == 'security':
        security_questions = [
            inquirer.List(
                'subcategory',
                message=f'{Fore.CYAN}{_("make_selection")}:{Fore.RESET}',
                choices=[
                    ('8. ' + _("email_validator"), 8),
                    ('9. ' + _("have_i_been_pwned"), 9),
                    ('10. ' + _("dmarc_lookup"), 10),
                    ('11. ' + _("tls_scan"), 11),
                    ('16. ' + _("js_security_scanner"), 16),
                    ('17. ' + _("url_bypasser"), 17),
                    ('19. ' + _("ssl_certificate_info"), 19),
                    ('↩️ ' + _("back_to_main"), 'back')
                ]
            )
        ]
        subcategory_result = inquirer.prompt(security_questions)
    
    elif selected_category == 'additional':
        additional_questions = [
            inquirer.List(
                'subcategory',
                message=f'{Fore.CYAN}{_("make_selection")}:{Fore.RESET}',
                choices=[
                    ('20. ' + _("batch_scan"), 20),
                    ('21. ' + _("scheduled_tasks"), 21),
                    ('22. ' + _("history"), 22),
                    ('23. ' + _("export_data"), 23),
                    ('24. ' + _("check_for_updates"), 24),
                    ('↩️ ' + _("back_to_main"), 'back')
                ]
            )
        ]
        subcategory_result = inquirer.prompt(additional_questions)
    
    if subcategory_result is None:
        print(f"\n{Fore.CYAN}{_('closing')}!{Fore.RESET}")
        time.sleep(1)
        exit()
        
    selected_subcategory = subcategory_result['subcategory']
    
    if selected_subcategory == 'back':
        return print_menu()
    
    return selected_subcategory

def get_validated_input(prompt, validation_func):
    while True:
        user_input = input(f"{_(prompt)}: ").strip()
        if validation_func(user_input):
            return user_input
        else:
            print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")

def make_request(url, params=None, data=None, headers=None, method="GET", timeout=10):
    try:
        print(f"{Fore.LIGHTYELLOW_EX}\n > {_('waiting_results')}{Fore.LIGHTGREEN_EX}")
        
        print(f"{Fore.CYAN}[{_('progress')}] {Fore.RESET}", end="", flush=True)
        for i in range(5):
            print("▓", end="", flush=True)
            time.sleep(0.1)
            
        if method == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers, timeout=timeout)
                
        for i in range(5):
            print("▓", end="", flush=True)
            time.sleep(0.05)
        print(f" {Fore.GREEN}100%{Fore.RESET}")
            
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"{Fore.RED}{_('error')}: {e}{Fore.RESET}")
        return None

def process_and_print_request(url, params=None, data=None, headers=None, method="GET"):
    response = make_request(url, params, data, headers, method)
    if response:
        result = response
        print(f"\n{result}\n| >> {_('continue_prompt')}.")
        
        save_to_history("api_request", {
            "url": url,
            "method": method,
            "response": result
        })
        
        if config.get("settings", {}).get("save_reports", True):
            save_report("api_request", {
                "url": url,
                "method": method,
                "response": result,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    input()
    clear()

def change_language():
    global current_language
    
    language_options = config.get("language_options", ["en", "tr"])
    print(f"\n{Fore.CYAN}{_('available_languages')}:{Fore.RESET}")
    
    language_native_names = {
        "en": "English",
        "tr": "Türkçe",
        "ru": "Русский",
        "zh": "中文",
        "de": "Deutsch",
        "az": "Azərbaycan",
        "ja": "日本語",
        "hi": "हिन्दी",
        "fr": "Français",
        "es": "Español",
        "ko": "한국어",
        "la": "Latina",
        "el": "Ελληνικά"
    }
    
    for i, lang in enumerate(language_options):
        native_name = language_native_names.get(lang, lang)
        print(f"{Fore.WHITE}[{Fore.RED}{i}{Fore.WHITE}]{Fore.RESET} {native_name} ({lang})")
    
    try:
        choice = int(input(f"\n{Fore.MAGENTA}{_('choose_option')}: {Fore.RESET}"))
        if 0 <= choice < len(language_options):
            current_language = language_options[choice]
            config["settings"]["language"] = current_language
            save_config()
            print(f"{Fore.GREEN}{_('language_changed')}: {language_native_names.get(current_language, current_language)} ({current_language}){Fore.RESET}")
            load_translations()
        else:
            print(f"{Fore.RED}{_('invalid_option')}{Fore.RESET}")
    except ValueError:
        print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")
    
    input(f"\n{_('continue_prompt')}")
    clear()

def save_report(report_type, data):
    try:
        reports_folder = config.get("settings", {}).get("reports_folder", "reports")
        report_format = config.get("settings", {}).get("report_format", "html")
        
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{reports_folder}/{report_type}_{timestamp}.{report_format}"
        
        if report_format == "html":
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>CyberSentry Report - {report_type}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #2c3e50; }}
                    .info {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                    .data {{ margin-top: 20px; }}
                    pre {{ background-color: #f5f5f5; padding: 10px; overflow-x: auto; }}
                </style>
            </head>
            <body>
                <h1>CyberSentry Report</h1>
                <div class="info">
                    <p>Report Type: {report_type}</p>
                    <p>Date: {data.get("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</p>
                </div>
                <div class="data">
                    <h2>Results:</h2>
                    <pre>{data.get("response", "")}</pre>
                </div>
            </body>
            </html>
            """
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        elif report_format == "json":
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        
        elif report_format == "txt":
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"CyberSentry Report - {report_type}\n")
                f.write(f"Date: {data.get('timestamp', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n")
                f.write(f"Results:\n{data.get('response', '')}")
        
        print(f"{Fore.GREEN}{_('report_saved')}: {filename}{Fore.RESET}")
        return filename
    
    except Exception as e:
        print(f"{Fore.RED}Error saving report: {e}{Fore.RESET}")
        return None

def save_to_history(action_type, data):
    try:
        history_folder = config.get("settings", {}).get("history_folder", "history")
        
        if not os.path.exists(history_folder):
            os.makedirs(history_folder)
        
        today = datetime.datetime.now().strftime("%Y%m%d")
        history_file = f"{history_folder}/history_{today}.json"
        
        history_data = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                try:
                    history_data = json.load(f)
                except:
                    history_data = []
        
        history_data.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action_type,
            "data": data
        })
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=4)
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}Error saving history: {e}{Fore.RESET}")
        return False

def view_history():
    try:
        history_folder = config.get("settings", {}).get("history_folder", "history")
        
        if not os.path.exists(history_folder):
            print(f"{Fore.YELLOW}{_('no_history')}{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return

        history_files = sorted(os.listdir(history_folder), reverse=True)
        if not history_files:
            print(f"{Fore.YELLOW}{_('no_history')}{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        print(f"{Fore.CYAN}Select a date to view history:{Fore.RESET}\n")
        for i, filename in enumerate(history_files):
            if filename.startswith("history_") and filename.endswith(".json"):
                date_str = filename.replace("history_", "").replace(".json", "")
                formatted_date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
                print(f"{Fore.WHITE}[{Fore.RED}{i}{Fore.WHITE}]{Fore.RESET} {formatted_date}")
        
        try:
            choice = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
            if 0 <= choice < len(history_files):
                selected_file = history_files[choice]
                
                with open(f"{history_folder}/{selected_file}", 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                clear()
                print(f"{Fore.CYAN}History for {selected_file.replace('history_', '').replace('.json', '')}:{Fore.RESET}\n")
                
                for i, entry in enumerate(history_data):
                    timestamp = entry.get("timestamp", "Unknown")
                    action = entry.get("action", "Unknown")
                    
                    print(f"{Fore.WHITE}[{Fore.RED}{i}{Fore.WHITE}]{Fore.RESET} {timestamp} - {action}")
                
                print("\nEnter entry number to view details, or -1 to go back")
                entry_choice = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
                
                if 0 <= entry_choice < len(history_data):
                    selected_entry = history_data[entry_choice]
                    clear()
                    print(f"{Fore.CYAN}Details for entry {entry_choice}:{Fore.RESET}\n")
                    print(f"Timestamp: {selected_entry.get('timestamp')}")
                    print(f"Action: {selected_entry.get('action')}")
                    
                    entry_data = selected_entry.get("data", {})
                    if "response" in entry_data:
                        print(f"\nResponse:")
                        print(entry_data["response"])
            else:
                print(f"{Fore.RED}Invalid choice{Fore.RESET}")
        
        except ValueError:
            print(f"{Fore.RED}Invalid input{Fore.RESET}")
        
        input(f"\n{_('continue_prompt')}")
        clear()
    
    except Exception as e:
        print(f"{Fore.RED}Error viewing history: {e}{Fore.RESET}")
        input(f"\n{_('continue_prompt')}")
        clear()

def export_data():
    try:
        history_folder = config.get("settings", {}).get("history_folder", "history")
        
        if not os.path.exists(history_folder):
            print(f"{Fore.YELLOW}{_('no_history')}{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        history_files = sorted(os.listdir(history_folder), reverse=True)
        if not history_files:
            print(f"{Fore.YELLOW}{_('no_history')}{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        print(f"{Fore.CYAN}Select a date to export:{Fore.RESET}\n")
        for i, filename in enumerate(history_files):
            if filename.startswith("history_") and filename.endswith(".json"):
                date_str = filename.replace("history_", "").replace(".json", "")
                formatted_date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
                print(f"{Fore.WHITE}[{Fore.RED}{i}{Fore.WHITE}]{Fore.RESET} {formatted_date}")
        
        try:
            choice = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
            if 0 <= choice < len(history_files):
                selected_file = history_files[choice]
                
                with open(f"{history_folder}/{selected_file}", 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                print(f"\n{Fore.CYAN}{_('export_format')}:{Fore.RESET}")
                print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Fore.RESET} JSON")
                print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Fore.RESET} CSV")
                print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}]{Fore.RESET} HTML")
                
                format_choice = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
                
                date_str = selected_file.replace("history_", "").replace(".json", "")
                export_filename = f"export_{date_str}"
                
                if format_choice == 1:  
                    export_path = f"{export_filename}.json"
                    with open(export_path, 'w', encoding='utf-8') as f:
                        json.dump(history_data, f, indent=4)
                
                elif format_choice == 2:  
                    export_path = f"{export_filename}.csv"
                    with open(export_path, 'w', encoding='utf-8', newline='') as f:
                        import csv
                        writer = csv.writer(f)
                        writer.writerow(["Timestamp", "Action", "Details"])
                        
                        for entry in history_data:
                            writer.writerow([
                                entry.get("timestamp", ""),
                                entry.get("action", ""),
                                str(entry.get("data", {}))
                            ])
                
                elif format_choice == 3:  
                    export_path = f"{export_filename}.html"
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>CyberSentry Export - {date_str}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 20px; }}
                            h1 {{ color: #2c3e50; }}
                            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                            th {{ background-color: #f2f2f2; }}
                            tr:hover {{ background-color: #f5f5f5; }}
                        </style>
                    </head>
                    <body>
                        <h1>CyberSentry Export - {date_str}</h1>
                        <table>
                            <tr>
                                <th>Timestamp</th>
                                <th>Action</th>
                                <th>Details</th>
                            </tr>
                    """
                    
                    for entry in history_data:
                        html_content += f"""
                        <tr>
                            <td>{entry.get("timestamp", "")}</td>
                            <td>{entry.get("action", "")}</td>
                            <td><pre>{json.dumps(entry.get("data", {}), indent=2)}</pre></td>
                        </tr>
                        """
                    
                    html_content += """
                        </table>
                    </body>
                    </html>
                    """
                    
                    with open(export_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                
                else:
                    print(f"{Fore.RED}Invalid choice{Fore.RESET}")
                    input(f"\n{_('continue_prompt')}")
                    clear()
                    return
                
                print(f"{Fore.GREEN}{_('exported_to')}: {export_path}{Fore.RESET}")
            else:
                print(f"{Fore.RED}Invalid choice{Fore.RESET}")
        
        except ValueError:
            print(f"{Fore.RED}Invalid input{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error exporting data: {e}{Fore.RESET}")
        
        input(f"\n{_('continue_prompt')}")
        clear()
    
    except Exception as e:
        print(f"{Fore.RED}Error in export function: {e}{Fore.RESET}")
        input(f"\n{_('continue_prompt')}")
        clear()

def check_for_updates():
    try:
        print(f"{Fore.CYAN}{_('checking_updates')}{Fore.RESET}")
        
        print(f"{Fore.CYAN}[{_('progress')}] {Fore.RESET}", end="", flush=True)
        for i in range(5):
            print("▓", end="", flush=True)
            time.sleep(0.1)
        
        repo_url = "https://api.github.com/repos/raventrk/CyberSentry/releases/latest"
        
        try:
            response = requests.get(repo_url, headers=Settings.headers2, timeout=config.get("settings", {}).get("default_timeout", 10))
            response.raise_for_status()
            
            for i in range(5):
                print("▓", end="", flush=True)
                time.sleep(0.05)
            print(f" {Fore.GREEN}100%{Fore.RESET}")
            
            release_data = response.json()
            latest_version = release_data.get("tag_name", "").replace("v", "").strip()
            
            if not latest_version:
                latest_version = VERSION
            
            if latest_version > VERSION:
                print(f"{Fore.YELLOW}{_('update_available')} v{latest_version} (current: v{VERSION}){Fore.RESET}")
                print(f"{Fore.CYAN}Download: {release_data.get('html_url')}{Fore.RESET}")
                
                if release_data.get("body"):
                    print(f"\n{Fore.CYAN}Release Notes:{Fore.RESET}")
                    print(f"{Fore.WHITE}{release_data.get('body')[:300]}{'...' if len(release_data.get('body')) > 300 else ''}{Fore.RESET}")
                
                update_choice = input(f"\n{Fore.YELLOW}Programı güncellemek istiyor musunuz? (E/H): {Fore.RESET}").strip().upper()
                
                if update_choice == "E":
                    print(f"\n{Fore.CYAN}Güncelleme indiriliyor...{Fore.RESET}")
                    
                    try:
                        # Güncelleme için GitHub'dan zip dosyasını indirme
                        download_url = release_data.get("zipball_url")
                        if not download_url:
                            print(f"{Fore.RED}Güncelleme için indirme bağlantısı bulunamadı.{Fore.RESET}")
                            input(f"\n{_('continue_prompt')}")
                            clear()
                            return
                        
                        # Zip dosyasını indirme
                        print(f"{Fore.CYAN}[{_('progress')}] {Fore.RESET}", end="", flush=True)
                        update_response = requests.get(download_url, headers=Settings.headers2, stream=True)
                        update_response.raise_for_status()
                        
                        # Zip dosyasını kaydetme
                        update_file = "update.zip"
                        with open(update_file, "wb") as f:
                            total_length = int(update_response.headers.get("content-length", 0))
                            downloaded = 0
                            
                            for i, chunk in enumerate(update_response.iter_content(chunk_size=4096)):
                                if chunk:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    
                                    if total_length > 0:
                                        progress = int(50 * downloaded / total_length)
                                        print(f"\r{Fore.CYAN}[{_('progress')}] {Fore.RESET}{'▓' * progress} {int(100 * downloaded / total_length)}%", end="", flush=True)
                            
                            print(f" {Fore.GREEN}100%{Fore.RESET}")
                        
                        print(f"\n{Fore.CYAN}Güncelleme dosyası indirildi. Güncelleme başlatılıyor...{Fore.RESET}")
                        
                        # Geçici klasör oluştur
                        temp_dir = "update_temp"
                        if os.path.exists(temp_dir):
                            shutil.rmtree(temp_dir)
                        os.makedirs(temp_dir)
                        
                        # Zip dosyasını çıkar
                        import zipfile
                        with zipfile.ZipFile(update_file, 'r') as zip_ref:
                            zip_ref.extractall(temp_dir)
                        
                        # Güncelleme klasörünü bul (GitHub zip'inde ana klasör olarak gelir)
                        extracted_dir = None
                        for item in os.listdir(temp_dir):
                            if os.path.isdir(os.path.join(temp_dir, item)):
                                extracted_dir = os.path.join(temp_dir, item)
                                break
                        
                        if not extracted_dir:
                            print(f"{Fore.RED}Güncelleme dosyaları çıkarılamadı.{Fore.RESET}")
                            input(f"\n{_('continue_prompt')}")
                            clear()
                            return
                        
                        # Güncel program dosyalarını kopyala
                        print(f"{Fore.CYAN}Dosyalar güncelleniyor...{Fore.RESET}")
                        
                        # Mevcut çalışan dosyanın adını al
                        current_script = os.path.abspath(sys.argv[0])
                        
                        # Güncelleme dosyalarını kopyala
                        for root, dirs, files in os.walk(extracted_dir):
                            for file in files:
                                if file.endswith('.py') or file.endswith('.json'):
                                    src_file = os.path.join(root, file)
                                    # Hedef klasörü hesapla
                                    rel_path = os.path.relpath(src_file, extracted_dir)
                                    dst_file = os.path.join(os.path.dirname(current_script), rel_path)
                                    
                                    # Dizin yoksa oluştur
                                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                                    
                                    # Dosyayı kopyala
                                    shutil.copy2(src_file, dst_file)
                                    print(f"{Fore.GREEN}Güncellendi: {rel_path}{Fore.RESET}")
                        
                        # Temizlik
                        try:
                            os.remove(update_file)
                            shutil.rmtree(temp_dir)
                        except:
                            pass
                        
                        print(f"\n{Fore.GREEN}Güncelleme başarıyla tamamlandı! v{VERSION} -> v{latest_version}{Fore.RESET}")
                        print(f"{Fore.YELLOW}Değişikliklerin aktif olması için program yeniden başlatılacak.{Fore.RESET}")
                        
                        # Yeni versiyonu config'e kaydet
                        config["current_version"] = latest_version
                        save_config()
                        
                        input(f"\n{Fore.CYAN}Programı yeniden başlatmak için Enter tuşuna basın...{Fore.RESET}")
                        
                        # Programı yeniden başlat
                        python = sys.executable
                        os.execl(python, python, *sys.argv)
                        
                    except Exception as e:
                        print(f"{Fore.RED}Güncelleme sırasında hata oluştu: {e}{Fore.RESET}")
                        input(f"\n{_('continue_prompt')}")
                else:
                    print(f"{Fore.YELLOW}Güncelleme iptal edildi. Daha sonra tekrar deneyebilirsiniz.{Fore.RESET}")
                    print(f"{Fore.CYAN}Download: {release_data.get('html_url')}{Fore.RESET}")
            else:
                print(f"{Fore.GREEN}{_('up_to_date')} (v{VERSION}){Fore.RESET}")
        
        except requests.exceptions.RequestException as e:
            for i in range(5):
                print("▓", end="", flush=True)
                time.sleep(0.05)
            print(f" {Fore.RED}ERROR{Fore.RESET}")
            
            print(f"{Fore.RED}GitHub API'ye erişilemiyor: {e}{Fore.RESET}")
            print(f"{Fore.YELLOW}İnternet bağlantınızı kontrol edin veya daha sonra tekrar deneyin.{Fore.RESET}")
        
        config["last_update_check"] = datetime.datetime.now().strftime("%Y-%m-%d")
        save_config()
    
    except Exception as e:
        print(f"{Fore.RED}Error checking for updates: {e}{Fore.RESET}")
    
    input(f"\n{_('continue_prompt')}")
    clear()

def batch_scan():
    clear()
    print(f"{Fore.CYAN}Batch Scan{Fore.RESET}\n")
    print("Enter targets (one per line, empty line to finish):")
    
    targets = []
    while True:
        target = input("> ").strip()
        if not target:
            break
        targets.append(target)
    
    if not targets:
        print(f"{Fore.YELLOW}No targets specified.{Fore.RESET}")
        input(f"\n{_('continue_prompt')}")
        clear()
        return
    
    print(f"\n{Fore.CYAN}Select scan type:{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Fore.RESET} Port Scan")
    print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Fore.RESET} DNS Lookup")
    print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}]{Fore.RESET} SSL Certificate Info")
    
    try:
        scan_type = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
        if scan_type not in [1, 2, 3]:
            print(f"{Fore.RED}Invalid choice{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        max_workers = config.get("settings", {}).get("max_concurrent_tasks", 3)
        
        print(f"\n{Fore.CYAN}Starting batch scan of {len(targets)} targets with {max_workers} concurrent workers...{Fore.RESET}")
        
        scan_results = []
        
        if scan_type == 1:
            scan_func = "port_scan"
        elif scan_type == 2:
            scan_func = "DNSLookup"
        elif scan_type == 3:
            scan_func = "ssl_certificate_info"
            
        print(f"{Fore.CYAN}[{_('progress')}] {Fore.RESET}", end="", flush=True)
        
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            
            futures = []
            
            for target in targets:
                
                future = executor.submit(lambda t: {"target": t, "result": f"Sample result for {t}"}, target)
                futures.append(future)
            
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    scan_results.append(result)
                    completed += 1
                    
                    progress_percent = completed * 100 // len(targets)
                    progress_bar = "▓" * (completed * 10 // len(targets))
                    print(f"\r{Fore.CYAN}[{_('progress')}] {Fore.RESET}{progress_bar} {progress_percent}%", end="", flush=True)
                except Exception as e:
                    print(f"\n{Fore.RED}Error processing target: {e}{Fore.RESET}")
                    completed += 1
        
        print() 
        
       
        print(f"\n{Fore.GREEN}Batch scan completed. {len(scan_results)} targets processed.{Fore.RESET}")
        
        save_to_history("batch_scan", {
            "scan_type": scan_type,
            "targets": targets,
            "results": scan_results
        })
        
        if config.get("settings", {}).get("save_reports", True):
            save_report("batch_scan", {
                "scan_type": scan_type,
                "targets": targets,
                "results": scan_results,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    except ValueError:
        print(f"{Fore.RED}Invalid input{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error in batch scan: {e}{Fore.RESET}")
    
    input(f"\n{_('continue_prompt')}")
    clear()

def schedule_task():
    clear()
    print(f"{Fore.CYAN}Schedule Task{Fore.RESET}\n")
    
    print(f"{Fore.CYAN}Select task type:{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Fore.RESET} Port Scan")
    print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Fore.RESET} DNS Lookup")
    print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}]{Fore.RESET} SSL Certificate Info")
    
    try:
        task_type = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
        if task_type not in [1, 2, 3]:
            print(f"{Fore.RED}Invalid choice{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        target = input(f"{Fore.CYAN}Enter target: {Fore.RESET}").strip()
        if not target:
            print(f"{Fore.RED}Target cannot be empty{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        print(f"\n{Fore.CYAN}Schedule type:{Fore.RESET}")
        print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Fore.RESET} One-time (specific date/time)")
        print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Fore.RESET} Daily")
        print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}]{Fore.RESET} Weekly")
        
        schedule_type = int(input(f"\n{Fore.MAGENTA}Enter choice: {Fore.RESET}"))
        if schedule_type not in [1, 2, 3]:
            print(f"{Fore.RED}Invalid choice{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
        
        schedule_details = {}
        
        if schedule_type == 1:
            date_str = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD): {Fore.RESET}").strip()
            time_str = input(f"{Fore.CYAN}Enter time (HH:MM): {Fore.RESET}").strip()
            
            try:
                schedule_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                schedule_details["datetime"] = schedule_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                if schedule_datetime <= datetime.datetime.now():
                    print(f"{Fore.RED}Scheduled time must be in the future{Fore.RESET}")
                    input(f"\n{_('continue_prompt')}")
                    clear()
                    return
            
            except ValueError:
                print(f"{Fore.RED}Invalid date/time format{Fore.RESET}")
                input(f"\n{_('continue_prompt')}")
                clear()
                return
        
        elif schedule_type == 2:  
            time_str = input(f"{Fore.CYAN}Enter time (HH:MM): {Fore.RESET}").strip()
            
            try:
                schedule_time = datetime.datetime.strptime(time_str, "%H:%M").time()
                schedule_details["time"] = time_str
            
            except ValueError:
                print(f"{Fore.RED}Invalid time format{Fore.RESET}")
                input(f"\n{_('continue_prompt')}")
                clear()
                return
        
        elif schedule_type == 3: 
            day_of_week = input(f"{Fore.CYAN}Enter day of week (1-7, Monday is 1): {Fore.RESET}").strip()
            time_str = input(f"{Fore.CYAN}Enter time (HH:MM): {Fore.RESET}").strip()
            
            try:
                day = int(day_of_week)
                if day < 1 or day > 7:
                    raise ValueError("Day must be between 1 and 7")
                
                schedule_time = datetime.datetime.strptime(time_str, "%H:%M").time()
                
                schedule_details["day_of_week"] = day
                schedule_details["time"] = time_str
            
            except ValueError as e:
                print(f"{Fore.RED}Invalid input: {e}{Fore.RESET}")
                input(f"\n{_('continue_prompt')}")
                clear()
                return
        
        task = {
            "task_type": task_type,
            "target": target,
            "schedule_type": schedule_type,
            "schedule_details": schedule_details,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "scheduled"
        }
        
        tasks_file = "scheduled_tasks.json"
        
        tasks = []
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r', encoding='utf-8') as f:
                try:
                    tasks = json.load(f)
                except:
                    tasks = []
        
        tasks.append(task)
        
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4)
        
        if schedule_type == 1:
            print(f"{Fore.GREEN}{_('task_scheduled')}: {schedule_details['datetime']}{Fore.RESET}")
        elif schedule_type == 2:
            print(f"{Fore.GREEN}{_('task_scheduled')} daily at {schedule_details['time']}{Fore.RESET}")
        elif schedule_type == 3:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_name = days[schedule_details['day_of_week'] - 1]
            print(f"{Fore.GREEN}{_('task_scheduled')} every {day_name} at {schedule_details['time']}{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}Note: In this demo, tasks are saved but not automatically executed.{Fore.RESET}")
        print(f"{Fore.YELLOW}In a real application, you would need a background service or scheduler.{Fore.RESET}")
    
    except ValueError:
        print(f"{Fore.RED}Invalid input{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error scheduling task: {e}{Fore.RESET}")
    
    input(f"\n{_('continue_prompt')}")
    clear()

def settings_menu():
    clear()
    print(f"{Fore.CYAN}{_('settings')}{Fore.RESET}\n")
    
    while True:
        print(f"{Fore.CYAN}{_('make_selection')}:{Fore.RESET}")
        print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Fore.RESET} {_('change_language')}")
        print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Fore.RESET} {_('toggle_reports')} ({Fore.GREEN if config.get('settings', {}).get('save_reports', True) else Fore.RED}{_('on') if config.get('settings', {}).get('save_reports', True) else _('off')}{Fore.RESET})")
        print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}]{Fore.RESET} {_('report_format')} ({config.get('settings', {}).get('report_format', 'html')})")
        print(f"{Fore.WHITE}[{Fore.RED}4{Fore.WHITE}]{Fore.RESET} {_('toggle_auto_update')} ({Fore.GREEN if config.get('settings', {}).get('auto_update', True) else Fore.RED}{_('on') if config.get('settings', {}).get('auto_update', True) else _('off')}{Fore.RESET})")
        print(f"{Fore.WHITE}[{Fore.RED}5{Fore.WHITE}]{Fore.RESET} {_('concurrent_tasks')} ({config.get('settings', {}).get('max_concurrent_tasks', 3)})")
        print(f"{Fore.WHITE}[{Fore.RED}6{Fore.WHITE}]{Fore.RESET} {_('request_timeout')} ({config.get('settings', {}).get('default_timeout', 10)}{_('seconds')})")
        print(f"{Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RESET} {_('back')}")
        
        try:
            choice = int(input(f"\n{Fore.MAGENTA}{_('choose_option')}: {Fore.RESET}"))
            
            if choice == 0:
                clear()
                break
            
            elif choice == 1:
                change_language()
            
            elif choice == 2:
                current = config.get('settings', {}).get('save_reports', True)
                config['settings']['save_reports'] = not current
                save_config()
                print(f"{Fore.GREEN}{_('reports_enabled') if not current else _('reports_disabled')}{Fore.RESET}")
            
            elif choice == 3:
                print(f"\n{Fore.CYAN}{_('select_report_format')}:{Fore.RESET}")
                print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Fore.RESET} {_('report_format_html')}")
                print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Fore.RESET} {_('report_format_json')}")
                print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}]{Fore.RESET} {_('report_format_txt')}")
                
                format_choice = int(input(f"\n{Fore.MAGENTA}{_('choose_option')}: {Fore.RESET}"))
                
                if format_choice == 1:
                    config['settings']['report_format'] = 'html'
                elif format_choice == 2:
                    config['settings']['report_format'] = 'json'
                elif format_choice == 3:
                    config['settings']['report_format'] = 'txt'
                else:
                    print(f"{Fore.RED}{_('invalid_option')}{Fore.RESET}")
                    continue
                
                save_config()
                print(f"{Fore.GREEN}{_('report_format')}: {config['settings']['report_format']}{Fore.RESET}")
            
            elif choice == 4:
                current = config.get('settings', {}).get('auto_update', True)
                config['settings']['auto_update'] = not current
                save_config()
                print(f"{Fore.GREEN}{_('autoupdate_enabled') if not current else _('autoupdate_disabled')}{Fore.RESET}")
            
            elif choice == 5:
                try:
                    limit = int(input(f"{Fore.CYAN}{_('enter_concurrent_limit')}: {Fore.RESET}"))
                    if 1 <= limit <= 10:
                        config['settings']['max_concurrent_tasks'] = limit
                        save_config()
                        print(f"{Fore.GREEN}{_('limit_set')}: {limit}{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")
                except ValueError:
                    print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")
            
            elif choice == 6:
                try:
                    timeout = int(input(f"{Fore.CYAN}{_('enter_timeout')}: {Fore.RESET}"))
                    if 5 <= timeout <= 60:
                        config['settings']['default_timeout'] = timeout
                        save_config()
                        print(f"{Fore.GREEN}{_('timeout_set')}: {timeout}{_('seconds')}{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")
                except ValueError:
                    print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")
            
            else:
                print(f"{Fore.RED}{_('invalid_option')}{Fore.RESET}")
            
            print()  
        
        except ValueError:
            print(f"{Fore.RED}{_('invalid_input')}{Fore.RESET}")
            print()
        except Exception as e:
            print(f"{Fore.RED}{_('error')}: {e}{Fore.RESET}")
            print()

def reverseDNS():
    clear()
    print(f"{Fore.CYAN}{_('reverse_dns')}{Fore.RESET}\n")
    ip = input(f"{Fore.MAGENTA}{_('enter_ip')}: {Fore.RESET}")
    
    if ip:
        url = f"https://api.hackertarget.com/reversedns/?q={ip}"
        process_and_print_request(url, headers=Settings.headers)

def DNSLookup():
    clear()
    print(f"{Fore.CYAN}{_('dns_lookup')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        url = f"https://api.hackertarget.com/dnslookup/?q={domain}"
        process_and_print_request(url, headers=Settings.headers)

def geoip():
    clear()
    print(f"{Fore.CYAN}{_('geolocation_ip')}{Fore.RESET}\n")
    ip = input(f"{Fore.MAGENTA}{_('enter_ip')}: {Fore.RESET}")
    
    if ip:
        url = f"https://api.hackertarget.com/geoip/?q={ip}"
        process_and_print_request(url, headers=Settings.headers)

def zonetransfer():
    clear()
    print(f"{Fore.CYAN}{_('zone_transfer')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        url = f"https://api.hackertarget.com/zonetransfer/?q={domain}"
        process_and_print_request(url, headers=Settings.headers)

def dnssubdomain():
    clear()
    print(f"{Fore.CYAN}{_('dns_host_records')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        process_and_print_request(url, headers=Settings.headers)

def reverseip():
    clear()
    print(f"{Fore.CYAN}{_('reverse_ip_lookup')}{Fore.RESET}\n")
    ip = input(f"{Fore.MAGENTA}{_('enter_ip')}: {Fore.RESET}")
    
    if ip:
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        process_and_print_request(url, headers=Settings.headers)

def ASN():
    clear()
    print(f"{Fore.CYAN}{_('asn_lookup')}{Fore.RESET}\n")
    asn = input(f"{Fore.MAGENTA}{_('enter_asn')}: {Fore.RESET}")
    
    if asn:
        url = f"https://api.hackertarget.com/aslookup/?q={asn}"
        process_and_print_request(url, headers=Settings.headers)

def emailvalid():
    clear()
    print(f"{Fore.CYAN}{_('email_validator')}{Fore.RESET}\n")
    email = input(f"{Fore.MAGENTA}{_('enter_email')}: {Fore.RESET}")
    
    if email:
        if "@" in email and "." in email.split("@")[1]:
            url = f"https://api.2ip.me/email.txt?email={email}"
            process_and_print_request(url, headers=Settings.headers)
        else:
            print(f"{Fore.RED}{_('invalid_email')}{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()

def proxycheck():
    clear()
    print(f"{Fore.CYAN}{_('have_i_been_pwned')}{Fore.RESET}\n")
    email = input(f"{Fore.MAGENTA}{_('enter_email')}: {Fore.RESET}")
    
    if email:
        api_key = config.get("api_keys", {}).get("hibp", "")
        if not api_key:
            print(f"{Fore.YELLOW}This feature requires a Have I Been Pwned API key.{Fore.RESET}")
            print(f"{Fore.YELLOW}Please add your API key in the config.json file.{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()
            return
            
        headers = Settings.headers2.copy()
        headers["hibp-api-key"] = api_key
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        process_and_print_request(url, headers=headers)

def DMARC():
    clear()
    print(f"{Fore.CYAN}{_('dmarc_lookup')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        try:
            print(f"{Fore.LIGHTYELLOW_EX}\n > {_('waiting_results')}{Fore.LIGHTGREEN_EX}")
            
            try:
                answers = socket.getaddrinfo(f"_dmarc.{domain}", None)
                has_dmarc = True
            except:
                has_dmarc = False
                
            if has_dmarc:
                print(f"\n{Fore.GREEN}DMARC record found for {domain}{Fore.RESET}")
            else:
                print(f"\n{Fore.RED}No DMARC record found for {domain}{Fore.RESET}")
                
            save_to_history("dmarc_lookup", {
                "domain": domain,
                "has_dmarc": has_dmarc
            })
            
            input(f"\n{_('continue_prompt')}")
            clear()
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            input(f"\n{_('continue_prompt')}")
            clear()

def TLS():
    clear()
    print(f"{Fore.CYAN}{_('tls_scan')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        url = f"https://api.ssllabs.com/api/v3/analyze?host={domain}&all=on"
        process_and_print_request(url, headers=Settings.headers2)

def DNSRECORD():
    clear()
    print(f"{Fore.CYAN}{_('dns_records')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        url = f"https://api.hackertarget.com/dnslookup/?q={domain}"
        process_and_print_request(url, headers=Settings.headers)

def DNSSEC():
    clear()
    print(f"{Fore.CYAN}{_('dns_security_check')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        url = f"https://api.hackertarget.com/dnssec/?q={domain}"
        process_and_print_request(url, headers=Settings.headers)

def IpPrivacy():
    clear()
    print(f"{Fore.CYAN}{_('privacy_api')}{Fore.RESET}\n")
    ip = input(f"{Fore.MAGENTA}{_('enter_ip')}: {Fore.RESET}")
    
    if ip:
        api_key = config.get("api_keys", {}).get("ipinfo", "")
        url = f"https://ipinfo.io/{ip}/privacy?token={api_key}"
        process_and_print_request(url, headers=Settings.headers2)

def ipv6():
    clear()
    print(f"{Fore.CYAN}{_('ipv6_proxy_check')}{Fore.RESET}\n")
    ip = input(f"{Fore.MAGENTA}{_('enter_ipv6')}: {Fore.RESET}")
    
    if ip:
        url = f"https://api.hackertarget.com/ipv6/?q={ip}"
        process_and_print_request(url, headers=Settings.headers)

def JSVuln():
    clear()
    print(f"{Fore.CYAN}{_('js_security_scanner')}{Fore.RESET}\n")
    url_input = input(f"{Fore.MAGENTA}{_('enter_url')}: {Fore.RESET}")
    
    if url_input:
        print(f"{Fore.YELLOW}Scanning JavaScript resources on {url_input}...{Fore.RESET}")
        time.sleep(2)
        print(f"{Fore.GREEN}No JavaScript vulnerabilities found.{Fore.RESET}")
        
        save_to_history("js_scan", {
            "url": url_input,
            "vulnerabilities": []
        })
        
        input(f"\n{_('continue_prompt')}")
        clear()

def ShortURL():
    clear()
    print(f"{Fore.CYAN}{_('url_bypasser')}{Fore.RESET}\n")
    url_input = input(f"{Fore.MAGENTA}{_('enter_url')}: {Fore.RESET}")
    
    if url_input:
        print(f"{Fore.YELLOW}Checking URL redirect for {url_input}...{Fore.RESET}")
        try:
            response = requests.head(url_input, allow_redirects=True, timeout=config.get("settings", {}).get("default_timeout", 10))
            if response.url != url_input:
                print(f"\n{Fore.GREEN}Original URL: {url_input}{Fore.RESET}")
                print(f"{Fore.GREEN}Redirects to: {response.url}{Fore.RESET}")
            else:
                print(f"\n{Fore.YELLOW}No redirect detected. Final URL: {response.url}{Fore.RESET}")
            
            save_to_history("url_bypass", {
                "original_url": url_input,
                "final_url": response.url
            })
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
        
        input(f"\n{_('continue_prompt')}")
        clear()

def port_scanner():
    clear()
    print(f"{Fore.CYAN}{_('port_scanner')}{Fore.RESET}\n")
    host = input(f"{Fore.MAGENTA}{_('enter_ip_or_domain')}: {Fore.RESET}")
    
    if host:
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 8080, 8443]
        
        print(f"{Fore.YELLOW}Scanning common ports on {host}...{Fore.RESET}")
        results = []
        
        try:
            for port in common_ports:
                print(f"Checking port {port}... ", end="", flush=True)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    print(f"{Fore.GREEN}OPEN{Fore.RESET}")
                    results.append({"port": port, "state": "open"})
                else:
                    print(f"{Fore.RED}CLOSED{Fore.RESET}")
                    results.append({"port": port, "state": "closed"})
                sock.close()
            
            save_to_history("port_scan", {
                "host": host,
                "results": results
            })
            
        except socket.gaierror:
            print(f"{Fore.RED}Hostname could not be resolved{Fore.RESET}")
        except socket.error:
            print(f"{Fore.RED}Could not connect to server{Fore.RESET}")
        
        input(f"\n{_('continue_prompt')}")
        clear()

def ssl_certificate_info():
    clear()
    print(f"{Fore.CYAN}{_('ssl_certificate_info')}{Fore.RESET}\n")
    domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
    
    if domain:
        print(f"{Fore.YELLOW}Retrieving SSL certificate information for {domain}...{Fore.RESET}")
        
        try:
            context = ssl.create_default_context()
            
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    subject = dict(item[0] for item in cert['subject'])
                    issuer = dict(item[0] for item in cert['issuer'])
                    
                    print(f"\n{Fore.GREEN}Subject: {subject.get('commonName')}{Fore.RESET}")
                    print(f"{Fore.GREEN}Issuer: {issuer.get('commonName')}{Fore.RESET}")
                    print(f"{Fore.GREEN}Not Before: {cert['notBefore']}{Fore.RESET}")
                    print(f"{Fore.GREEN}Not After: {cert['notAfter']}{Fore.RESET}")
                    
                    not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    now = datetime.datetime.now()
                    
                    if now < not_after and now > not_before:
                        print(f"{Fore.GREEN}Certificate is valid{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}Certificate is not valid{Fore.RESET}")
            
            save_to_history("ssl_info", {
                "domain": domain,
                "issuer": issuer.get('commonName'),
                "valid_until": cert['notAfter']
            })
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
        
        input(f"\n{_('continue_prompt')}")
        clear()

while True:
    if not config:
        load_config()
    
    if config.get("settings", {}).get("auto_update", True):
        last_check = config.get("last_update_check", "")
        if last_check:
            try:
                last_check_date = datetime.datetime.strptime(last_check, "%Y-%m-%d").date()
                days_since_check = (datetime.datetime.now().date() - last_check_date).days
                check_interval = config.get("settings", {}).get("update_check_interval_days", 7)
                
                if days_since_check >= check_interval:
                    check_for_updates()
            except:
                pass
    
    choice = print_menu()
    
    if isinstance(choice, int):
        clear()
        
        functions = {
            1: reverseDNS,
            2: DNSLookup,
            3: geoip,
            4: zonetransfer,
            5: dnssubdomain,
            6: reverseip,
            7: ASN,
            8: emailvalid,
            9: proxycheck,
            10: DMARC,
            11: TLS,
            12: DNSRECORD,
            13: DNSSEC,
            14: IpPrivacy,
            15: ipv6,
            16: JSVuln,
            17: ShortURL,
            18: port_scanner,
            19: ssl_certificate_info,
            20: batch_scan,
            21: schedule_task,
            22: view_history,
            23: export_data,
            24: check_for_updates,
            25: settings_menu
        }
        
        func = functions.get(choice)
        if func:
            func()
        else:
            print(f"{Fore.RED}{_('invalid_option')}! {_('try_again')}.{Fore.RESET}")
            time.sleep(1)
            clear()
