''' File Info
Author: Cameron Varley
Date: 2020-02-07 13:10:03
Filename: textwars.py
Description: Text based war game using python, rewrite of my original textwars.
version: 2.2.1
'''

import time
import os
import pickle
import math
import random
import sys
import pymenu as pm
import pystore as ps


class user():
    def __init__(self, username='', playedBefore=False, money=500, troops=[1, 0], battlesWon=0, totalBattles=0, token=0, hp=50, powerups=[0, 0]):
        self.username = username
        self.playedBefore = playedBefore
        self.money = money
        self.troops = troops
        self.battlesWon = battlesWon
        self.totalBattles = totalBattles
        self.token = token
        self.hp = hp
        self.powerups = powerups


# Game Variables
version = '2.2.1'
player = user()

# initialize the menus
storeItems = ps.store('store')

mainMenu = pm.menu('Main')
storeMenu = mainMenu.newSubMenu('Store', 'mainMenu')
debugMenu = mainMenu.newSubMenu('Debug', 'mainMenu')

# Create Menu Items
mainMenu.populate([storeMenu, 'battle', 'scout', 'gamble',
                   'hospital', 'retire', 'save', debugMenu])

for i in vars(user()).keys():
    debugMenu.newItems(i)


def initialize():
    global storeItems
    with open('store.config', 'rb') as store_config:
        storeItems = pickle.load(store_config)
        for i in storeItems.categories:
            storeMenu.newItems(i)


def validate(msg, type_, min=None, max=None, cost=None, allowEmpty=False):
    ''' 
    Input validation script, can check type, input range, and funds verification 
    '''
    while True:
        userInput = input(msg)
        try:
            # first check if user didnt enter anything, if so then return an exit notice
            if allowEmpty and not userInput:
                return
            # try and verify the input value against the type_ provided
            userInput = type_(userInput)
            # Check if the min and max are set
            if max and min:
                # when user enters a value between allowed range return else error
                if userInput <= max and userInput >= min:
                    return type_(userInput)
                raise ValueError()
            # if only max is set ensure proper entry (same for min)
            elif max and userInput > max:
                raise ValueError()
            elif min and userInput < min:
                raise ValueError()
            # if cost is set then we will check if the user has enough funds to do it before continuing
            if cost and not validate_cost(int(cost*userInput)):
                continue
        except ValueError:
            print('Your input was not valid')
            continue
        else:
            # Return value if all else fails
            return type_(userInput)


def validate_bool(msg, options, exit='0'):
    '''
    a function that is designed to return a True or False
    takes a msg, [true, false]
    '''
    while True:
        userInput = input('{}({}/{}) '.format(msg, options[0], options[1]))
        if userInput == exit or len(userInput) == exit:
            return
        if userInput.lower() in options:
            return True if userInput.lower() == options[0] else False
        print('Please enter a valid option')


def validate_cost(cost):
    ''' 
    a simple script that will just check if the user has enough funds for the required item 
    '''
    global player
    if cost > player.money:
        print("Insufficient Funds!")
        return False
    player.money -= cost
    return True


def save(load=False):
    ''' 
    this will pickle the uservalues into a savefile for loading later 
    '''
    global player
    if load:
        with open(player.username, 'rb') as f:
            ask = validate_bool('Reset your old game? ', ['y', 'n'])
            player = player if ask else pickle.load(f)
    with open(player.username, 'wb') as f:
        pickle.dump(player, f)


def wait_clear(wait=False, clear=False, length=0):
    ''' 
    allows to clear or wait based on what is needed
    future option is to just ask user to press enter to continue or wait the aloted time...
    this may require to do a interupt with multithreading the python script 
    '''
    if wait:
        time.sleep(length)
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')


def main():
    ''' 
    Main script to begin the game 
    '''
    global player
    wait_clear(clear=True)
    print('TextWars V{}'.format(version))
    print()
    print('Lets get started with a few questions!')
    player.username = validate('What is your name? ', str)
    # if the user enters no here we will enable hints
    player.playedBefore = validate_bool(
        'Have you played before? ', ['y', 'n'])
    if player.playedBefore:
        try:
            # Check if file can be loaded
            save(True)
        except:
            # create save if the users save couldnt be found
            print('Old save not found')
            player.playedBefore = False
    print('Saving')
    save()
    menu()


def menu():
    '''
    A function that will display any menu in the game and will allow for ease of navigation
    '''
    toDisplay = mainMenu
    while True:
        info()
        toDisplay.display()
        prompt = validate('Enter an option: ', int, 1,
                          len(toDisplay.items), allowEmpty=True)
        if not prompt and toDisplay.parent:
            # if the user input is empty and parent isnt blank we will send them to the parent menu
            toDisplay = globals()[toDisplay.parent]
        elif not prompt:
            # if input empty but no parent then we will display the same menu
            toDisplay = toDisplay
        else:
            # user enetered someting so we will go here and store the location and key in a list
            value = list(toDisplay.items.values())[int(prompt)-1]
            key = list(toDisplay.items.keys())[int(prompt)-1]
            if isinstance(key, pm.menu):
                # if the inputed location is a menu we will display that menu
                location = '{}Menu'.format(
                    value)
                toDisplay = globals()[location]
            elif toDisplay.name.lower() == 'store':
                # if we are in the store then go to the purchase menu for inputed category
                purchase(value)
            elif toDisplay.name.lower() == 'debug':
                # similar to store but we go to the debug menu
                debug(value)
            else:
                try:
                    # if the item entered is not a menu then it must be a function se we call it
                    globals()[value]()
                except:
                    pass


def transport():
    ''' 
    function that makes sure the troops are in the right place
    we ensure that there is always 10 troops available when
    there is some in reserve 
    '''
    global player
    if player.troops[0] < 10 and player.troops[1] > 0:
        print('Calling in the reserves')
        while player.troops[1] > 0:
            player.troops[0] += 1
            player.troops[1] -= 1
    if player.troops[0] > 10:
        print('Sending to reserves')
        while player.troops[0] > 10:
            player.troops[0] -= 1
            player.troops[1] += 1


def info():
    ''' 
    print all the user statistics 
    '''
    wait_clear(clear=True)
    check()
    transport()
    print(str('-')*20)
    print("Troops/Extra:   {}/{}".format(player.troops[0],
                                         player.troops[1]))
    print("Money:          {}".format(player.money))
    print("Casino Tokens:  {}".format(player.token))
    print("HP:             {}".format(player.hp))
    print("Nukes/Lasers:   {}/{}".format(player.powerups[0],
                                         player.powerups[1]))
    print(str('-')*20)
    print()


def check():
    ''' 
    bonus if you have reached a certain number of battle 
    '''
    global player
    if player.hp <= 0:
        retire()
    if player.battlesWon % 5 == 0 and player.battlesWon > 0:
        player.token += 1
        player.money += 200
        player.battlesWon = 0
        print('Your paycheck has arrived')
        wait_clear(True, length=2)
    if player.totalBattles % 5 == 0 and player.totalBattles > 0:
        tax()
        player.totalBattles = 0


def tax():
    ''' 
    a function which will tax the user a certain amount of money 
    '''
    global player
    print('Paying your troops 13%')
    tax = 13 * player.money / 100
    if player.money > 0:
        player.money -= tax
    else:
        player.money += tax


def purchase(category):
    '''
    a function that will display the items available for the given category
    '''
    global player
    wait_clear(clear=True)
    storeItems.display(category)
    items = list(storeItems.items[category].keys())
    costs = list(storeItems.items[category].values())
    prompt = validate('What item Do you want to buy: (1-{}) '.format(len(items)),
                      int, 0, len(items), allowEmpty=True)
    if prompt:
        amount = validate('How many {} do you want to buy: '.format(items[prompt-1]),
                          int, 0, cost=costs[prompt-1][0], allowEmpty=True)
        if not amount:
            pass
        elif items[prompt-1] == 'nuke':
            player.powerups[0] += amount
        elif items[prompt-1] == 'laser':
            player.powerups[1] += amount
        elif type(getattr(player, costs[prompt-1][1])) == list:
            getattr(player, costs[prompt-1][1])[0] += amount
        else:
            currentVal = getattr(player, costs[prompt-1][1])
            setattr(player, costs[prompt-1][1], currentVal+amount)
    return


def debug(value):
    ''' 
    allows me to change any value from in the game 
    '''
    global player
    currentVal = getattr(player, value)
    wait_clear(clear=True)
    print('Current Value: {}'.format(currentVal))
    if isinstance(currentVal, list):
        for n, i in enumerate(currentVal):
            newValue = validate('Change item {} ({}) to: '.format(
                n+1, i), type(currentVal[n]), allowEmpty=True)
            getattr(player, value)[
                n] = currentVal[n] if not newValue else newValue
        return
    else:
        newValue = validate('Change {} to: '.format(
            value), type(currentVal), allowEmpty=True)
    if not newValue:
        return
    else:
        setattr(player, value, newValue)


def battle():
    global player
    info()
    print('Welcome to the battlefield')
    enemyTroops = enemy_Gen()
    if enemyTroops == 'Flee' or enemyTroops == 0:
        print('There are no enemy troops left')
        wait_clear(True, length=2)
        return
    print('Enemy Troops: {}'.format(enemyTroops))
    if any(i > 0 for i in list(player.powerups)):
        prompt = validate_bool('Would you like to use a powerup? ', ['y', 'n'])
        if prompt and player.powerups[0] > 0:
            nuke = validate_bool('Use Nuke: ', ['y', 'n'])
            player.powerups[0] -= 1 if nuke else 0
        elif prompt and player.powerups[1] > 0:
            laser = validate_bool('Use Laser: ', ['y', 'n'])
            player.powerups[1] -= 1 if laser else 0
        player.money = enemyTroops*50 if nuke else 5*50
        enemyTroops = 0 if nuke else enemyTroops-5
        loot()
    if enemyTroops == math.ceil(player.troops[0] * 1.5):
        print('Sir, they attacked before we had the chance.')
        print('We lost a HALF of our soldiers.')
        player.troops[0] //= 2
        player.hp -= 3
        wait_clear(True, length=2)
    elif enemyTroops > player.troops[0]:
        print('Sir, they attacked before we had the chance.')
        print('We lost a member of our family today')
        player.troops[0] -= 1
        player.hp -= 1
        wait_clear(True, length=2)
    elif enemyTroops < player.troops[0]:
        print('Sir, We have won the battle.')
        earn = enemyTroops*10
        print('We have earned ${}'.format(earn))
        player.money += earn
        player.battlesWon += 1
        loot()
        wait_clear(True, length=2)
    else:
        print('It was a tie')
        print('auto re-roll')
        wait_clear(True, length=2)
        battle()
    player.totalBattles += 1
    return


def scout():
    scout = random.randint(1, 10)
    if scout % 3 == 0:
        loot()
    elif scout % 4 == 0:
        print('You encountered an enemy!')
        wait_clear(True, length=1)
        print('Starting fight sequence')
        wait_clear(True, length=1)
        battle()
    else:
        print('Nothing to report')
    wait_clear(True, length=2)
    return


def gamble():
    global player
    if player.money == 0:
        print('Come back when you have money to loose')
        wait_clear(True, length=2)
        return
    if player.token > 0:
        lootnum = random.randint(1, 10)
        if not lootnum % 2:
            loot()
        elif lootnum == 1:
            print('You lost $100')
            player.money -= 100
        elif lootnum == 3:
            print('You lost $200')
            player.money -= 200
        else:
            print('Better luck nexk time')
        player.token -= 1
    else:
        print("You cannot use the casino right now")
    wait_clear(True, length=2)


def loot():
    global player
    loot = random.randint(1, 10)
    if loot == 1:
        player.money += 100
        print("You've found $100 in loot")
    elif loot == 3:
        player.money += 200
        print("You've found $200 in loot")
    elif loot == 5:
        player.token += 1
        print("You've found a token")
    elif loot == 7:
        player.token += 2
        print("You've found two tokens")
    elif loot == 9:
        player.troops[0] += 2
        print("You've gained new recruits")
    else:
        player.money += 5
        print("You got $5 as a consolation prize")


def hospital():
    global player
    cost = 225
    increase = 15
    info()
    print('Hospital')
    print('Treatment: ${} for {}HP per hour'.format(cost, increase))
    prompt = validate(
        'How long would you like to stay? (hr) ', int, 0, cost=cost, allowEmpty=True)
    if not prompt:
        return
    player.money -= prompt * cost
    player.hp += increase * prompt
    return


def enemy_Gen():
    ''' 
    generates a random number of enemies to fight 
    '''
    maxTroops = player.troops[0] * 1.35
    minTroops = player.troops[0] - (player.troops[0] * 0.35)
    fleeChance = random.randint(1, 100)
    numTroops = random.randint(math.floor(minTroops), math.ceil(maxTroops))
    if fleeChance <= 25 or numTroops == 0:
        numTroops = 'Flee'
    return numTroops


def retire():
    wait_clear(clear=True)
    print('Thanks for playing!')
    wait_clear(True, length=5)
    exit()


if __name__ == '__main__':
    initialize()
    main()
