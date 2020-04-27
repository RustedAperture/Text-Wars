#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <ctime>
#include <cmath>
#include <limits>

#include "Include/tsl/ordered_map.h"
#include "menu.cpp"

#define VERSION 1

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::vector;

string username;
bool played_before = false;
float money = 500;
int troops[2] = {1, 0};
int battles_won = 0;
int total_battles = 0;
int tokens = 1;
int hp = 50;
int powerups[2] = {0, 0};

Menu main_menu;
Menu store_menu;
Menu *menu_to_show;
vector<Menu *> menu_pointers;

typedef void (*menu_method)(void);
tsl::ordered_map<string, menu_method> main_menu_items;

int get_int(int min, int max, string prompt)
{
    int ret_integer;
    string str_number;

    while (true)
    {
        cout << prompt << "(" << min << "-" << max << ") ";
        std::getline(cin, str_number);         //get string input
        std::stringstream convert(str_number); //turns the string into a stream

        //checks for complete conversion to integer and checks for minimum value
        if (convert >> ret_integer && !(convert >> str_number) && ret_integer >= min && ret_integer <= max)
            return ret_integer;

        cin.clear(); //just in case an error occurs with cin (eof(), etc)
        std::cerr << "Input must be between " << min << " and " << max << ". Please try again.\n";
    }
}

bool get_bool(string prompt)
{
    char response;
    cout << prompt << " (y/n) ";
    cin >> response;
    response = toupper(response);

    while (response != 'Y' && response != 'N')
    {
        cin.clear();
        cin.ignore(100, '\n');
        cout << "Please enter only Y or N: ";
        cin >> response;
        response = toupper(response);
    }

    if (response == 'Y')
    {
        return true;
    }
    return false;
}

void transport()
{
    if (troops[0] < 10 && troops[1] > 0)
    {
        cout << "Calling in the reserves" << endl;
        while (troops[1] > 0)
        {
            troops[0]++;
            troops[1]--;
        }
    }
    if (troops[0] > 10)
    {
        cout << "Sending to the reserves" << endl;
        while (troops[0] > 10)
        {
            troops[0]--;
            troops[1]++;
        }
    }
}

void stats()
{
    transport();
    system("CLS");
    cout << "--------------------" << endl;
    cout << "Username: " << username << endl;
    cout << "Troops/Extra: " << troops[0] << "/" << troops[1] << endl;
    cout << "Money: " << money << endl;
    cout << "Tokens: " << tokens << endl;
    cout << "HP: " << hp << endl;
    cout << "Nukes/Lasers: " << powerups[0] << "/" << powerups[1] << endl;
    cout << "--------------------" << endl;
    cout << endl;
}

void loot()
{
    srand(time(NULL));
    int win = rand() % 10 + 1;
    switch (win)
    {
    case 1:
        money += 100;
        cout << "You've found $100 in loot" << endl;
        break;
    case 3:
        money += 200;
        cout << "You've found $200 in loot" << endl;
        break;
    case 5:
        tokens += 1;
        cout << "You've found a token" << endl;
        break;
    case 7:
        tokens += 2;
        cout << "You've found two tokens" << endl;
        break;
    case 9:
        troops[0] += 2;
        cout << "You've gained new recruits" << endl;
        break;
    default:
        money += 5;
        cout << "You got $5 as a consolation prize" << endl;
        break;
    }
}

int enemygen()
{
    srand(time(NULL));
    float mintroops = troops[0] - (troops[0] * 0.35);
    float maxtroops = troops[0] * 1.35;
    int mod = (ceil(maxtroops) - floor(mintroops) + 1) + floor(mintroops);
    int enemies = rand() % mod;
    int flee_chance = rand() % 100 + 1;
    if (flee_chance <= 25 || enemies == 0)
    {
        return -5;
    }
    return enemies;
}

bool purchase(int amount, int price)
{
    if (amount * price <= money)
    {
        money -= price * amount;
        return true;
    }
    else
    {
        cout << "Not enough money!" << endl;
        system("PAUSE");
        return false;
    }
}

void store(int submenu)
{
    bool bought = false;

    while (!(bought))
    {
        stats();

        int amount;
        int item;
        int price;

        switch (submenu)
        {
        case 0:
            cout << "Troop Shop" << endl;
            cout << "--------------------" << endl;
            cout << "cost per troop: $50" << endl;
            price = 50;
            amount = get_int(0, money / price, "How many would you like to purchase: ");
            bought = purchase(amount, price);
            troops[0] += amount;
            break;
        case 1:
            cout << "Powerup Shop" << endl;
            cout << "--------------------" << endl;
            cout << "0. nuke: $1250" << endl;
            cout << "1. laser: $650" << endl;
            cout << "Which item would you like to purchase (0-1): ";
            cin >> item;
            price = item == 0 ? 1250 : 650;
            amount = get_int(0, money / price, "How many would you like to purchase: ");
            bought = purchase(amount, price);
            powerups[item] += amount;
            break;
        case 2:
            cout << "Token Shop" << endl;
            cout << "--------------------" << endl;
            cout << "cost per token: $10" << endl;
            price = 10;
            amount = get_int(0, money / price, "How many would you like to purchase: ");
            bought = purchase(amount, price);
            tokens += amount;
            break;
        case 3:
            cout << "Item Shop" << endl;
            cout << "--------------------" << endl;
            cout << "First Aid Kit: $50" << endl;
            price = 50;
            amount = get_int(0, money / price, "How many would you like to purchase: ");
            bought = purchase(amount, price);
            hp += amount * 10;
            break;
        case 4:
            menu_to_show = menu_pointers[0];
            break;
        }
    }
}

void battle()
{
    stats();

    int enemy_troops = enemygen();
    int earn = 0;

    if (enemy_troops == -5)
    {
        cout << "Enemy Fled" << endl;
        system("PAUSE");
        return;
    }
    if (powerups[0] > 0 || powerups[1] > 0)
    {
        bool prompt;
        bool nuke;
        bool laser;

        prompt = get_bool("Would you like to use a powerup?");
        if (prompt && powerups[0] > 0)
        {
            nuke = get_bool("Would you like to use a nuke?");
            if (nuke)
            {
                powerups[0]--;
                earn += enemy_troops * 50;
                enemy_troops = 0;
            }
        }
        else if (prompt && powerups[1] > 0)
        {
            laser = get_bool("Would you like to use a laser?");
            if (laser)
            {
                powerups[0]--;
                money += 5 * 50;
                enemy_troops -= 5;
            }
        }
    }
    cout << "Enemy Troops: " << enemy_troops << endl;
    if (enemy_troops == ceil(troops[0] * 1.5))
    {
        cout << "Sir, they attacked before we had the chance." << endl;
        cout << "We lost a HALF of our soldiers." << endl;
        troops[0] /= 2;
        hp -= 3;
        system("PAUSE");
    }
    else if (enemy_troops > troops[0])
    {
        cout << "Sir, they attacked before we had the chance." << endl;
        cout << "We lost a member of our family today" << endl;
        troops[0]--;
        hp--;
        system("PAUSE");
    }
    else if (enemy_troops < troops[0])
    {
        cout << "Sir, We have won the battle." << endl;
        earn += enemy_troops * 10;
        cout << "We have earned: $" << earn << endl;
        money += earn;
        battles_won++;
        cout << "Checking for extra rewards" << endl;
        loot();
        system("PAUSE");
    }
    else
    {
        cout << "It was a tie" << endl;
        cout << "Auto re-rolling" << endl;
        system("PAUSE");
        battle();
    }

    total_battles++;
    return;
}

void scout()
{
    srand(time(NULL));
    int scout = rand() % 10 + 1;
    if (scout % 3 == 0)
    {
        loot();
        system("PAUSE");
    }
    else if (scout % 4 == 0)
    {
        cout << "You entountered an enemy!" << endl;
        cout << "Engaging enemy" << endl;
        system("PAUSE");
        battle();
    }
    else
    {
        cout << "Nothing to report" << endl;
        system("PAUSE");
    }
}

void gamble()
{
    srand(time(NULL));
    int gamble = rand() % 10 + 1;
    if (money == 0)
    {
        cout << "Come back when you have money to loose!" << endl;
        system("PAUSE");
    }
    else if (tokens == 0)
    {
        cout << "You Dont have any tokens to gamble right now!" << endl;
        system("PAUSE");
    }
    else
    {
        if (tokens > 0 && gamble % 2 != 0)
        {
            loot();
        }
        else if (tokens > 0 && gamble == 1)
        {
            cout << "You Lost $100" << endl;
            money -= 100;
        }
        else if (tokens > 0 && gamble == 3)
        {
            cout << "You Lost $200" << endl;
            money -= 200;
        }
        else
        {
            cout << "Better luck next time" << endl;
        }
        system("PAUSE");
        tokens--;
    }
}

void hospital()
{
    int cost = 225;
    int heal = 15;
    int time;
    stats();
    cout << "Hospital" << endl;
    cout << "--------------------" << endl;
    cout << "The cost to visit is: $" << cost << "/hr" << endl;
    cout << "This will heal at a rate of: " << heal << endl;
    time = get_int(0, money / cost, "How long would you like to stay for: ");
    hp += heal * time;
}

void initialize()
{
    // Method to initialize the menu system
    menu_pointers.push_back(&main_menu);
    menu_pointers.push_back(&store_menu);

    store_menu = main_menu.new_sub_menu("Store", menu_pointers[0], menu_pointers[1]);

    main_menu_items.insert({"Store", &initialize});
    main_menu_items.insert({"Battle", &battle});
    main_menu_items.insert({"Scout", &scout});
    main_menu_items.insert({"Gamble", &gamble});
    main_menu_items.insert({"Hospital", &hospital});

    store_menu.item_names.push_back("Troops");
    store_menu.item_names.push_back("Powerup");
    store_menu.item_names.push_back("Token");
    store_menu.item_names.push_back("Items");
    store_menu.item_names.push_back("Main Menu");

    main_menu.add_items(main_menu_items);

    menu_to_show = menu_pointers[0];
}

int menu(Menu *menu)
{
    while (true)
    {
        stats();

        menu->display_menu();
        int choice = get_int(0, menu->item_names.size() - 1, "Enter an option: ");
        if (choice < menu->item_names.size() && choice >= 0)
        {
            if (menu->submenus.find(menu->item_names[choice]) != menu->submenus.end())
            {
                menu_to_show = menu->submenus.at(menu->item_names[choice])->self;
            }
            else
            {
                if (menu->name == "Store" && choice == menu->item_names.size() - 1)
                {
                    menu_to_show = menu->parent;
                }
                else if (menu->name == "Store")
                {
                    store(choice);
                }
                else
                {
                    (menu->item_methods[choice])();
                }
            }
        }
        return choice;
    }
}

int main()
{
    system("CLS");
    cout << "Text Wars V" << VERSION << endl;
    cout << endl;
    cout << "Lets start with a few questions!" << endl;
    cout << "What is your name: ";
    cin >> username;

    bool yes_no;
    yes_no = get_bool("Have you played before?");

    if (yes_no)
    {
        played_before = true;
    }
    else
    {
        played_before = false;
    }

    cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    initialize();

    int choice;

    while (true)
    {
        choice = menu(menu_to_show);
    }
}