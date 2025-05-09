import random
import time
import sys
import os
import requests

try:
    from colorama import Fore, Style, init
except ImportError:
    os.system('pip install colorama')
    from colorama import Fore, Style, init

init(autoreset=True)

# --- Animation d'introduction hacker --- (ajustée pour défilement rapide en 3 secondes avec couleurs)
def hacker_intro(duration=3):
    start_time = time.time()
    while time.time() - start_time < duration:
        line = ''.join(random.choice(['0', '1']) for _ in range(80))
        color = random.choice([Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA])  # Choix de la couleur aléatoire
        sys.stdout.write("\r" + color + line)  # Affiche sur la même ligne
        sys.stdout.flush()
        time.sleep(0.04)  # Vitesse encore plus rapide pour 3 secondes
    print()  # Pour un saut de ligne après l'animation

# --- Affichage du banner DARK_DANTE ---
def display_banner():
    print(Fore.RED + Style.BRIGHT + """
  
                       ░▒█▀▀▄░█▀▀▄░▒█▀▀▄░▒█░▄▀░░░▒█▀▀▄░█▀▀▄░▒█▄░▒█░▀▀█▀▀░▒█▀▀▀
                       ░▒█░▒█▒█▄▄█░▒█▄▄▀░▒█▀▄░░░░▒█░▒█▒█▄▄█░▒█▒█▒█░░▒█░░░▒█▀▀▀
                       ░▒█▄▄█▒█░▒█░▒█░▒█░▒█░▒█░░░▒█▄▄█▒█░▒█░▒█░░▀█░░▒█░░░▒█▄▄▄
  
    Coded by DARK_DANTE - Hack The System T.me/DARK_DANTE_OFF +221784180290⚡
    """)
    print(Style.RESET_ALL)

# --- Génération de cartes ---
def complete_bin(bin_pattern):
    completed = ""
    for c in bin_pattern:
        if c == 'x':
            completed += str(random.randint(0, 9))
        else:
            completed += c
    while len(completed) < 15:
        completed += str(random.randint(0, 9))
    return completed

def luhn_complete(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return (10 - checksum % 10) % 10

def generate_card(bin_pattern):
    incomplete = complete_bin(bin_pattern)
    incomplete = incomplete[:15]
    check_digit = luhn_complete(incomplete)
    return incomplete + str(check_digit)

def random_bin():
    brand = random.choice(['4', '5'])
    bin_rest = ''.join(str(random.randint(0, 9)) for _ in range(5))
    return brand + bin_rest + "xxxx"

def generate_cards(bin_input, quantity, output_file="cards.txt"):
    try:
        bin_pattern, month, year, cvv_mode = bin_input.split("|")
    except ValueError:
        print(Fore.RED + "Erreur : format invalide. Exemple : 542432360758xxxx|08|2026|rnd")
        return

    cards = []
    for _ in range(quantity):
        card_number = generate_card(bin_pattern)
        cvv = str(random.randint(100, 999)) if cvv_mode.lower() == "rnd" else cvv_mode
        cards.append(f"{card_number}|{month}|{year}|{cvv}")

    with open(output_file, "w") as f:
        for card in cards:
            f.write(card + "\n")

    print(Fore.GREEN + f"[+] {quantity} cartes générées et enregistrées dans {output_file}.")

# --- Checker des cartes ---
def luhn_check(card_number):
    card_number = card_number.replace(" ", "").strip()
    digits = [int(d) for d in card_number]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0

def get_info_from_bin(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            country = data.get("country", {}).get("name", "Inconnu")
            bank = data.get("bank", {}).get("name", "Inconnu")
            card_type = data.get("type", "Inconnu")
            return f"{country} - {bank} - {card_type.upper()}"
        else:
            return "Inconnu"
    except Exception:
        return "Inconnu"

def check_cards(file_path="cards.txt"):
    try:
        with open(file_path, 'r') as file:
            cards = file.readlines()
    except FileNotFoundError:
        print(Fore.RED + f"Erreur : Fichier '{file_path}' introuvable.")
        return

    valid_cards = []
    invalid_cards = []

    for line in cards:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) >= 1:
            card_number = parts[0]
            bin_number = card_number[:6]
            info = get_info_from_bin(bin_number)
            if luhn_check(card_number):
                print(Fore.GREEN + f"[VALIDE]   {line} [{info}]")
                valid_cards.append(f"{line} [{info}]")
            else:
                print(Fore.RED + f"[INVALIDE] {line} [{info}]")
                invalid_cards.append(f"{line} [{info}]")

    with open("valid_cards.txt", "w") as f:
        for card in valid_cards:
            f.write(card + "\n")

    with open("invalid_cards.txt", "w") as f:
        for card in invalid_cards:
            f.write(card + "\n")

    print(Fore.CYAN + f"[+] {len(valid_cards)} cartes valides sauvegardées dans valid_cards.txt")
    print(Fore.CYAN + f"[+] {len(invalid_cards)} cartes invalides sauvegardées dans invalid_cards.txt")

# --- Menu principal ---
def menu():
    while True:
        print(Fore.CYAN + "\n--- MENU DARK_DANTE TOOL ---")
        print("[1] Générer des cartes")
        print("[2] Checker des cartes")
        print("[3] Quitter")
        choix = input(Fore.YELLOW + "Choisis une option: ")

        if choix == "1":
            bin_input = input(Fore.YELLOW + "Entre ton BIN (ex: 542432360758xxxx|08|2026|rnd) ou laisse vide pour automatique : ").strip()
            if bin_input == "":
                print(Fore.GREEN + "[!] Aucun BIN entré, génération automatique...")
                bin_generated = random_bin()
                mois = str(random.randint(1, 12)).zfill(2)
                annee = random.randint(2025, 2030)
                bin_input = f"{bin_generated}|{mois}|{annee}|rnd"
                print(Fore.GREEN + f"[+] BIN généré: {bin_input}")
            quantity = int(input(Fore.YELLOW + "Combien de cartes veux-tu générer ? "))
            generate_cards(bin_input, quantity)

        elif choix == "2":
            fichier = input(Fore.YELLOW + "Nom du fichier à checker (laisser vide = cards.txt) : ").strip()
            if fichier == "":
                fichier = "cards.txt"
            check_cards(fichier)

        elif choix == "3":
            print(Fore.RED + "Fermeture... À bientôt DARK_DANTE 👾")
            break

        else:
            print(Fore.RED + "Option invalide, réessaye frérot.")

# --- Lancement ---
if __name__ == "__main__":
    hacker_intro(3)  # Animation plus rapide en 3 secondes
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    menu()
