# :gift: Secret Santa Twilio Python Program :santa:

## Description
Last year I wrote some python code to allow me to create a secret santa system for my family which would send messages to each person 
so even I wouldn't know who everyone had... This year I decided to one up last year and build a fully usable GUI for others to try!
This program is designed for couples in family buying joint gifts for other couples. I'll be creating an individual program shortly as well

## Getting Started
### Dependencies
* Python
* PyQt5
* Twilio

## Installing PyQt5
* [PyQt5 Tutorial](https://pypi.org/project/PyQt5/)

## Twilio
Twilio is a fantastic programmable communications provider, I highly suggest you check them out!
To run this application successfully you will need an account with Twilio that is not a trial account (can't send messages to unverified numbers without paid account)
Steps to setup twilio correctly to run this application:

1. Head to [Twilio Sign-up Page](https://www.twilio.com/try-twilio) and create a free account
2. Log in to your Twilio account
3. Under Phone Numbers on the sidebar, click Regulatory Compliance, then select Bundles
4. Create a bundle and wait for verification
5. Search for messaging services and click 'Create Messaging Service'. Go through the steps to set this up (add phone number if you have one)
6. Make sure you add the regulatory bundle to the messaging service!
7. Search for messaging services and write down your messaging service sid
8. Navigate to Auth Tokens & API keys, note down your Account SID and Auth Token (these will only be stored locally when running the program for security reasons)


### Couple vs Individual
* I've now made two seperate python programs! One for Secret santa as couples and one for individuals, hopefully at somepoint in the future I can merge these together as seperate tabs of the same application!


### Running the python file
* Download zip and extract to folder
* open christmas.py in vscode or respective IDE
* Press run

OR
* Download zip and extract to folder
* Open a terminal in respective folder
* run 'python christmas.py' 

## How to use
### Testing mode
* Testing mode means you don't need to input any twilio information and you can see how the program would run if you did have an active twilio account
* Add the event organiser name so you can get sweet juicy credit in the message!
* Then, add couples detail information such as 'Damon, '+61487234556' and press add couple
* Once you have at least two or three couples, hit send secret santa message.
* If you're testing, a dialogue prompt will alert the user, showing them how the messages would've been sent
* If you're working, the console will output as it is sending messages and a dialogue box will pop up to notify the user when all messages are successfully sent. If any fail the for loop aborts so make sure all the phone numbers are correct!

### Working mode
* Same as above, except pressing ```send secret santa message``` will yield a warning if no twilio information is given
* If twilio information is given, the program will likely succeed unless a twilio error occurs, which is printed to the screen

## Importing Objects from CSV file
* NEW: importing people/couples from CSV: I really like this feature, it allows you to select a CSV which automatically inserts all the objects to the list. Ensure the CSV file is as following:
* Couples: first_name | first_number | second_name | second_number
* Individuals: name | number

## Additional Notes
* Make sure your Twilio phone service is working before using the app, this can be done very easily on the Twilio website
* When entering phone numbers, make sure the format is '+61 XXX XXX XXX' where 61 is your area code (no apostrophes needed)
* Ensure you enter enough couples for the program to actually work, the algorithm works by making selectable people then removing them so the more the merrier!

### Building an executable
* An executable can be made with Pyinstall by first running pip install pyinstaller then running ```pyinstaller.exe --onefile --windowed christmas_individual.py``` or ```pyinstaller.exe --onefile --windowed christmas_couple.py``` 
* If you run this executable, the font will not copy across, I have no idea why

## Built With
* Python
* Twilio
* PyQt5

## Contact Me!
If you have any feedback or questions, feel free to contact me [here](mailto:damon.oneil2@hotmail.com)
