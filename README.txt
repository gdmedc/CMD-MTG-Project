This is a student project created in 2023 and uploaded in 2025 for archival purposes. This project may no longer function properly due to API changes.

To run the project use 'python3 mtgProject.py' and optionally 'python3 partnerservice.py'. The primary purpose of this project is to allow users to interact with Scryfall.com through the command line/terminal to search for and view the properties of Magic: The Gathering cards. The project also features a guessing game where a card is selected at random for the user to deduce (partnerservice.py does not need to be run if the user does not intend to interact with this mode). I have no affiliation with Scryfall or Wizards of The Coast.

Required Python packages: 'requests', 'ijson'

This project reads from a text file containing a list of card dictionaries, which is not included to comply with Scryfall's API policies. To obtain this list visit https://scryfall.com/docs/api/bulk-data and then download the 'default cards' file as 'default-cards.json'.
