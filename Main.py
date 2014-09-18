''' File Info
Author: Cameron Varley
Date: March 21, 2014
Filename: Game.py
Description: Text based war game using python
Version: 1.4.0
versions since relese: 9
'''

import os
import sys
import time
import random
import pickle

money = 500
troops = 1
extra_troops = 0
enemy_troops = 0
buy_troops = 0
battles_won = 0
total_battles = 0
discount = 0
token = 0
HP = 50
points = 0
powerups = [0, 0] # Nuke($1250), Laser($650)
version = "1.4.5"
hasloaded = 0

def savegame(filename):
	global money
	global troops
	global extra_troops
	global discount
	global token
	global HP
	global powerups
	global battles_won
	global total_battles
	
	with open(filename, 'wb') as f:
		pickle.dump([money, troops, extra_troops, discount, token, HP, powerups, battles_won, total_battles], f)

def loadgame(filename):
	global money
	global troops
	global extra_troops
	global discount
	global token
	global HP
	global powerups
	global battles_won
	global total_battles
	
	with open(filename, 'rb') as f:
		money, troops, extra_troops, discount, token, HP, powerups, battles_won, total_battles = pickle.load(f)
    
# Custom Game Functions
def wait_clear(mode, n='', mode1=''):
	if mode == "wait":
		time.sleep(n)
		if mode1 == "clear":
			wait_clear("clear")
	elif mode == "clear":	
		os.system('cls' if os.name == 'nt' else 'clear')

# Changelog
def changelog():
	print ("Changes since 1.4.0\n")
	print ("1. Added base structure for points.")
	print ("For a full changleog since the start goto: https://github.com/Camvar97/Text-Wars")
	print ("To provide user feedback email: Cam.avarley@gmail.com with the subject TextWars\n")
		
# Intro Sequence
def intro():
	wait_clear("wait", n=1, mode1="clear")
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
	print ("When you reach 0 HP the game ends\n")
	cont = input("Press enter to continue")
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
	global powerups
	global HP
	
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
		powerups = [0, 0]
		HP = 50
		points = 0
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
	global hasloaded
	
	transport(mode)
	if mode == 1:
		info(mode)
		print ("Welcome to the training menu.\nYou will always revert to this menu anytime you finish a task!\n")
		print ("Training Menu")
		print ("---------------------------------")
		print ("1. Store (You can purchase stuff here)\n2. Battle (Fight a random enemy)\n3. Scout (Search the area. Fight or Loot)\n4. Gamble (Use your tokens here!)\n5. Hospital (15 HP for $225)\n6. Retire (This is where you can end your game)\n7. Save/Load game")
	elif mode == 2:
		info(mode)
		print ("Main Menu")
		print ("---------------------------------")
		print ("1. Store\n2. Battle\n3. Scout\n4. Gamble\n5. Hospital\n6. Retire\n7. Save/Load game")
	print ("Choose an item: ", end="")
	m_location = input()
	if m_location == '1':
		wait_clear("clear")
		store(mode)
	elif m_location == '2':
		if troops == 0:
			print ("Are you trying to kill yourself? (Yes/No): ", end="")
			yn = input()
			if yn.lower() == "yes":
				wait_clear("clear")
				battle(mode)
			elif yn.lower() == "no":
				print ("Good we thought you were insane!")
				wait_clear("wait", n=2, mode1="clear")
				menu(mode)
			else:
				print ("Invalid response")
				wait_clear("wait", n=2, mode1="clear")
				menu(mode)
		else:
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
		hospital(mode)
	elif m_location == '6':
		wait_clear("clear")
		retire(mode)
	elif m_location == '7':
		print ("Would you like to save your game or load a previous game?")
		sl = str(input("(save/load): "))
		if sl.lower() == "save":
			filename = str(input("Filename: "))
			savegame(filename)
			menu(mode)
		elif sl.lower() == "load":
			if hasloaded == 0:
				try:
					filename = str(input("Filename: "))
					loadgame(filename)
					hasloaded = 1
					menu(mode)
				except:
					print ("Invalid filename")
					wait_clear("wait", n=2, mode1="clear")
					menu(mode)
			elif hasloaded == 1:
				print ("You've already loaded a game")
				wait_clear("wait", n=2, mode1="clear")
				menu(mode)
	elif m_location == 'wwssadadba':
		wait_clear("clear")
		debug(mode)
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
	global HP
	
	info(mode)
	if mode == 1:
		print ("Welcome to the store")
		print ("This is where you can purchase troops, powerups, and tokens\n")
		print ("Training Store")
		print ("---------------------------------")
		print ("1. Buy Troops\n2. Buy Powerup\n3. Buy Tokens\n4. Buy Items\n5. Main Menu")
	elif mode == 2:
		print ("Store")
		print ("---------------------------------")
		print ("1. Buy Troops\n2. Buy Powerup\n3. Buy Tokens\n4. Buy Items\n5. Main Menu")
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
		try:
			buy = int(input())
			buy_troops = buy
		except:
			print ("An error with your input occured!")
			wait_clear("wait", n=2, mode1="clear")
			store(mode)
		if buy_troops < 0:
			print ("NO! How dare you try that!")
			wait_clear("wait", n=2, mode1="clear")
			store(mode)
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
					transport(mode)
					buy_troops = 0
					store(mode)
		else:
			money_isnull = money - buy*100
			if money_isnull <= -100000:
				print ("We're sorry but we can't provide you with the resources.")
				wait_clear("wait", n=3, mode1="clear")
				menu(mode)
			elif money <= -100000:
				print ("I'm sorry but we can't give you a loan at this time.")
				wait_clear("wait", n=3, mode1="clear")
				menu(mode)
			else:
				troops += buy
				money -= buy*100
				print ("New amount of troops: ", troops)
				print ("New balance: ", money)
				wait_clear("wait", n=2, mode1='clear')
				transport(mode)
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
			try:
				buy = int(input())
			except:
				print ("An error with your input occured!")
				wait_clear("wait", n=2, mode1="clear")
				store(mode)
			if buy < 0:
				print ("NO! How dare you try that!")
				wait_clear("wait", n=2, mode1="clear")
				store(mode)
			if buy > 0:
				powerups[0] += 1
				money -= buy*1250
				store(mode)
			else:
				print ("Invalid Response")
				store(mode)
		elif option.lower() == "laser":
			print ("How many lasers: ", end="")
			try:
				buy = int(input())
			except:
				print ("An error with your input occured!")
				wait_clear("wait", n=2, mode1="clear")
				store(mode)
			if buy < 0:
				print ("NO! How dare you try that!")
				wait_clear("wait", n=2, mode1="clear")
				store(mode)
			if buy > 0:
				powerups[1] += 1
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
		try:
			buy = int(input())
			money_ispos = money - buy * 10
		except:
			print ("An error with your input occured!")
			wait_clear("wait", n=2, mode1="clear")
			store(mode)
		if buy < 0:
			print ("NO! How dare you try that!")
			wait_clear("wait", n=2, mode1="clear")
			store(mode)
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
	elif m_location == '4': # Item Store
		info(mode)
		print ("Item Store\n")
		print ("Items")
		print ("1. First Aid kit\n")
		print ("Please enter the number for the item you would like to buy: ", end="")
		item_loc = input()
		if item_loc == "":
			store(mode)
		item_loc = int(item_loc)
		if item_loc == 1:
			print ("You choose the first aid kit.")
			print ("They are $75 for 5 HP")
			print ("How many would you like to buy: ", end="")
			try:
				buy = int(input())
				money_ispos = money - buy * 10
			except:
				print ("An error with your input occured!")
				wait_clear("wait", n=2, mode1="clear")
				store(mode)
			if buy < 0:
				print ("NO! How dare you try that!")
				wait_clear("wait", n=2, mode1="clear")
				store(mode)
			if money > 0 and money_ispos > 0:
				HP += buy*5
				money -= buy*75
				print ("\nNew amount of HP: ",HP)
				print ("New balance: ", money)
				wait_clear("wait", n=2, mode1='clear')
				store(mode)
			else:
				print ("We don't support credit card")
				wait_clear("wait", n=2, mode1='clear')
				store(mode)
		else:
			store(mode)
	elif m_location == '5': # Main Menu
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
	global HP
	
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
				if powerups[0] > 0:
					print ("You used a nuke!")
					money += enemy_troops*50
					loot()
					enemy_troops -= enemy_troops
					wait_clear("wait", n=2, mode1="clear")
					powerups[0] -= 1
					menu(mode)
				else:
					print ("You don't have a nuke")
			elif power.lower() == "laser":
				if powerups[1] > 0:
					print ("You used a laser!")
					money += enemy_troops*50
					loot()
					enemy_troops -= 5
					wait_clear("wait", n=2)
					powerups[1] -= 1
				else:
					print ("You don't have a laser")
	for i in range(5, 0, -1):
		print ("\r", i, end="")
		wait_clear("wait", n=0.75)
	print ("\nThey have: ", enemy_troops, " troops")
	if troops == 0:
		print ("Are you ok? (Yes/No): ", end="")
		ask = input()
		if ask.lower() == "yes":
			print ("OK good!")
			print ("Just to let you know you lost 10HP")
			HP -= 10
			wait_clear("wait", n=3, mode1="clear")
			menu(mode)
		if ask.lower() == "no":
			print ("Well thats what you get!")
			print ("Just to let you know you lost 10HP")
			HP -= 10
			wait_clear("wait", n=3, mode1="clear")
			menu(mode)
	elif enemy_troops == troops * 2:
		print ("Sir, they attacked before we had the chance.")
		print ("We lost a HALF of our soldiers")
		troops //= 2
		HP -= 3
		print ("we now have: ", troops, " troops.")
		print ("HP: ", HP)
		wait_clear("wait", n=7, mode1="clear")
		transport(mode)
		menu(mode)
	elif enemy_troops > troops and enemy_troops >= 1:
		print ("Sir, they attacked before we had the chance.")
		print ("We lost a member of our family today")
		HP -= 1
		troops -= 1
		print ("we now have: ", troops, " troops.")
		print ("HP: ", HP)
		total_battles += 1
		wait_clear("wait", n=7, mode1="clear")
		transport(mode)
		menu(mode)
	elif enemy_troops < troops and enemy_troops >= 1:
		print ("We've done well today soldiers")
		print ("we earned: ", enemy_troops*10)
		print ("New balance: ", money+enemy_troops*10)
		loot()
		money += enemy_troops*10
		battles_won += 1
		total_battles += 1
		wait_clear("wait", n=7, mode1="clear")
		menu(mode)
	elif enemy_troops == 0:
		print ("Commander they've disapeared!")
		print ("We couldn't attack")
		total_battles += 1
		wait_clear("wait", n=7, mode1="clear")
		menu(mode)
	else:
		print ("It was a tie")
		print ("auto re-roll")
		total_battles += 1
		wait_clear("wait", n=7, mode1="clear")
		battle(mode)
	
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

# Checker
def check(mode):
	global token
	global battles_won
	global money
	
	rounded = round(money,2)
	money = rounded
	
	if troops < 10:
		transport(mode)
		
	if battles_won % 5 == 0 and battles_won > 0:
		token += 1
		print ("Your $200 paycheck has arrived")
		money += 200
		wait_clear("wait", n=5)
		battles_won = 0
		tax()
		menu(mode)
		
	if total_battles % 5 == 0 and total_battles > 0:
		tax()
		menu(mode)
		
	if HP <= 0:
		retire(mode)
	
# Current stats
def info(mode):
	global token
	global battles_won
	global money
	
	wait_clear("clear")
	
	check(mode)
	
	print ("-----------------------------------------")
	print ("| Troops:         ", str(troops).rjust(20), "|")
	print ("| Extra Troops:   ", str(extra_troops).rjust(20), "|")
	print ("| Money:          ", str(money).rjust(20), "|")
	print ("| Discount Cards: ", str(discount).rjust(20), "|")
	print ("| Casino Tokens:  ", str(token).rjust(20), "|")
	print ("| HP:             ", str(HP).rjust(20), "|")
	print ("| Nukes:          ", str(powerups[0]).rjust(20), "|")
	print ("| Lasers:         ", str(powerups[1]).rjust(20), "|")
	print ("| Points:         ", str(points).rjust(20), "|")
	print ("-----------------------------------------\n")

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
	global points
	
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
		wait_clear("wait", n=2)
		transport(mode)
	else:
		print ("You didn't find any loot")
		
# Troop Transfer
def transport(mode):
	
	global troops
	global extra_troops
	
	if troops < 10 and extra_troops > 0:
		troops += 1
		extra_troops -= 1
		wait_clear("wait", n=0.06)
		print ("Transfering troops to front lines")
		wait_clear("wait", n=0.06, mode1="clear")
		menu(mode)
	elif troops >= 11:
		dif = buy_troops - 10
		extra_troops += dif
		troops -= dif
		while troops >= 11:
			troops -= 1
			extra_troops += 1
		print ("Transfering troops to barracks")
		wait_clear("wait", n=2)
		menu(mode)
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
		money -= tax
	else:
		money += tax
	total_battles = 0

# Hospital
def hospital(mode):
	global HP
	global money
	
	info(mode)
	
	print ("Hospital\n")
	print ("Treatment: $225 for 15HP\n")
	print ("How many treatment would you like to take: ", end="")
	buy = input()
	if buy == "":
		menu(mode)
	try:
		buy = int(buy)
	except:
		print ("An error with your input occured!")
		wait_clear("wait", n=2, mode1="clear")
		menu(mode)
	money_ispos = money - buy*225
	if buy < 0:
		print ("NO! How dare you try that!")
		wait_clear("wait", n=2, mode1="clear")
		store(mode)
	if money > 0 and money_ispos > 0:
		HP += buy*15
		money -= buy*225
		print ("New amount of HP: ", HP)
		print ("New balance: ", money)
		wait_clear("wait", n=2, mode1='clear')
		menu(mode)
	else:
		print ("We don't support credit cards")
		wait_clear("wait", n=2, mode1='clear')
		menu(mode)

# Debug mode
def debug(mode):
	global money
	global troops
	global extra_troops
	global discount
	global token
	global HP
	global powerups
	global battles_won
	global total_battles
	
	wait_clear("clear")
	
	info(mode)
	
	print ("Debug\n")
	print ("1. Change money\n2. Change troops\n3. Change extra troops\n4. Change number of discount cards\n5. Change number of tokens\n6. Change current HP\n7. Change power-ups\n8. Change battles one\n9. Change total number of battle played\n10. Save Game\n11. Load Game\nEnter or 12: Main menu\n")
	print ("Please make a selection: ", end="")
	m_location = input()
	if m_location == "":
		menu(mode)
	m_location = int(m_location)
	if m_location == 1:
		print ("Please enter the new money balance: ", end="")
		try:
			add = float(input())
		except:
			debug(mode)
		money = add
		debug(mode)
	elif m_location == 2:
		print ("Please enter the new amount of troops: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		troops = add
		debug(mode)
	elif m_location == 3:
		print ("Please enter the new amounts of extra troops: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		extra_troops = add
		debug(mode)
	elif m_location == 4:
		print ("Please enter the new amount of discount cards: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		discount = add
		debug(mode)
	elif m_location == 5:
		print ("Please enter the new amount of tokens: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		token = add
		debug(mode)
	elif m_location == 6:
		print ("Please enter your new HP: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		HP = add
		debug(mode)
	elif m_location == 7:
		print ("Nuke or Laser: ", end="")
		m_location = input()
		if m_location.lower() == "nuke":
			print ("Please enter a new amount of nukes: ", end="")
			try:
				add = int(input())
			except:
				debug(mode)
			powerups[0] = add
			debug(mode)
		if m_location.lower() == "laser":
			print ("Please enter a new amount of lasers: ", end="")
			try:
				add = int(input())
			except:
				debug(mode)
			powerups[1] = add
			debug(mode)
		else:
			debug(mode)
	elif m_location == 8:
		print ("Please enter the battles that you want to win: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		battles_won = add
		debug(mode)
	elif m_location == 9:
		print ("Please enter how many total battles you want: ", end="")
		try:
			add = int(input())
		except:
			debug(mode)
		total_battles = add
		debug(mode)
	elif m_location == 10:
		savegame('debug')
		debug(mode)
	elif m_location == 11:
		loadgame('debug')
		debug(mode)
	elif m_location == 12:
		menu(mode)
	else:
		print ("Error")
		wait_clear("wait", n=2, mode1="clear")
		debug(mode)		

print ("Starting Game")
for i in range(50+1):
	time.sleep(0.1)
	print ("\r", ("*"*i)+('-'*(50-i)), end="")
print ("\n")
intro()
