from hands_power import get_hands_rank

# PRINTABLE HELPER FUNCTIONS
def print_cards(hand: list):
    # Converting tuple to easy to read format
    printable_hand = ""
    for card in hand:
        printable_hand += card[0][0] + card[1] + " "

    return printable_hand

def print_game_state(stage: str, player_cards: list, computer_cards: list, table_cards: list):
    
    print(f"{50*'-'}{stage}{50*'-'}")
    print(f"Your  cards: {print_cards(player_cards)}")
    print(f"Comp  cards: {print_cards(computer_cards)}")
    # In future version, computer's cards should be hidden
    # print(f"Comp  cards: XX XX")
    print(f"Table cards: {print_cards(table_cards)}")

def print_highest_hand(best_hand: tuple):
    printable_hand = ""
    printable_hand += get_hands_rank(best_hand[0])

    # Assigning different format of preposition depending on hand to make print statement nicer

    if best_hand[0] == 10 or best_hand[0] == 9 or best_hand[0] == 6 or best_hand[0] == 5:
        printable_hand += f" from {best_hand[1]}"
    elif best_hand[0] == 8 or best_hand[0] == 4 or best_hand[0] == 2:
        printable_hand += f" of {best_hand[1]}"
    elif best_hand[0] == 7 or best_hand[0] == 3:
        printable_hand += f": {best_hand[1]} and {best_hand[2]}"
    else:
        printable_hand += f": {best_hand[1]}"

    return printable_hand