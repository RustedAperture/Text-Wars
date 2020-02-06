''' File Info
Author: Cameron Varley
Date: 2020-02-06 13:51:58
Filename: textwars.py
Description: Text based war game using python, rewrite of my original textwars.
version: 2.0.2
'''

import time
import os
import pickle
import math
import random
import sys

# Game Variables
version = '2.0.2'
userValues = {'username': 'username',
              'playedBefore': False,
              'money': 500,
              'troops': [1, 0],
              'battlesWon': 0,
              'totalBattles': 0,
              'token': 0,
              'hp': 50,
              'points': 0,
              'powerups': [0, 0]}
# Hints bool will be used to toggle hints on or off when asked if played before
hints = False


# Input validation script, can check type, input range, and funds verification
def validate(msg, type_, min=None, max=None, cost=None, allowEmpty=False):
    while True:
        userInput = input(msg)
        try:
            # first check if user didnt enter anything, if so then return an exit notice
            if allowEmpty:
                if not userInput:
                    return 'exit'
            # try and verify the input value against the type_ provided
            userInput = type_(userInput)
            # Check if the min and max are set
            if max != None and min != None:
                # when user enters a value between allowed range return else error
                if userInput <= max and userInput >= min:
                    return type_(userInput)
                else:
                    raise ValueError()
            # if only max is set ensure proper entry (same for min)
            elif max != None:
                if userInput > max:
                    raise ValueError()
            elif min != None:
                if userInput < min:
                    raise ValueError()
            # if cost is set then we will check if the user has enough funds to do it before continuing
            if cost != None:
                if not validate_cost(int(cost*userInput)):
                    continue
        except ValueError:
            print('Your input was not valid')
            continue
        else:
            # Return value if all else fails
            return type_(userInput)


# a function that is designed to return a True or False
# takes a msg, [true, false]
def validate_bool(msg, options, exit='0'):
    while True:
        userInput = input('{}({}/{}) '.format(msg, options[0], options[1]))
        if userInput == exit or len(userInput) == int(exit):
            return exit
        if userInput.lower() in options:
            return True if userInput.lower() == options[0] else False
        else:
            print('Please enter a valid option')


# a simple script that will just check if the user has enough funds for the required item
def validate_cost(cost):
    global userValues
    if cost > userValues['money']:
        print("Insufficient Funds!")
        return False
    else:
        userValues['money'] -= cost
        return True


# this will pickle the uservalues into a savefile for loading later
def save_load(func, username):

    global userValues

    if func:
        with open(username, 'rb') as f:
            ask = validate_bool('Reset your old game? ', ['y', 'n'])
            userValues = userValues if ask else pickle.load(f)
    else:
        with open(username, 'wb') as f:
            pickle.dump(userValues, f)


# allows to clear or wait based on what is needed
# future option is to just ask user to press enter to continue or wait the aloted time...
# this may require to do a interupt with multithreading the python script
def wait_clear(wait=False, clear=False, length=0):
    if wait:
        time.sleep(length)
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')


# Main script to begin the game
def main():

    global userValues
    global hints

    wait_clear(clear=True)
    print('TextWars V{}'.format(version))
    print()
    print('Lets get started with a few questions!')
    userValues['username'] = validate('What is your name? ', str)
    # if the user enters no here we will enable hints
    userValues['playedBefore'] = validate_bool(
        'Have you played before? ', ['y', 'n'])
    hints = True if not userValues['playedBefore'] else False
    if userValues['playedBefore']:
        try:
            # Check if file can be loaded
            save_load(True, userValues['username'])
        except:
            # create save if the users save couldnt be found
            print('Old save not found')
            userValues['playedBefore'] = False
    print('Saving')
    save_load(False, userValues['username'])
    menu()


# menu funtion that will display the main menu,
# eventually i want to make this a function that will display
# any menu that is passed to it but will be dificult for a
# multimenu system
def menu():
    wait_clear(clear=True)
    info()
    menuItems = {'store': store,
                 'battle': battle,
                 'scout': scout,
                 'gamble': gamble,
                 'hospital': hospital,
                 'retire': retire,
                 'save': save_load}
    print('Menu')
    print('----------------------')
    counter = 1
    for key in menuItems:
        print('{}. {}'.format(counter, key.title()))
        counter += 1

    while True:
        action = validate('Enter a menu option: (1-7) ',
                          int, 1, 8, allowEmpty=True)
        try:
            if action == 'exit':
                menu()
            if action == 7:
                save_load(False, userValues['username'])
                menu()
            if action == 8:
                debug()
            # convert values to a list which index alues can be passed to,
            # this allows a function to be run from the dictionary based
            # on int input
            # list(dict.values())[index]()
            list(menuItems.values())[action-1]()
            break
        except:
            print('You should never see this!')


# function that makes sure the troops are in the right place
# we ensure that there is always 10 troops available when
# there is some in reserve
def transport():

    global userValues

    if userValues['troops'][0] < 10 and userValues['troops'][1] > 0:
        difference = 10 - userValues['troops'][0]
        userValues['troops'][0] += difference
        userValues['troops'][1] -= difference
        if userValues['troops'][1] < 0:
            userValues['troops'][0] += userValues['troops'][1]
        print('Calling in the reserve')
        wait_clear(True, length=2)
    elif userValues['troops'][0] >= 11:
        difference = userValues['troops'][0] - 10
        userValues['troops'][0] -= difference
        userValues['troops'][1] += difference
        print('Sending troops to the reserves')
        wait_clear(True, length=2)
    if userValues['troops'][0] < 0:
        userValues['troops'][0] = 0
    elif userValues['troops'][1] < 0:
        userValues['troops'][1] = 0


# print all the user statistics
def info():
    check()
    transport()
    print("----------------------")
    print("Troops/Extra:   {}/{}".format(userValues['troops'][0],
                                         userValues['troops'][1]))
    print("Money:          {}".format(userValues['money']))
    print("Casino Tokens:  {}".format(userValues['token']))
    print("HP:             {}".format(userValues['hp']))
    print("Nukes/Lasers:   {}/{}".format(userValues['powerups'][0],
                                         userValues['powerups'][1]))
    print("Points:         {}".format(userValues['points']))
    print("----------------------")
    print()


# bonus if you have reached a certain number of battle
def check():

    global userValues

    if userValues['battlesWon'] % 5 == 0 and userValues['battlesWon'] > 0:
        userValues['token'] += 1
        userValues['money'] += 200
        userValues['battlesWon'] = 0
        print('Your paycheck has arrived')
        wait_clear(True, length=2)
    if userValues['totalBattles'] % 5 == 0 and userValues['totalBattles'] > 0:
        tax()
        userValues['totalBattles'] = 0
    if userValues['hp'] <= 0:
        retire()


# we will take mney because taxes
def tax():

    global userValues

    print('Paying your troops 13%')
    tax = 13 * userValues['money'] / 100
    if userValues['money'] > 0:
        userValues['money'] -= tax
    else:
        userValues['money'] += tax


# this is the store funstion, I want to eventually make this significantly smaller
# the universal menu function will be best for this but i will need to find a way to
# tell items apart
def store():

    global userValues

    # List of items available in the store
    # These will eventually be catagorized and editable from the debug
    items = {'troops': 100,
             'nuke': 1250,
             'laser': 650,
             'tokens': 10,
             'first aid kits': 75}

    wait_clear(clear=True)

    print('Welcome to the store')
    storeMenu = ('Buy Troops', 'Buy Powerups',
                 'Buy Tokens', 'Buy Items', 'Exit')
    for i in range(len(storeMenu)):
        print('{}. {}'.format(i+1, storeMenu[i]))

    # allowing empty here will enable the user to just go back to the main menu
    prompt = validate('Enter a menu option: (1-5) ',
                      int, 1, 5, allowEmpty=True)

    wait_clear(clear=True)
    info()
    if prompt == 1:
        print('Troops: ${}/millitant'.format(items['troops']))
        prompt = validate('How many would you like to buy: ',
                          int, 0, cost=items['troops'], allowEmpty=True)
        if prompt == 'exit':
            store()
        userValues['troops'][0] += prompt
    elif prompt == 2:
        for i in range(0, 2):
            print('{}. {} - ${}'.format(i+1,
                                        list(items.keys())[i+1], list(items.values())[i+1]))
        prompt = validate_bool(
            'Which would you like to buy: ', ['1', '2'])
        if prompt == '0':
            store()
        powerup = 'nuke' if prompt else 'laser'
        cost = list(items.values())[1] if prompt else list(items.values())[2]
        amount = validate('How many {} would you like to buy: '.format(powerup),
                          int, 0, cost=cost, allowEmpty=True)
        if amount == 'exit':
            store()
        userValues['powerups'][int(prompt)-1] += amount
    elif prompt == 3:
        print('tokens: ${}'.format(items['tokens']))
        prompt = validate('How many would you like to buy: ',
                          int, 0, cost=items['tokens'], allowEmpty=True)
        if prompt == 'exit':
            store()
        userValues['token'] += prompt
    elif prompt == 4:
        for i in range(4, len(items)):
            print('{}. {} - ${}'.format(i-3,
                                        list(items.keys())[i], list(items.values())[i]))
        prompt = validate(
            'What would you like to buy: (1-{}) '.format(len(items)-4), int, 0, len(items))
        amount = validate('How many would you like to buy: ',
                          int, 0, cost=list(items.values())[prompt+3], allowEmpty=True)
        if prompt == 'exit':
            store()
        if prompt == 1:
            userValues['hp'] += 5*amount
    else:
        menu()
    store()


def train():

    global train

    print("Welcome to training mode, we will give you hints along the way")
    train = True


# allows me to change any value from in the game
def debug():

    global userValues

    wait_clear(clear=True)
    info()
    print('Debug Menu')
    print('----------------------')
    options = {'Change Troops': 'troops',
               'Change Reserve': 'troops',
               'Change Money': 'money',
               'Change Tokens': 'tokens',
               'Change HP': 'hp',
               'Change Power-Ups': 'powerups',
               'Change Battles Won': 'battlesWon',
               'Change Total Battles': 'totalBattles',
               'Save Game': 'save',
               'Load Game': 'load',
               'Main Menu': menu}
    for i in range(len(options)):
        print('{}. {}'.format(i+1, list(options.keys())[i]))
    print('----------------------')
    action = validate('What would you like to do? (1-{}) '.format(len(options)),
                      int, 0, len(options), allowEmpty=True)
    if action == 'exit':
        debug()
    if action > 0 and action <= 2:
        change = validate('Change this to: ', int)
        userValues[list(options.values())[action-1]][action-1] = change
        debug()
    if action > 2 and action < 9:
        change = validate('Change this to: ', int)
        userValues[list(options.values())[action-1]] = change
        debug()
    if action == 9:
        filename = validate('Enter username of save: ', str)
        save_load(False, filename)
        debug()
    if action == 10:
        filename = validate('Enter username of save: ', str)
        save_load(True, filename)
        debug()
    if action == 11:
        menu()


def battle():

    global userValues

    wait_clear(clear=True)
    info()
    print('Welcome to the battlefield')
    enemyTroops = enemy_Gen()
    if enemyTroops == 'Flee' or enemyTroops == 0:
        print('There are no enemy troops left')
        wait_clear(True, length=2)
        menu()
    print('Enemy Troops: {}'.format(enemyTroops))
    if any(i > 0 for i in list(userValues['powerups'])):
        prompt = validate_bool('Would you like to use a powerup? ', ['y', 'n'])
        if prompt and userValues['powerups'][0] > 0:
            nuke = validate_bool('Use Nuke: ', ['y', 'n'])
            userValues['powerups'][0] -= 1 if nuke else 0
            userValues['money'] = enemyTroops*50
            enemyTroops = 0
        elif prompt and userValues['powerups'][1] > 0:
            laser = validate_bool('Use Laser: ', ['y', 'n'])
            userValues['powerups'][1] -= 1 if laser else 0
            userValues['money'] = 5*50
            enemyTroops -= 5
        # if prompt:
        loot()
    if enemyTroops == 'flree' or enemyTroops == 0:
        print('There are no enemy troops left')
        wait_clear(True, length=2)
        menu()
    if userValues['troops'][0] == 0:
        print('What were you thinking attacking with no troops?')
        loss = random.randint(1, 10)
        userValues['hp'] -= loss
        print('minus {} health'.format(loss))
        wait_clear(True, length=2)
    elif enemyTroops == math.ceil(userValues['troops'][0] * 1.5):
        print('Sir, they attacked before we had the chance.')
        print('We lost a HALF of our soldiers.')
        userValues['troops'][0] //= 2
        userValues['hp'] -= 3
        wait_clear(True, length=2)
    elif enemyTroops > userValues['troops'][0]:
        print('Sir, they attacked before we had the chance.')
        print('We lost a member of our family today')
        userValues['troops'][0] -= 1
        userValues['hp'] -= 1
        userValues['totalBattles'] += 1
        wait_clear(True, length=2)
    elif enemyTroops < userValues['troops'][0]:
        print('Sir, We have won the battle.')
        earn = enemyTroops*10
        print('We have earned ${}'.format(earn))
        userValues['money'] += earn
        userValues['totalBattles'] += 1
        userValues['battlesWon'] += 1
        loot()
        wait_clear(True, length=2)
    else:
        print('It was a tie')
        print('auto re-roll')
        userValues['totalBattles'] += 1
        wait_clear(True, length=2)
        battle()
    menu()


def scout():
    scout = random.randint(1, 10)
    if scout % 3 == 0:
        loot()
        wait_clear(True, length=2)
        menu()
    elif scout % 4 == 0:
        print('You encountered an enemy!')
        wait_clear(True, length=1)
        print('Starting fight sequence')
        wait_clear(True, length=1)
        battle()
    else:
        print('Nothing to report')
        wait_clear(True, length=2)
        menu()


def gamble():

    global userValues

    if userValues['money'] == 0:
        print('Come back when you have money to loose')
        wait_clear(True, length=2)
        menu()

    if userValues['token'] > 0:
        loot = random.randint(1, 10)
        if loot == 1:
            userValues['money'] += 100
            print("You've won $100")
        elif loot == 2:
            userValues['money'] -= 100
            print("You've lost $100")
        elif loot == 3:
            userValues['money'] += 200
            print("You've won $200")
        elif loot == 4:
            userValues['money'] -= 200
            print("You've lost $200")
        elif loot == 5:
            userValues['money'] += 1
            print("You've won an extra token")
        elif loot == 7:
            userValues['money'] += 2
            print("You've won two extra tokens")
        elif loot == 9:
            userValues['troops'][0] += 2
            print("You've won two extra troops")
        else:
            print("You've recieved... nothing!")
        wait_clear(True, length=2)
        userValues['token'] -= 1
        menu()
    else:
        print("You cannot use the casino right now")
        wait_clear(True, length=2)
        menu()


def loot():

    global userValues

    loot = random.randint(1, 10)
    if loot == 1:
        userValues['money'] += 100
        print("You've found $100 in loot")
    elif loot == 3:
        userValues['money'] += 200
        print("You've found $200 in loot")
    elif loot == 5:
        userValues['token'] += 1
        print("You've found a token")
    elif loot == 7:
        userValues['token'] += 2
        print("You've found two tokens")
    elif loot == 9:
        userValues['troops'][0] += 2
        print("You've taken 2 hostage for your own troops")
    else:
        print("You didn't find any loot")
    wait_clear(True, length=2)


def hospital():
    wait_clear(clear=True)

    global userValues

    cost = 225
    increase = 15

    info()
    print('Hospital')
    print('Treatment: ${} for {}HP per hour'.format(cost, increase))
    prompt = validate(
        'How long would you like to stay? (hr) ', int, 0, cost=cost, allowEmpty=True)
    if prompt == 'exit':
        menu()
    userValues['money'] -= prompt * cost
    userValues['hp'] += increase * prompt
    menu()


# generates a random number of enemies to fight
def enemy_Gen():
    maxTroops = userValues['troops'][0] * 1.35
    minTroops = userValues['troops'][0] - (userValues['troops'][0] * 0.35)
    fleeChance = random.randint(1, 100)
    numTroops = random.randint(math.floor(minTroops), math.ceil(maxTroops))
    if fleeChance <= 25 or numTroops == 0:
        numTroops = 'Flee'
    return numTroops


def retire():
    wait_clear(clear=True)
    print('Thnaks for playing!')
    wait_clear(True, length=5)
    exit()


if __name__ == '__main__':
    main()
