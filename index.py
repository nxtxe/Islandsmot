# Artjom Pushkar // Vor 2025

import random
import time

# Spyr notanda um nafn
player_name = input("Hvað heitir þú? ")

# Veljum leik (1: Klasískur leikur, 2: Leikur með Upphæð)
while True:
    mode_input = input("Veldu leik (1: Klasískur, 2: Með Upphæð): ").strip()
    if mode_input in ['1', '2']:
        break
    else:
        print("Rangt inntak. Veldu 1 eða 2.")
betting_mode = (mode_input == '2')

# Ef leikur með Upphæð, spyrjum notanda um upphaflegan isk.
if betting_mode:
    while True:
        try:
            starting_balance = int(input("Sláðu inn upphaflegan isk. fyrir alla leikmenn: "))
            if starting_balance > 0:
                break
            else:
                print("isk. þarf að vera jákvæð tala.")
        except ValueError:
            print("Rangt inntak. Sláðu inn tölu.")

# Veljum fjölda tölvuleikmanna (1 til 3)
while True:
    try:
        num_computers = int(input("Sláðu inn fjölda tölvuleikmanna (1-3): "))
        if 1 <= num_computers <= 3:
            break
        else:
            print("Veldu tölu á bilinu 1 til 3.")
    except ValueError:
        print("Rangt inntak. Sláðu inn tölu.")

# Búum til spilastokkinn með hefðbundnum spilum
suits = ['♥', '♦', '♣', '♠']
def new_deck():
    # Skilar nýjum spilastokk með spilum 1 til 13 og fjórum deildum
    return [(value, suit) for value in range(1, 13) for suit in suits]

deck = new_deck()

# Skilgreinum leikmann með upphafsgögnum (gildir fyrir bæði notanda og tölvuleikmenn)
def create_player(name, p_type):
    player = {
        'name': name,      # Nafn leikmanns
        'type': p_type,    # Tegund: 'human' fyrir notanda, 'computer' fyrir tölvuleikmann
        'cards': [],       # Listi af spulum sem leikmaðurinn hefur
        'sum': 0,          # Heildarupphæð spila
        'win': 0           # Fjöldi rúna sigra
    }
    if betting_mode:
        # Ef leikur með Upphæð, stillum upphaflegan isk.
        player['balance'] = starting_balance
    return player

# Búum til lista af leikmönnum: Fyrsti er notandinn, síðan tölvuleikmenn
players = [create_player(player_name, 'human')]
for i in range(1, num_computers + 1):
    players.append(create_player(f"Leikmaður {i}", 'computer'))

def giveUpdate():
    """
    Velur slembið spili (gildi og deild) úr stokknum og fjarlægir það.
    """
    global deck # Global leyfir að nota data og breyta það
    card = random.choice(deck) # gefur spil
    deck.remove(card)
    return card

def giveCard(who):
    """
    Úthlýtur slembið spili til leikmanns eða tölvu.
    Bætir spilinu (tupill með gildi og deild) við lista who['cards']
    og eykur summuna um gildið á spilinu.
    """
    card = giveUpdate()  # Dregum spilið úr stokknum
    value = card[0]
    who['cards'].append(card) # bætum i spil leikmanns
    who['sum'] += value # breytum summu spila
    return card

def human_turn(player):
    """
    Leikur fyrir mannleikmanninn.
    Notandinn dregur spil og velur hvernig ásinn skal teljast (1 eða 15).
    """
    print(f"\n{player['name']}, þinn umferð hefst.")
    while True:
        card = giveCard(player)
        # Ef ás kemur upp, bjóðum við notandanum að velja gildið 1 eða 15
        if card[0] == 1:
            while True:
                try:
                    choice = int(input(f"\nÞú fékkst {card[0]}{card[1]}. Vilt þú nota það sem 1 eða 15? "))
                    if choice == 15:
                        player['sum'] += 14   # Bætum við 14 til að breyta 1 í 15
                        player['cards'][-1] = (15, card[1])
                        break
                    elif choice == 1:
                        break
                    else:
                        print("Rangur innsláttur. Veldu 1 eða 15.")
                except ValueError:
                    print("Rangur innsláttur. Sláðu inn tölu (1 eða 15).")
        # Ef summa fer yfir 30, tapar leikmaðurinn
        if player['sum'] > 30:
            print(f"\n{player['name']}, þú tapaðir! Þú ert með summu {player['sum']}.")
            print(f"Spil þín: {', '.join(f'{c[0]}{c[1]}' for c in player['cards'])}") # print með for lykkju inni til að prenta allt
            break
        else:
            print(f"\n{player['name']}, þú hefur spil: {', '.join(f'{c[0]}{c[1]}' for c in player['cards'])}")
            print(f"Þín summa spila: {player['sum']}")
            cont = input("Vilt þú halda áfram? (y/n) ").strip().lower()
            while cont not in ['y', 'n']:
                cont = input("Rangt innsláttur. Sláðu inn y eða n: ").strip().lower()
            if cont == 'n':
                break

def computer_turn(player):
    """
    Leikur fyrir tölvuleikmanninn.
    Tölvan dregur spil þar til summan er 24 eða meira.
    Ef ás kemur upp, er notað gildið 15 ef það leyfir ekki fara yfir 30.
    """
    print(f"\n{player['name']} byrjar að drekka spil.")
    while player['sum'] < 24:
        card = giveCard(player)
        if card[0] == 1 and player['sum'] + 14 < 30:
            player['sum'] += 14
            player['cards'][-1] = (15, card[1])
        current_output = f"{player['name']}, þú hefur spil: {', '.join(f'{c[0]}{c[1]}' for c in player['cards'])}"
        print("\r" + current_output, end="", flush=True) # prentum spil tölva i eina linu til að gera output hreinara
        time.sleep(0.5)
        if player['sum'] > 30:
            break
    print(f"\n{player['name']}'s summan: {player['sum']}")

def get_bet(player):
    """
    Fá stöðu frá leikmanni.
    Ef notandi spilar, beðið um að slá inn veðmátt á bilinu 1 til isk. hans.
    Fyrir tölvuleikmenn er notuð einföld stefna (veðja 10 eða allt ef minni).
    """
    if player['type'] == 'human':
        while True:
            try:
                bet = int(input(f"{player['name']}, sláðu inn þína veðmátt (1 til {player['balance']}): "))
                if 1 <= bet <= player['balance']:
                    return bet
                else:
                    print("Ógilt upphæð. Reyndu aftur.")
            except ValueError:
                print("Rangt innsláttur, sláðu inn tölu.")
    else:
        # Einföld stefna fyrir tölvuleikmenn: veðja 10 eða, ef isk. er minna, öll peningarnir
        bet = 10 if player['balance'] >= 10 else player['balance']
        print(f"{player['name']} veðjar {bet}")
        return bet

def endGame():
    """
    Spyr hvort leikmaður vill spila aftur.
    Ef já – endurstillir gögn (spil og summur) og endurheimtir spilastokkinn,
    annars lokar leiknum.
    """
    global deck
    while True:
        userInput = input("\nVilt þú spila aftur? (y/n) ").strip().lower()
        if userInput in ['y', 'n']:
            break
        else:
            print("Rangt val. Sláðu inn y eða n.")
    if userInput == 'y':
        deck = new_deck()
        # Endurstillum spil og summu fyrir hvern leikmann
        for p in players:
            p['cards'] = []
            p['sum'] = 0
        return True
    else:
        return False

while True:
    deck = new_deck()
    for p in players:
        p['cards'] = []
        p['sum'] = 0

    pot = 0  # Sameinuð upphæð Staða
    if betting_mode:
        print("\nStaða ")
        for p in players:
            if p.get('balance', 0) > 0:
                p['bet'] = get_bet(p)
                p['balance'] -= p['bet']
                pot += p['bet']
            else:
                p['bet'] = 0
        print(f"Heildar pot: {pot}")

    #  Leik umferðir: Hver leikmaður tekur sína umferð 
    for p in players:
        # Ef leikmaður hefur ekki nægan isk. (í Staðaa ham) eða er útskrifaður, sleppum við
        if betting_mode and p.get('balance', 0) <= 0:
            continue
        if p['type'] == 'human':
            human_turn(p)
        else:
            computer_turn(p)

    #  Ákveðum round vinnara
    eligible = [p for p in players if p['sum'] <= 30]
    if not eligible:
        print("\nAllir fóru yfir 30. Enginn vinnir runduna.")
        winners = []
    else:
        max_sum = max(p['sum'] for p in eligible)
        winners = [p for p in eligible if p['sum'] == max_sum]
    
    if len(winners) == 1:
        winner = winners[0]
        print(f"\nVann: {winner['name']} með summu {winner['sum']}")
        winner['win'] += 1
        if betting_mode:
            print(f"{winner['name']} vinnur potið {pot}!")
            winner['balance'] += pot
    else:
        print("\nJafntefli milli:")
        for w in winners:
            print(f"{w['name']} með summu {w['sum']}")
        if betting_mode:
            # Ef jafntefli, endurgreiðum stöðu
            for p in players:
                p['balance'] += p.get('bet', 0)
            print("Staða endurgreidd vegna jafntefli.")

    #  Sýnum stöðu leikmanna 
    print("\nStaða ")
    for p in players:
        if betting_mode:
            print(f"{p['name']} - isk.: {p['balance']} | vinningar: {p['win']}")
        else:
            print(f"{p['name']} - vinningar: {p['win']}")

    # Ef leikur með Upphæð, athugum hvort notandi hafi tapað öllum peningunum eða sé einn eftir
    if betting_mode:
        # Fjarum leikmönnum sem hafa 0 eða minna isk.
        players = [p for p in players if p['balance'] > 0]
        if not any(p['type'] == 'human' for p in players):
            print("\nÞú hefur tapað öllum peningunum. Leik lokið.")
            break
        if len(players) < 2:
            print("\nEinungis einn leikmaður eftir. Leik lokið.")
            break

    if not endGame():
        print("\nTakk fyrir að spila!")
        break
