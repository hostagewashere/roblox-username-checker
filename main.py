import requests
from colorama import Fore, Style
import os

def send_to_discord_webhook(webhook_url, username, ping_everyone):
    content = "@everyone" if ping_everyone else ""
    embed = {
        "title": "🎉 Username Available! 🎉",
        "description": f"The username `{username}` is **available** on Roblox!",
        "color": 0x00FF00,  # Green color
        "footer": {
            "text": "Roblox Username Validator"
        }
    }
    data = {
        "content": content,  # Ping everyone if enabled
        "embeds": [embed]  # Include the embed
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"{Fore.RED}Failed to send to Discord webhook{Style.RESET_ALL}")

def validate_username(username, use_webhook, webhook_url, ping_everyone):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            print(f"{Fore.GREEN} '{username}' is available{Style.RESET_ALL}")
            if use_webhook:
                send_to_discord_webhook(webhook_url, username, ping_everyone)
            else:
                with open('valid.txt', 'a') as file:
                    file.write(username + '\n')
        elif data['code'] == 1:
            print(f"{Fore.RED} '{username}' is already in use{Style.RESET_ALL}")
        elif data['code'] == 2:
            print(f"{Fore.RED} '{username}' is not appropriate for Roblox{Style.RESET_ALL}")
        elif data['code'] == 10:
            print(f"{Fore.YELLOW} '{username}' might contain private information{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Unable to access Roblox API{Style.RESET_ALL}")

def validate_usernames_from_file(filename, use_webhook, webhook_url, ping_everyone):
    with open(filename, "r") as file:
        usernames = file.read().splitlines()
    for username in usernames:
        validate_username(username, use_webhook, webhook_url, ping_everyone)

def display_rainbow_ascii_art():
    rainbow_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    ascii_art = [
        " _______     ___   _____       ___     ____   ____ ",
        "|_   __ \\  .'   `.|_   _|    .'   `.  |_  _| |_  _|",
        "  | |__) |/  .-.  \\ | |     /  .-.  \\   \\ \\   / /  ",
        "  |  ___/ | |   | | | |   _ | |   | |    \\ \\ / /   ",
        " _| |_    \\  `-'  /_| |__/ |\\  `-'  /     \\ ' /    ",
        "|_____|    `.___.'|________| `.___.'       \\_/     "
    ]
    for i, line in enumerate(ascii_art):
        color = rainbow_colors[i % len(rainbow_colors)]  # Cycle through rainbow colors
        print(color + line + Style.RESET_ALL)
    print(f"{Fore.CYAN}Made by Hostage{Style.RESET_ALL}")  # Added "Made by Hostage"

def get_webhook_name(webhook_url):
    # Extract the webhook name from the URL (the part after /webhooks/)
    parts = webhook_url.split("/webhooks/")
    if len(parts) > 1:
        return parts[1].split("/")[0]  # Get the webhook name
    return "Unknown Webhook"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console

def main():
    webhook_url = None
    use_webhook = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to use a Discord webhook? (y/n): ").lower() == 'y'
    if use_webhook:
        webhook_url = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter your Discord webhook URL: ")
        webhook_name = get_webhook_name(webhook_url)
    else:
        webhook_name = None

    while True:
        print()
        clear_console()  # Clear console
        display_rainbow_ascii_art()  # Display rainbow ASCII art

        # Display "Logged in as" message if a webhook is used
        if use_webhook and webhook_name:
            print(f"{Fore.GREEN}Logged in as: {webhook_name}{Style.RESET_ALL}")

        print()
        print(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Choose an option:")
        print(f"{Fore.MAGENTA}[{Fore.RESET}1{Fore.MAGENTA}]{Fore.RESET} Manually enter a username")
        print(f"{Fore.MAGENTA}[{Fore.RESET}2{Fore.MAGENTA}]{Fore.RESET} Check a list of usernames from a file")
        print(f"{Fore.MAGENTA}[{Fore.RESET}0{Fore.MAGENTA}]{Fore.RESET} Exit")
        choice = input(f"{Fore.MAGENTA}[{Fore.RESET}>{Fore.MAGENTA}]{Fore.RESET} ")

        if choice == '1':
            clear_console()  # Clear console before checking
            username = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter a username: ")
            ping_everyone = False
            if use_webhook:
                ping_everyone = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to ping @everyone? (y/n): ").lower() == 'y'
            validate_username(username, use_webhook, webhook_url, ping_everyone)
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press Enter to continue...")  # Pause before returning to the menu
        elif choice == '2':
            clear_console()  # Clear console before checking
            filename = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter the filename of the usernames file (must include .txt): ")
            ping_everyone = False
            if use_webhook:
                ping_everyone = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to ping @everyone? (y/n): ").lower() == 'y'
            validate_usernames_from_file(filename, use_webhook, webhook_url, ping_everyone)
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press Enter to continue...")  # Pause before returning to the menu
        elif choice == '0':
            break
        else:
            print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press Enter to continue...")  # Pause before returning to the menu

if __name__ == "__main__":
    main()