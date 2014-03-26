''' File Info
Author: Cameron Varley
Date: March 21, 2014
Filename: Game.py
Description: Text based war game using python
Version: 1.1.0
versions since relese: 3
'''

import os
import sys
import time
import random

money = 500
troops = 1
extra_troops = 0
enemy_troops = 0
buy_troops = 0
battles_won = 0
total_battles = 0
discount = 0
token = 0
powerups = [0, 0] # Nuke($1250), Laser($650)
version = "1.1.0"

# Custom Game Functions
def wait_clear(mode, n='', mode1=''):
	if mode == "wait":
		time.sleep(n)
		if mode1 == "clear":
			wait_clear("clear")
	elif mode == "clear":	
		os.system('cls')
		os.system('clear')

# Changelog
def changelog():
	print ("Changes since 1.0.5\n")
	print ("1. Added the Powerup store")
	print ("2. Powerups are now fully functional")
	print ("For a full changleog siince the start goto:\nhttps://github.com/Camvar97/Text-Wars\n")
		
# Intro Sequence
def intro():
	print ("Text Wars\nversion:", version, "\n\n")
	changelog()
	print ("Welcome to the text wars arena")
	print ("Please enter your name: ", end="")
	name = input()
	wait_clear("clear")
	print ("Welcome Commander", name)
	print ("let's get started with how the game works\n\n")
	print ("You will be given $500 to start")
	print ("You can fight, purchase, or retire if you want.")
	print ("When you lose your last man the game ends\n")
	print ("Please wait 10s for the game to load")
	wait_clear("wait", n=10, mode1="clear")
	play_b4()
	
# Plyed B4
def play_b4():
	global money
	global troops
	global extra_troops
	global enemy_troops
	global buy_troops
	global battles_won
	global total_battles
	global discount
	global token
	
	print ("Do you know how to play? (yes/no): ", end="")
	playb4 = input()
	if playb4.lower() == "yes" or playb4.lower() == "y":
		# make sure all values are set to defualt
		money = 500
		troops = 1
		extra_troops = 0
		enemy_troops = 0
		buy_troops = 0
		battles_won = 0
		total_battles = 0
		discount = 0
		token = 0	
		wait_clear("clear")
		menu(2)
	elif playb4.lower() == "no" or playb4.lower() == "n":
		wait_clear("clear")
		training()
	else:
		print ("Invalid Response")
		wait_clear("wait", n=2, mode1='clear')
		play_b4()

# Training sequence
def training():
	print ("OK let's start you off with the menu")
	wait_clear("wait", n=2, mode1='clear')
	menu(1)

# Menu Sequence
def menu(mode):
	if mode == 1:
		info(mode)
		print ("Welcome to the training menu.\nYou will always revert to this menu anytime you finish a task!\n")
		print ("Training Menu")
		print ("---------------------------------")
		print ("1. Store (You can purchase stuff here)\n2. Battle (Fight a random enemy)\n3. Scout (Search the area. Fight or Loot)\n4. Gamble (Use your tokens here!)\n5. Retire (This is where you can end your game)")
	elif mode == 2:
		info(mode)
		print ("Main Menu")
		print ("---------------------------------")
		print ("1. Store\n2. Battle\n3. Scout\n4. Gamble\n5. Retire")
	print ("Choose an item: ", end="")
	m_location = input()
	if m_location == '1':
		wait_clear("clear")
		store(mode)
	elif m_location == '2':
		wait_clear("clear")
		battle(mode)
	elif m_location == '3':
		wait_clear("clear")
		scout(mode)
	elif m_location == '4':
		wait_clear("clear")
		gamble(mode)
	elif m_location == '5':
		wait_clear("clear")
		retire(mode)
	else:
		print ("Invalid Response")
		wait_clear("wait", n=2, mode1="clear")
		menu(mode)
		
# Store
def store(mode):
	
	global troops
	global money
	global discount
	global buy_troops
	global token
	
	info(mode)
	if mode == 1:
		print ("Welcome to the store")
		print ("This is where you can purchase troops, powerups, and tokens\n")
		print ("Training Store")
		print ("---------------------------------")
		print ("1. Buy Troops\n2. Buy Powerup\n3. Buy Tokens\n4. Main Menu")
	elif mode == 2:
		print ("Store")
		print ("---------------------------------")
		print ("1. Buy Troops\n2. Buy Powerup\n3. Buy Tokens\n4. Main Menu")
	print ("Choose an item: ", end="")
	m_location = input()
	if m_location == '1': # Troops
		wait_clear("clear")
		info(mode)
		if discount > 0:
			print ("Troops: $50/militant\n")
		else:
			print ("Troops: $100/militant\n")
		print ("How many would you like to buy: ", end="")
		buy = int(input())
		buy_troops = buy
		if discount >= 1:
				if buy_troops > discount:
					print ("You don't have enough discounts for that")
					wait_clear("wait", n=2, mode1='clear')
					store(mode)
				else:
					troops += buy
					money -= buy*50
					discount -= buy
					print ("Remaining discounts: ", discount)
					print ("New amount of troops: ", troops)
					print ("New balance: ", money)
					wait_clear("wait", n=2, mode1='clear')
					transport()
					buy_troops = 0
					store(mode)
		else:
			troops += buy
			money -= buy*100
			print ("New amount of troops: ", troops)
			print ("New balance: ", money)
			wait_clear("wait", n=2, mode1='clear')
			transport()
			buy_troops = 0
			store(mode)
	elif m_location == '2': # Powerups
		wait_clear("clear")
		info(mode)
		print ("Nuke: $1250")
		print ("Laser: $650\n")
		print ("what would you like? (nuke/laser): ", end="")
		option = input()
		if option.lower() == "nuke":
			print ("How many nukes: ", end="")
			buy = int(input())
			if buy > 0:
				powerups[0] += 1
				money -= buy*1250
				store(mode)
			else:
				print ("Invalid Response")
				store(mode)
		elif option.lower() == "laser":
			print ("How many lasers: ", end="")
			buy = int(input())
			if buy > 0:
				powerups[0] += 1
				money -= buy*650
				store(mode)
			else:
				print ("Invalid Response")
				store(mode)
		else:
			print ("Invalid Response")
			store(mode)
		wait_clear("wait", n=2, mode1="clear")
		store(mode)
	elif m_location == '3': # Tokens
		wait_clear("clear")
		info(mode)
		print ("Tokens: $10\n")
		print ("How many would you like to buy: ", end="")
		buy = int(input())
		money_ispos = money - buy * 10
		if money > 0 and money_ispos > 0:
			token += buy
			money -= buy*10
			print ("New amount of tokens: ", token)
			print ("New balance: ", money)
			wait_clear("wait", n=2, mode1='clear')
			store(mode)
		else:
			print ("We don't support gambling addictions")
			wait_clear("wait", n=2, mode1='clear')
			store(mode)
	elif m_location == '4': # Main Menu
		menu(mode)
	else:
		print ("Invalid Response")
		wait_clear("wait", n=2, mode1="clear")
		store(mode)

# Battle
def battle(mode):
	
	global troops
	global total_battles
	global battles_won
	global money
	global enemy_troops
	
	if mode == 1:
		info(mode)
		print ("Welcome to battle training\n")
		print ("This page will be where you fight.")
		print ("Every battle is random, you could win and you could loose.")
		print ("Every time you loose, you will loose a troop.")
		print ("Every time you win, you will get $10 for every enemy soldier.")
	elif mode == 2:
		info(mode)
		print ("Welcome to the battle Commander!")
		print ("Lets Fight!")
	enemy()
	if powerups[0] > 0 or powerups[1] > 0:
		print ("You have powerup(s)!\n")
		print ("Nukes: ", powerups[0])
		print ("lasers: ", powerups[1], "\n")
		print ("They have: ", enemy_troops, " troops")
		power_use = input("Would you like to use a powerup: (yes/no)")
		if power_use.lower() == "yes" or power_use.lower() == "y":
			power = input("Which one: (nuke/laser)")
			if power.lower() == "nuke":
				print ("You used a nuke!")
				money += enemy_troops*50
				loot()
				enemy_troops -= enemy_troops
				wait_clear("wait", n=2, mode1="clear")
				powerups[0] -= 1
				menu(mode)
			elif power.lower() == "laser":
				print ("You used a laser!")
				money += enemy_troops*50
				loot()
				enemy_troops -= 5
				wait_clear("wait", n=2)
				powerups[1] -= 1
	for i in range(5, 0, -1):
		print (i)
		wait_clear("wait", n=0.75)
	print ("They have: ", enemy_troops, " troops")
	if enemy_troops == troops * 2:
		print ("Sir, they attacked before we had the chance.")
		print ("We lost a HALF of our soldiers")
		troops = troops // 2
		print ("we now have: ", troops, " troops.")
		wait_clear("wait", n=7, mode1="clear")
		transport()
		menu(mode)
	elif enemy_troops > troops and enemy_troops >= 1:
		print ("Sir, they attacked before we had the chance.")
		print ("We lost a member of our family today")
		troops = troops - 1
		print ("we now have: ", troops, " troops.")
		total_battles = total_battles + 1
		wait_clear("wait", n=7, mode1="clear")
		transport()
		menu(mode)
	elif enemy_troops < troops and enemy_troops >= 1:
		print ("We've done well today soldiers")
		print ("we earned: ", enemy_troops*10)
		print ("New balance: ", money+enemy_troops*10)
		loot()
		money = money + enemy_troops*10
		battles_won = battles_won+1
		total_battles = total_battles + 1
		wait_clear("wait", n=7, mode1="clear")
		menu(mode)
	elif enemy_troops == 0:
		print ("Commander they've disapeared!")
		print ("We couldn't attack")
		total_battles = total_battles + 1
		wait_clear("wait", n=7, mode1="clear")
		menu(mode)
	else:
		print ("It was a tie")
		print ("auto re-roll")
		total_battles = total_battles + 1
		wait_clear("wait", n=7, mode1="clear")
		menu(mode)
	
# Scout
def scout(mode):
	scout = random.randint(1,10)
	if scout == 1 or scout == 3 or scout == 5:
		print ("You encountered an enemy!")
		wait_clear("wait", n=1)
		print ("Starting fight sequence")
		wait_clear("wait", n=1)
		battle(mode)
	elif scout == 8 or scout == 4 or scout == 6:
		loot()
		wait_clear("wait", n=2)
		menu(mode)
	else:
		print ("Nothing to report")
		wait_clear("wait", n=2)
		menu(mode)
	
# Gamble
def gamble(mode):
	global token
	global money
	global troops
	global discount
	global extra_troops
	
	if money <= 0:
		print ("Come back when you have money to lose")
		wait_clear("wait", n=2)
		menu(mode)
	if mode == 1:
		print ("Training Casino\n")
	elif mode == 2:
		print ("Casino\n")
	if token > 0:
		loot = random.randint(1, 10)
		if loot == 1:
			money += 100
			print ("You've won $100")
		elif loot == 2:
			money -= 100
			print ("You've lost $100")
		elif loot == 3:
			money += 200
			print ("You've won $200")
		elif loot == 4:
			money -= 200
			print ("You've lost $200")
		elif loot == 5:
			token += 1
			print ("You've won an extra token")
		elif loot == 7:
			token += 2
			print ("You've won two extra tokens")
		elif loot == 9:
			extra_troops += 2
			print ("You've won two extra troops")
		else:
			print ("You've recieved... nothing!")
		wait_clear("wait", n=4)
		token = token - 1
		menu(mode)
	else:
		print ("You cannot use the casino right now")
		wait_clear("wait", n=4)
		menu(mode)
	
# Retire
def retire(mode):
	if mode == 1:
		play_b4()
	elif mode == 2:
		print ("Thanks For playing")
		wait_clear("wait", n=2)
		sys.exit()
	
# Current stats
def info(mode):
	
	global token
	global battles_won
	global money
	
	wait_clear("clear")
	
	print ("Troops: ", troops)
	if troops < 10:
		transport()
	print ("Extra Troops: ", extra_troops)
	print ("Money: ", money)
	print ("Discount Cards: ", discount)
	print ("Casino Tokens: ", token)
	if battles_won % 5 == 0 and battles_won > 0:
		token = token + 1
		print ("Your $200 paycheck has arrived")
		money = money + 200
		wait_clear("wait", n=5)
		battles_won = 0
		tax()
		menu(mode)
	if total_battles % 5 == 0 and total_battles > 0:
		tax()
		menu(mode)
	print ("\n")

# Enemy Generation
def enemy():
	
	global enemy_troops
	
	enemy_troops = random.randint(1,11)
	retreat = random.randint(1,5)
	if retreat == 1:
		enemy_troops = 0
	else:
		enemy_troops = enemy_troops

# Loot Generator
def loot():
	global money
	global troops
	global discount
	global extra_troops
	
	loot = random.randint(1, 10)
	if loot == 1:
		money += 100
		print ("You've found $100 in loot")
	elif loot == 3:
		money += 200
		print ("You've found $200 in loot")
	elif loot == 5:
		discount += 1
		print ("You've found a discount card")
	elif loot == 7:
		discount += 2
		print ("You've found two discount cards")
	elif loot == 9:
		extra_troops += 2
		print ("You've taken 2 hostage for your own troops")
		transport()
	else:
		print ("You didn't find any loot")
		
# Troop Transfer
def transport():
	
	global troops
	global extra_troops
	
	if troops < 10 and extra_troops > 0:
		troops = troops + 1
		extra_troops = extra_troops - 1
		wait_clear("wait", n=0.06)
		print ("Transfering troops to front lines")
		wait_clear("wait", n=0.06, mode1="clear")
		menu(2)
	elif troops >= 11:
		dif = buy_troops - 10
		extra_troops = extra_troops + dif
		troops = troops - dif
		while troops >= 11:
			troops = troops - 1
			extra_troops = extra_troops + 1
		print ("Transfering troops to barracks")
		wait_clear("wait", n=2)
	if troops < 0:
		troops = 0

# Tax
def tax():
	global money
	global total_battles
	
	print ("You were taxed 13%")
	wait_clear ("wait", n=2)
	tax = 13 * money / 100.0
	if money > 0:
		money = money - tax
	else:
		money = money + tax
	total_battles = 0

intro() 