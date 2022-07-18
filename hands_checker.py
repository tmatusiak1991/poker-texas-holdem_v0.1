import collections
# HELPER FUNCTIONS

# Taking all cards from player/computer and getting only list of colors, which is needed to checking Flush
def get_colors_only(all_cards: list):
    temp_colors_list = []
    for cards in all_cards:
        temp_colors_list.append(cards[1])
    return(temp_colors_list)

# Taking all cards from player/computer and getting only list of figures, which is needed to checking e.g. Straight
def get_figures_only(all_cards: list):
    temp_figures_list = []
    for cards in all_cards:
        temp_figures_list.append(cards[0])
    return(temp_figures_list)

#  Making collection of figures, which is needed to count occurence of each figure to check 4 of a kind or 2 pairs etc.
def make_figures_collection(all_cards: list):
    figures = get_figures_only(all_cards)
    figures_counter = dict(collections.Counter(figures))
    return figures_counter


# CHECKER FUNCTIONS

def check_flush(all_cards: list):
    colors = get_colors_only(all_cards)
    colors_counter = dict(collections.Counter(colors))

    for color, occurence in colors_counter.items():
        if occurence >= 5:
            color_to_find = color
            for card, color in all_cards:
                if color == color_to_find:
                    return (card[0])
    return False

def check_straight(all_cards: list):
    figures = get_figures_only(all_cards)
    figures_no_duplicates = sorted(set(figures), key = lambda x: x[1], reverse=True)

    # Terrible notation, but it is working fine at this point of time, priority to change in next version..
    # TODO SIMPLYFIY THAT WITH SOME LOOP AND MOVE TO SEPARATE FUNCTION
    if len(figures_no_duplicates) == 7:

        if figures_no_duplicates[0][1] - figures_no_duplicates[4][1] == 4:
            return (figures_no_duplicates[0][0])
        elif figures_no_duplicates[1][1] - figures_no_duplicates[5][1] == 4:
            return (figures_no_duplicates[1][0])
        elif figures_no_duplicates[2][1] - figures_no_duplicates[6][1] == 4:
            return (figures_no_duplicates[2][0])
        # this is special case when there is straight 5 4 3 2 A
        elif (figures_no_duplicates[3][1] - figures_no_duplicates[6][1] == 3) and figures_no_duplicates[0][1] == 14 and figures_no_duplicates[6][1] == 2:    
            return (figures_no_duplicates[3][0])

    elif len(figures_no_duplicates) == 6:

        if figures_no_duplicates[0][1] - figures_no_duplicates[4][1] == 4:
            return (figures_no_duplicates[0][0])
        elif figures_no_duplicates[1][1] - figures_no_duplicates[5][1] == 4:
            return (figures_no_duplicates[1][0])
        elif (figures_no_duplicates[2][1] - figures_no_duplicates[5][1] == 3) and figures_no_duplicates[0][1] == 14 and figures_no_duplicates[5][1] == 2:    
            return (figures_no_duplicates[3][0])

    elif len(figures_no_duplicates) == 5:

        if figures_no_duplicates[0][1] - figures_no_duplicates[4][1] == 4:
            return (figures_no_duplicates[0][0])
        elif (figures_no_duplicates[1][1] - figures_no_duplicates[4][1] == 3) and figures_no_duplicates[0][1] == 14 and figures_no_duplicates[4][1] == 2:    
            return (figures_no_duplicates[3][0])

    return False

def check_four(all_cards: list):
    figures_counter = make_figures_collection(all_cards)

    for figure, occurence in figures_counter.items():
        if occurence == 4:
            return (figure[0])

    return False

def check_rest_hands(all_cards: list):
    figures_counter = make_figures_collection(all_cards)

    # sorting figures collection
    sorted_figures_counter = dict(sorted(figures_counter.items(), key = lambda x: x[1], reverse=True))
    # making set of figures to simplify checking all configurations of remaing hands
    figures_set = list(sorted_figures_counter.values())

    # need to separate that for 2 elements for some hands, e.g. in Full House: AAA = first_hand_elem KK = second_hand_elem
    first_hand_elem = list(sorted_figures_counter.keys())[0][0]
    second_hand_elem = list(sorted_figures_counter.keys())[1][0]

    # FULL HOUSE
    if figures_set == [3,3,1] or figures_set == [3,2,2] or figures_set == [3,2,1,1]:
        return (7, first_hand_elem, second_hand_elem)
    # THREE OF A KIND
    elif figures_set == [3,1,1,1,1]:
        return (4, first_hand_elem, 0)
    # TWO PAIRS
    elif figures_set == [2,2,2,1] or figures_set == [2,2,1,1,1]:
        return (3, first_hand_elem, second_hand_elem)
    # PAIR
    elif figures_set == [2,1,1,1,1,1]:
        return (2, first_hand_elem, 0)

    return False