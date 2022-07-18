from random import shuffle
from hands_checker import check_flush, check_straight, check_four, check_rest_hands
from print_functions import print_game_state, print_highest_hand
from hands_power import evaluate_hands_power
from basic_deck import get_colors, get_figures

# ---------------------------------------------------------------INITALIZING DECK OF CARDS

def initalize_full_deck():
    colors = get_colors()
    figures = get_figures()
    deck = []

    for color in colors:
        for key, value in figures.items():
            deck.append(((key, value), color))

    shuffle(deck)
    return deck

def deal(cards_no: int, deck: list):
    hand = []
    
    for i in range (cards_no):
        hand.append(deck.pop())

    return hand
# ---------------------------------------------------------------EO INITALIZING

# ---------------------------------------------------------------HANDS CHECKING
def check_best_hand(all_cards: list):
    sorted_cards = sorted(all_cards, key = lambda x: x[0][1], reverse=True)

    flush_checker = check_flush(sorted_cards)
    straight_checker = check_straight(sorted_cards)
    four_checker = check_four(sorted_cards)

    # return tuple from ifs below = (A, B, C) where:
    # A = hand power (e.g. flush) 
    # B = highest card/cards in hand power from point A, e.g. if B = "Q" and A = "Flush" it means that Q is highest card from this flush
    # C = in some hands, there is need to egzamine second "highest" card to check which hand is better, e.g. when both players have 2 pairs QQ JJ is higher than QQ 66

    # ROYAL FLUSH  # 9
    if flush_checker != False and straight_checker == "A":
        return (9, "A", 0)
    # Straight flush # 8
    elif flush_checker != False and straight_checker != False:
        return (8, straight_checker, 0)
    # Four of a kind # 7
    elif four_checker != False:
        return (7, four_checker, 0)
    # Flush # 6
    elif flush_checker != False:
        return (6, flush_checker, 0)
    # Straight # 5
    elif straight_checker != False:
        return (5, straight_checker, 0)
    
    # All other hands
    rest_hands = check_rest_hands(sorted_cards)
    if rest_hands != False:
        return (rest_hands[0], rest_hands[1], rest_hands[2])
    else:
        return (1,sorted_cards[0][0][0], 0)
# --------------------------------------------------------------- EO HANDS CHECKING

def money_operations(small_blind: int, big_blind: int, p_1_chips: int, p_2_chips: int):
    # p1 should be small blind normally, but in this version there is no possibliy to fold, so every time player is playing big blind also; this will be fixed in new version
    # p_1_to_substract = small_blind

    p_1_to_substract = big_blind
    p_2_to_substract = big_blind

    # Checking if chips which needs to be deducted are not bigger than p1 chips -> if yes; p2 can only have same amount deducted from his account
    if p_1_to_substract >= p_1_chips:
        p_1_to_substract = p_1_chips
        p_2_to_substract = p_1_chips

    # Checking if chips which needs to be deducted are not bigger than p2 chips -> if yes; p1 can only have same amount deducted from his account
    if p_2_to_substract >= p_2_chips:
        p_1_to_substract = p_2_chips
        p_2_to_substract = p_2_chips
    
    return(p_1_to_substract, p_2_to_substract)



# ---------------------------MAIN GAME------------------------------------------------------
def main_game():
    # Initialize Game State = Starting chips stake; small blind size; who is starting game as small blind

    # Variable Values
    starting_chips = 100
    small_blind = 10
    rounds_till_small_incease = 5
    # Constant Values
    player_on_small = True
    main_pot = 0
    round_no = 1
    game_stages = ["FLOP", "TURN", "RIVER"]
    player_chips = starting_chips
    computer_chips = starting_chips

    # Main loop
    while True:
        deck = initalize_full_deck()
        big_blind = small_blind * 2

        player_cards = deal(2, deck)
        computer_cards = deal(2, deck)
        
        # Checking how many chips to deduct from chips account; if player is on small; player has 1st turn and computer 2nd turn
        if player_on_small == True:
            chips_deduct_tuple = money_operations(small_blind, big_blind, player_chips, computer_chips)
            player_pot = chips_deduct_tuple[0]
            computer_pot = chips_deduct_tuple[1]
        else:
            chips_deduct_tuple = money_operations(small_blind, big_blind, computer_chips, player_chips)
            computer_pot = chips_deduct_tuple[0]
            player_pot = chips_deduct_tuple[1]

        # Deducting money from players account and adding it to main pot
        player_chips -= player_pot
        computer_chips -= computer_pot
        main_pot += player_pot + computer_pot

      
        # Only to show who is on small blind
        if player_on_small == True:
            who_on_small = "Player"
        else:
            who_on_small = "Computer"

        # print to show initial round status
        # TODO change format of that, maybe move to some function

        print(f"{20*'#'} STARTING ROUND {round_no} {20*'#'}")
        print(f"# Small blind:  {small_blind}$    ||  Big blind: {big_blind}$")
        print(f"# Small blind:  {who_on_small.upper()}")
        print(f"# Player chips: {player_chips}$   ||  Computer chips: {computer_chips}$    ||  POT: {main_pot}$ \n")


        # Loop to go throught all game stages (Flop, turn, river), in the future this loop will be significantly enhanced
        # TODO enhance this module in next version of program
        for stage in game_stages:
            if stage == "FLOP":
                table_cards = deal(3, deck)
            else:
                table_cards += deal(1, deck)

            print_game_state(stage, player_cards, computer_cards, table_cards)
            # below will be replace by new module with decision tree - if user wants to raise or fold etc., in this version we can only go to next stage
            next_step = (input("Press any key to go to next stage."))



        # adding table cards to player & computer hand to check best hand
        player_all_cards = player_cards + table_cards
        computer_all_cards = computer_cards + table_cards
        
        # Checking best hand power
        player_best_hand = check_best_hand(player_all_cards)
        computer_best_hand = check_best_hand(computer_all_cards)

        # print to show best hands
        # TODO change format of that, maybe move to some function
        print(f"{50*'-'}RESULT{49*'-'}")
        print(f"Player best hand:   {print_highest_hand(player_best_hand)} ")
        print(f"Computer best hand: {print_highest_hand(computer_best_hand)} \n")

        game_result = evaluate_hands_power(player_best_hand, computer_best_hand)

        # Checking who won current round 
        # TODO change format of that, maybe move to some function
        if game_result == "player_won":
            print("PLAYER WINS!")
            player_chips += main_pot
            main_pot = 0
        elif game_result == "computer_won":
            computer_chips += main_pot
            main_pot = 0
            print("COMPUTER WINS!")
        else:
            player_chips += int(main_pot / 2)
            computer_chips += int(main_pot / 2)
            main_pot = 0
            print("DRAW")

        print(f"Player chips: {player_chips}$  || Computer chips: {computer_chips}$ \n")


        # Checking if game is over
        # TODO change format of that, maybe move to some function
        if player_chips == 0:
            print(f"{50*'%'}")
            print("You are bankrupt! You are loser!")
            print(f"Computer won in {round_no} rounds")
            print(f"{50*'%'}")
            break
        elif computer_chips == 0:
            print(f"{50*'%'}")
            print("Congratulations! You are winner!")
            print(f"Player won in {round_no} rounds")
            print(f"{50*'%'}")
            break
        
        # reverse 
        player_on_small = not player_on_small
        
        print(f"{105*'-'}")
        print("Do you want to play next round?")
        next_step = (input("Press any key to continue; 0 to exit \n"))
        if next_step == "0":
            break
        round_no += 1

        # small blind increases by 10$ after each X rounds to speed up game; 
        if round_no % rounds_till_small_incease == 0:
            small_blind += 10


    print("Thanks for playing!")
    




main_game()