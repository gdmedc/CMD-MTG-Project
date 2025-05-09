# Author: Guillermo Medina
import time
import requests
import json
import numpy
from art import *


def scryfall(params=None):
    """
    Call scryfall API for card data

    Args:
        params (string, optional): Parameters for scryfall search. Defaults to None.

    Returns:
        string: JSON string containing card data
    """
    # Run search with parameters, if any
    url = "https://api.scryfall.com/cards"
    if params != None:
        url += params

    response = requests.get(url)
    return response.json()

def record(score):
    """
    Read/write high score from/to file

    Args:
        score (int): tally of earned points
    """
    # Read high score from file
    fScore = open("highscore.txt","r+")  
    highScore = numpy.loadtxt("highscore.txt", usecols = 1, dtype = int)

    # If no data is present, given name and score are new high score
    if highScore.size == 0:
        highScore = score
    # If new score is greater than or equal to high score, overwrite high score   
    if score >= highScore:
        print("New High Score!")
        name = "" + input("Enter your name: ")
        if name == "":
            name = "DEFAULT"
        # Erase spaces from name
        name = name.replace(" ","")
        newScore = name + " " + str(score) + " points"
        
        fScore.truncate(0)
        fScore.seek(0)
        fScore.write(newScore)
    else:
        print("Too Bad! You Failed to Beat Your High Score.")
    
    fScore.close()

def print_score():
    """
    Print high score from highscore.txt file
    """
    fScore = open("highscore.txt","r+")
    line = fScore.read()
    fScore.close
    print()
    print("--------------------High Score--------------------")
    print("Current High Score: ", line)
    print()

    input("Press an key to return to main menu: ")
    print()
    
def print_card(card):
    """
    Prints text of given card

    Args:
        card (string): JSON string holding all card properties 
    """
    # Some cards have special formatting that must be accounted for
    if card["layout"] != "normal":
        # Print each card face
        for i in range(2):
            print("Name: ", card["card_faces"][i]["name"], "\t", "Mana Cost: ", card["card_faces"][i]["mana_cost"])
            print("Type: ", card["card_faces"][i]["type_line"], "\t", "Rarity: ", card["rarity"])
            print("Card Text:\n", card["card_faces"][i]["oracle_text"])
            
            if "Creature" in card["card_faces"][i]["type_line"]:
                print("Power/Toughness:","\t", card["card_faces"][i]["power"],"/",card["card_faces"][i]["toughness"])
            if "Planeswalker" in card["card_faces"][i]["type_line"]:
                print("Loyalty:","\t", card["card_faces"][i]["loyalty"])
            if "Battle" in card["card_faces"][i]["type_line"]:
                print("Defense:","\t", card["card_faces"][i]["defense"])
            print()
            
    else: 
        # Print normal card
        print("Name: ", card["name"], "\t", "Mana Cost: ", card["mana_cost"])
        print("Type: ", card["type_line"], "\t", "Rarity: ", card["rarity"])
        print("Card Text:\n", card["oracle_text"])
        if "Creature" in card["type_line"]:
            print("Power/Toughness:","\t", card["power"],"/",card["toughness"])
        if "Planeswalker" in card["type_line"]:
            print("Loyalty:","\t", card["loyalty"])
        if "Battle" in card["type_line"]:
            print("Defense:","\t", card["defense"])
            
def card_search():
    """
    Prompt user for a card name and output that card's text
    """
    loop = True
    while loop:
        print()
        print("--------------------Card Search--------------------")
        uInput = input("Enter a card name: ")
        uInput = uInput.replace(' ','+')
        query = '/named?fuzzy='
        query += uInput
                
        card = scryfall(query)
        if card["object"] == "error":
            uInput = input("Error occurred. Your search was invalid or there is a problem with Scryfall. Try again? Y/N: ")
            loop = True if uInput == 'y' or uInput == 'Y' else False
                
        else: 
            loop = False
            print()     
            print_card(card)
    
    print()
    input("Enter any key to continue: ")
    print()
    
def list_menu():
    """
    User menu for list search function

    Returns:
        int: Int representing user choice
    """
    print()
    loop = True
    while loop:
        choices = ["1) View the next 25 results", "2) View Card Details", "3) Return to menu"]
        for choice in choices:
            print(choice)

        uInput = input("Enter a number: ")
        print()
        match uInput:
            case '1':
                return 1
            case '2':
                return 2
            case '3':
                return 3 
            case _:
                print("Invalid input. Try again.")
                print()

def list_prompts():
    """
    Prompt user for search parameters

    Returns:
        string: String of search parameters 
    """
    query = "/search?q="
    # Prompt User for card types
    prompt = input("Search by Card Type? Y/N: ")
    if prompt == 'y' or prompt == 'Y': 
    # Allow user to add as many elements as they desire for each parameter
        uInput = input("Enter Card Types (Goblin, Planeswalker, Instant, etc.): ")
        uInput = uInput.replace(" ", "+t=")
        query += "t=" + uInput + "+"
    print()
    # Prompt user for color identity
    prompt = input("Search by Color Identity? Y/N: ")
    if prompt == 'y' or prompt == 'Y': 
        print("In MTG, colors are represented by single characters. Colored cards cannot be colorless.")
        uInput = input("Enter Card Colors as Characters (W - White, U - Blue, B - Black, R - Red, G - Green, or C - Colorless): ")
        uInput = uInput.replace(" ", "")
        query += "color=" + uInput + "+"
    print()    
    # Prompt user for cmc
    prompt = input("Search by Converted Mana Cost? Y/N: ")
    if prompt == 'y' or prompt == 'Y':
        # Cards only have 1 cmc
        uInput = input("Enter a CMC (0, 1, 2, 3, 4, 5, etc.): ")
        query += "cmc=" + uInput + "+"
    print()    
    # Prompt user for rarity
    prompt = input("Search by Card Rarity? Y/N: ")
    if prompt == 'y' or prompt == 'Y':
        # Cards only have 1 rarity
        uInput = input("Enter a Rarity (Common, Uncommon, Rare, Mythic): ")
        query += "rarity=" + uInput + "+"
    print()  
    # Prompt user for legality
    prompt = input("Search by Format Legality? Y/N: ")
    if prompt == 'y' or prompt == 'Y': 
        uInput = input("Enter Formats (Vintage, Legacy, Modern, Pioneer, etc.): ")
        uInput = uInput.replace(" ", "+legal=")
        query += "legal=" + uInput
    else: 
        # Only search for paper cards by default
        query += "legal=vintage"
    print()
    
    return query

def list_search():
    """
    Prompt user for some parameters and output a list of all cards matching search criteria
    """
    print()
    print("--------------------List Search--------------------")
    query = list_prompts()
    cardList = scryfall(query)
    # Error checking
    if cardList["object"] == "error":
        print("Search returned no matches.")
        print()
    else:
        # If parameters were valid, output all card names in list
        count = 1
        loop = True
        total = cardList["total_cards"]
        print("Your search returned ", total, "cards!")
        
        while loop:
            if count == 1: 
                print("--------------------List Search Results--------------------")
            # Scryfall API returns cards in 175 length chunks
            if cardList["has_more"] == True and (count % 175) == 0:
                response = requests.get(cardList["next_page"])
                cardList = response.json()
            elif cardList["has_more"] == False:
                loop = False
            # Output current chunk    
            for card in cardList["data"]:
                print(count, ") ", card["name"])
                if count % 25 == 0 or count == total:
                    cont = list_menu()
                    match cont:
                        case 2:
                            card_search()
                        case 3:
                            print()
                            loop = False
                            break
                    print("--------------------List Search Results--------------------")
                count += 1
    
def game():
    """
    Deduction game. A card is generated at random and the user is asked to name the generated card.
    Feedback is given on incorrect responses. A score is tallied and saved to a text file on completion.
    """
    playing = True
    score = 0
    while playing:
        print()
        print("--------------------Deduction Game--------------------")
        print("Selecting random card ....")
        mCard = scryfall("/named?fuzzy=" + microservice())
        guess = 0
        guessList = []
        correct = False
        # Player gets 20 guesses
        while guess < 20 and not correct:
            # Print all previous guesses, if any
            if len(guessList) != 0:
                print("--------------------Deduction Game--------------------")
                print("Previous Guesses: ")
                print("Name — CMC — Color(s) — Rarity — Supertype(s) — Subtype(s)")
                for i in range(len(guessList)):
                    print(guessList[i])
                    if (i + 1) % 2 == 0:
                        print()
            print("Guess: ", guess + 1,"/ 20")
            pCard = guess_input()
            guessList.append(guess_attrs(guess, pCard))
            
            # Game ends when player guesses correctly or guess limit is reached
            correct, clues = guess_check(pCard, mCard)
            guessList.append(clues)
            
            if not correct:
                guess += 1
                
        score += 20 - guess
        
        if correct:
            print()
            print("WINNER!!! You guessed correctly! Your current score is: ", score)
            uInput = input("Would you like to keep playing? (Y/N): ")
            print()
            playing = True if uInput == 'y' or uInput == 'Y' else False  
        else:
            print()
            print("You lost! Better luck next time! Your final score is: ", score)
            print()
            playing = False
    # Check if player beat high score, and record new high score if so      
    record(score)

def guess_attrs(guess, card):
    """
    Condense card attributes into a string

    Args:
        guess (int): Guess number
        card (string): JSON card object

    Returns:
        string: String of card attributes
    """
    cSuper, cSub = simplify_types(card)
    supT = ""
    for type in cSuper:
        supT += type + " "
    subT = ""
    for type in cSub:
        subT += type + " " 
    if subT =="":
        subT = "No subtype" 
           
    colorID = color_str(card["color_identity"])
    
    return (str(guess + 1) + ") " + card["name"] + " — " + str(int(card["cmc"])) + " — " 
    + colorID + " — " + card["rarity"] + " — " + supT + "— " + subT)
    
def guess_input():
    """
    Collect and verify input from user
    Returns:
        string: JSON string containing relevant card information
    """
    valid = False
    while not valid:
        uInput = input("Enter a valid card name: ")
        print()
        query = '/named?fuzzy=' + uInput.replace(' ','+')
        card = scryfall(query) 
        if card["object"] != "error":
            valid = True
        else: 
            print("Invalid input. Try again.")
            print()
            
    return card

def guess_check(pCard, mCard):
    """
    Run a series of comparisons between given cards

    Args:
        pCard (string): JSON card object
        mCard (string): JSON card object

    Returns:
        bool: True if guess is correct, False otherwise
        string: Clues for the given card
    """
    print("You guessed: ")
    print_card(pCard)
    print()
    input("Enter any key to continue: ")
    print()
    """
    Do check here: if "object" != "error" [...] else [...]
    """
    clues = ""
    # Check if user guessed correctly
    print("Your guess is .... ", end="")
    if compare_name(pCard, mCard):
        print("Correct!")
        return True, clues        
    else:
        clues += "Incorrect!"
        print("Incorrect!")
        print()
    # Otherwise run comparisons to provide feedback
    print("Converted Mana Cost is .... ", end="")
    tempStr = compare_cmc(pCard, mCard)
    clues += " — " + tempStr
    print(tempStr)

    print("Color Identity is .... ", end="")
    tempStr = compare_color(pCard, mCard)
    clues += " — " + tempStr
    print(tempStr)

    print("Rarity is .... ", end="")
    tempStr = compare_rarity(pCard, mCard)
    clues += " — " + tempStr
    print(tempStr)
    
    mSuper, mSub = simplify_types(mCard)
    pSuper, pSub = simplify_types(pCard)
    
    print("SuperType is .... ", end="")
    tempStr = compare_types(pSuper, mSuper)
    clues += " — " + tempStr
    print(tempStr)
    
    print("SubType is .... ", end="")
    tempStr = compare_types(pSub, mSub)
    clues += " — " + tempStr
    print(tempStr)
    
    print()
    input("Enter any key to continue: ")
    print()
    
    return False, clues

def compare_rarity(pCard, mCard):
    """
    Run a comparison of card rarities between given cards

    Args:
        pCard (string): JSON card object
        mCard (string): JSON card object

    Returns:
        string: String describing result of comparison
    """
    # Do direct comparison first
    if pCard["rarity"] == mCard["rarity"]:
        return "Correct!"
    # If rarity is not correct, give a player some clue. Rarity cannot be a partial match.
    rarities = ["common", "uncommon", "rare", "mythic"]
    for i in range(len(rarities)):
        if pCard["rarity"] == rarities[i]:
            pCount = i
    
    for i in range(len(rarities)):
        if mCard["rarity"] == rarities[i]:
            mCount = i

    if pCount < mCount:
        return "Incorrect! It is a higher rarity." 
    
    return "Incorrect! It is a lower rarity."

def color_str(list):
    """
    Converts elements of a list into a single string

    Args:
        list (list): List of any length containing any types

    Returns:
        string: String consisting of list elements 
    """
    cString = ""
    for color in list:
        cString += color  
    if cString == "":
        cString = "Colorless"
    return cString
 
def compare_color(pCard, mCard):
    """
    Run a comparison of color identities between given cards

    Args:
        pCard (string): JSON card object
        mCard (string): JSON card object

    Returns:
        string: String describing result of comparison
    """
    pColors = pCard["color_identity"]
    mColors = mCard["color_identity"]

    pString = color_str(pColors)
    mString = color_str(mColors)    
    
    if pString == mString:
        return "Correct!"
    
    for pID in pString:
        for mID in mString:
            if pID == mID:
                return "Partial Match!"
    
    return "Incorrect!"

def compare_cmc(pCard, mCard):
    """
    Run a comparison of converted mana costs between given cards

    Args:
        pCard (string): JSON card object
        mCard (string): JSON card object

    Returns:
        string: String describing result of comparison
    """
    if pCard["cmc"] == mCard["cmc"]:
        return "Correct!"
    
    if abs(pCard["cmc"] - mCard["cmc"]) <= 2:
        return "Close! You are +/- 2 off the correct cmc."
    
    return "Incorrect!"

def compare_name(pCard, mCard):
    """
    Compare the names of the given cards

    Args:
        pCard (string): JSON card object
        mCard (string): JSON card object

    Returns:
        bool: True if match, false otherwise 
    """
    # Account for dfc, split cards, transforming cards, etc.
    if pCard["layout"] == "normal":
        pName = pCard["name"]
    else:
        pName = pCard["card_faces"][0]["name"]
        
    if mCard["layout"] == "normal":
        mName = mCard["name"]
    else:
        mName = mCard["card_faces"][0]["name"]   
    
    if pName == mName:
        return True
    else: 
        return False
    
def compare_types(pType, mType):
    """
    Run a comparison of card types between given lists

    Args:
        pType (list): List of types in some card
        m_type (list): List of types in some card

    Returns:
        string: String describing result of comparison
    """
    # Check if lists are empty
    if len(pType) == 0 and len(mType) != 0:
        return "Incorrect!"
    if len(pType) != 0 and len(mType) == 0:
        return "Incorrect!"
    
    if pType == mType:
        return "Correct!"
    else:    
        matches = 0
        for x in pType:
            for z in mType:
                if x == z:
                    matches += 1
        if matches > 0:
            return "Partial Match!"
        else:
            return "Incorrect!"
        
def simplify_types(card):
    """
    Break down the typeline of given card into supertypes and subtypes

    Args:
        card (string): JSON object

    Returns:
        tuple: Tuple containing types as two lists
    """
    if card["layout"] == "normal":
        types = card["type_line"].split()
    else:
        types = card["card_faces"][0]["type_line"].split()
    # Find where supertype ends and subtype begins 
    cutoff = 0
    for word in types:
        cutoff += 1
        if word == "—":
            break
    
    # Assign super and sub types to their own lists 
    super = []
    for i in range(cutoff):
        if types[i] != "—":
            super.append(types[i])
    sub = []
    if cutoff < len(types):
        for i in range(cutoff, len(types)):
            sub.append(types[i])
    return (super, sub)

def microservice():
    """
    Call Microservice to generate a random card for deduction game

    Returns:
        string: Name of the generated card
    """
    # Call microservice
    file = open("transfer.txt","r+")
    file.truncate(0)
    file.seek(0)
    file.write('run')
    file.close() 
       
    time.sleep(1)
    # Open file after small delay to collect card from microservice
    file = open("transfer.txt","r+")
    card = file.read()
    card = json.loads(card)
    file.close()

    return card["name"]
    
def main_menu():
    """
    Program's main menu from which all major functions are called
    """
    loop = True
    while loop:
        title = text2art("MTG  Terminal  Tool")
        choices = [
            "1) Card Search ",
            "2) List Search", 
            "3) Deduction Game",
            "4) High Score",
            "5) Exit"
            ]
        descriptions = [
            "Output the card text/properties of any given Magic: The Gathering card.\n",
            "Generate a list of all cards that match given search parameters.\n",
            "Game where user attempts to name a randomly selected Magic: The Gathering card.\n(Requires extensive knowledge of MTG)\n",
            "View Current High Score.\n",
            "Close the Program.\n"
        ]
        print(title)
        for i in range(len(choices)):
            print(choices[i])
            print(descriptions[i])
            
        uInput = input("Enter a number: ")
        match uInput:
            case '1':
                card_search()
            case '2':
                list_search()
            case '3':
                game()
            case '4':
                print_score()
            case '5':
                loop = False             
            case _:
                print("Invalid input. Try again.")
                print()

if __name__ == '__main__':
    main_menu()
