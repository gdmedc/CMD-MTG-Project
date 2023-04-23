
from consolemenu import *
from consolemenu.items import *
import time
import requests
import json


def scryfall(params=None):
    url = "https://api.scryfall.com/cards"
    if params != None:
        url += params
    print(url)
    response = requests.get(url)

    if response:
        response.encoding = 'utf-8'
        response.text
        return response.json()
    else:
        raise Exception("There appears to be an issue with Scryfall. Please try again later.")
        response.encoding = 'utf-8'
        response.text
        card = response.json()
        print()
        print(card["details"])
        exit()

def high_score():
    print("This program function is currently WIP and serves only to demonstrate its final appearance.")
    print()
    print("High Scores")
    print("1) Jace Beleren 20 points")
    print("2) Nicol Bolas 18 points")
    print("3) The Raven Man 16 points")
    print("4) Urza 15 points")
    print("5) Ajani Pridemane 13 points")

    input("Press an key to return to main menu: ")

def print_card(card):
    print(card["name"], "\t", card["mana_cost"])
    print(card["type_line"])
    print(card["oracle_text"])

def card_search():
    u_input = input("Enter a card name: ")
    u_input = u_input.replace(' ','+')
    query = '/named?fuzzy='
    query += u_input

    print_card(scryfall(query))
    print()
    input("Press any key to return to main menu: ")

def list_menu():
    print()
    choices = ["1) View the next 25 results", "2) View Card Details", "3) Return to menu"]
    for choice in choices:
        print(choice)

    u_input = input("Enter a number: ")

    match u_input:
        case '1':
            u_input = 1
        case '2':
            u_input = 2
        case '3':
            u_input = 3
        case _:
            u_input = 0

    while (u_input < 1):
        print()
        print("Invalid input. Try again.")
        u_input = input("Enter a number: ")

        match u_input:
            case '1':
                u_input = 1
            case '2':
                u_input = 2
            case '3':
                u_input = 3
            case _:
                u_input = 0

    if u_input == 1:
        return 1
    elif u_input == 2:
        return 2
    elif u_input == 3:
        return 3

def list_search():
    print("This program function is currently WIP and has limited functionality. ")
    print("At present it is only possible to search by card type. ")
    print()

    u_input = input("Enter a card type: ")
    props = u_input.split()
    query = "/search?q="
    count = 1
    for prop in props:
        query += "t=" + prop
        if count < len(props):
            query += "+"
        count += 1

    card_list = scryfall(query)

    print("Currently, I am having issues parsing the list, but the data is being fetched correctly.  ")
    print("The JSON will be printed below shortly and the program will return to the main menu.")
    time.sleep(10)
    print(card_list)
    # count = 1
    # for card in card_list:
    #     print(count, ") ", card["name"])
    #     if count % 25:
    #         cont = list_menu()
    #         if cont == 2:
    #             card_search()
    #         elif cont == 3:
    #             break
    #     count += 1

def game():
    """
    Call microservice and store card name
    """
    print("This program function is currently WIP and serves only to demonstrate its final appearance.")
    print()
    score = 20
    u_input = input("Enter a valid card name: ")
    """
    Compare user input to card name (while loop)
    """
    guess_menu(u_input, score)
    print("WINNER!!! You guessed correctly!")
    cont = input("Would you like to keep playing? (y/n) ")

    if cont == 'y' or cont == 'Y':
        game()
def guess_menu(u_input, score):
    print("You guessed: ", u_input, " Your score is: ", score)
    print("Mana Value is ....", end="")
    time.sleep(1)
    print("Correct!")

    print("Color Identity is ....", end="")
    time.sleep(1)
    print("Partial Match!")

    print("Rarity is ....", end="")
    time.sleep(1)
    print("Incorrect!")

    print("Type is ....", end="")
    time.sleep(1)
    print("Incorrect!")

def main_menu():
    # main_men = ConsoleMenu("Placeholder title")
    choices = ["PLACEHOLDER TITLE", "1) Guessing Game", "2) Card Search", "3) List Search", "4) High Score", "5) Exit"]
    # selec_menu = SelectionMenu(choices)
    # main_men.show()
    # selec_menu.show()
    for choice in choices:
        print(choice)
    u_input = input("Enter a number: ")

    match u_input:
        case '1':
            u_input = 1
        case '2':
            u_input = 2
        case '3':
            u_input = 3
        case '4':
            u_input = 4
        case '5':
            u_input = 5
        case _:
            u_input = 0

    while (u_input < 1):
        print()
        print("Invalid input. Try again.")
        u_input = input("Enter a number: ")

        match u_input:
            case '1':
                u_input = 1
            case '2':
                u_input = 2
            case '3':
                u_input = 3
            case '4':
                u_input = 4
            case '5':
                u_input = 5
            case _:
                u_input = 0

    if u_input == 1:
        game()
    elif u_input == 2:
        card_search()
    elif u_input == 3:
        list_search()
    elif u_input == 4:
        high_score()
    elif u_input == 5:
        return False
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    playing = True
    while(playing):
        playing = main_menu()

