#include "menu.h"
#include "player.h"

#include <stdlib.h>

#include <cmath>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

#define VERSION 1.9

using namespace std;

bool debug = false;

Player player;

Menu main_menu("Main Menu");
Menu store_menu("Store Menu", &main_menu);
Menu debug_menu("Debug Menu", &main_menu);
Menu* menu_to_show;

void retire() {
    cout << "Thanks for playing." << endl;
    player.savePlayer();
    system("PAUSE");
    exit(3);
}

int get_int(int min, int max, string prompt) {
    int ret_integer;
    string str_number;

    while (true) {
        cout << prompt << " (" << min << "-" << max << ") " << flush;
        getline(cin, str_number);          // get string input
        stringstream convert(str_number);  // turns the string into a stream

        // checks for complete conversion to integer and checks for minimum value
        if (convert >> ret_integer && !(convert >> str_number) && ret_integer >= min &&
            ret_integer <= max)
            return ret_integer;

        cin.clear();
        cerr << "Input must be between " << min << " and " << max
             << ". Please try again.\n";
    }
}

bool get_bool(string prompt) {
    char response;
    cout << prompt << " (y/n) ";
    cin >> response;
    response = toupper(response);

    while (response != 'Y' && response != 'N') {
        cin.clear();
        cin.ignore(100, '\n');
        cout << "Please enter only Y or N: ";
        cin >> response;
        response = toupper(response);
    }

    if (response == 'Y') {
        return true;
    }
    return false;
}

void transport() {
    if (player.troops.active_duty < 10 && player.troops.reserve > 0) {
        cout << "Calling in the reserves" << endl;
        while (player.troops.reserve > 0) {
            player.troops.active_duty++;
            player.troops.reserve--;
        }
    }
    if (player.troops.active_duty > 10) {
        cout << "Sending to the reserves" << endl;
        while (player.troops.active_duty > 10) {
            player.troops.active_duty--;
            player.troops.reserve++;
        }
    }
}
void tax() {
    float tax = 13 * player.money / 100;
    if (tax == 0)
        tax = 100;
    if (player.money > 0 && player.troops.active_duty > 0) {
        cout << "Paying your troops 13%." << endl;
        system("PAUSE");
        player.money -= tax;
    } else if (player.money <= 0) {
        cout << "It's your lucky day!" << endl;
        system("PAUSE");
        player.money += tax;
    }
}

void check() {
    if (player.hp <= 0) {
        retire();
    }
    if (player.battles_won % 5 == 0 && player.battles_won > 0) {
        player.tokens++;
        player.money += 200;
        player.battles_won = 0;
        cout << "You have recieved a paycheck." << endl;
        system("PAUSE");
    }
    if (player.total_battles % 5 == 0 && player.total_battles > 0) {
        tax();
        player.total_battles = 0;
    }
}

void stats() {
    check();
    transport();
    system("CLS");
    cout << "----------------------" << endl;
    cout << fixed << "Username:      " << player.username << endl;
    cout << fixed << "Troops/Extra:  " << player.troops.active_duty << "/"
         << player.troops.reserve << endl;
    cout << setprecision(2) << fixed << "Money:         " << player.money << endl;
    cout << fixed << "Tokens:        " << player.tokens << endl;
    cout << fixed << "HP:            " << player.hp << endl;
    cout << fixed << "Nukes/Lasers:  " << player.powerups.nukes << "/"
         << player.powerups.lasers << endl;
    cout << "----------------------" << endl;
    if (debug) {
        cout << fixed << "Battles Won:   " << player.battles_won << endl;
        cout << fixed << "Total Battles: " << player.total_battles << endl;
        cout << "----------------------" << endl;
    }
    cout << endl;
}

void loot() {
    srand(time(NULL));
    int win = rand() % 10 + 1;
    switch (win) {
        case 1:
            player.money += 100;
            cout << "You've found $100 in loot" << endl;
            break;
        case 3:
            player.money += 200;
            cout << "You've found $200 in loot" << endl;
            break;
        case 5:
            player.tokens += 1;
            cout << "You've found a token" << endl;
            break;
        case 7:
            player.tokens += 2;
            cout << "You've found two tokens" << endl;
            break;
        case 9:
            player.troops.active_duty += 2;
            cout << "You've gained new recruits" << endl;
            break;
        default:
            player.money += 5;
            cout << "You got $5 as a consolation prize" << endl;
            break;
    }
}

int enemygen() {
    srand(time(NULL));
    float mintroops = player.troops.active_duty - (player.troops.active_duty * 0.35);
    float maxtroops = player.troops.active_duty * 1.35;
    if (maxtroops == 0)
        maxtroops = 5;
    int mod = (ceil(maxtroops) - floor(mintroops) + 1) + floor(mintroops);
    int enemies = rand() % mod;
    int flee_chance = rand() % 100 + 1;
    if (flee_chance <= 25 || enemies == 0) {
        return -5;
    }
    return enemies;
}

bool purchase(int amount, int price) {
    if (amount * price <= player.money) {
        player.money -= price * amount;
        return true;
    } else {
        cout << "Not enough player.money!" << endl;
        system("PAUSE");
        return false;
    }
}

void store(int submenu) {
    bool bought = false;

    while (!(bought)) {
        stats();

        int amount;
        int item;
        int price;

        switch (submenu) {
            case 0:
                cout << "Troop Shop" << endl;
                cout << "----------------------" << endl;
                cout << "cost per troop: $50" << endl;
                price = 50;
                amount = get_int(0, player.money / price,
                                 "How many would you like to purchase:");
                bought = purchase(amount, price);
                player.troops.active_duty += amount;
                break;
            case 1:
                cout << "Powerup Shop" << endl;
                cout << "----------------------" << endl;
                cout << "0. nuke: $1250" << endl;
                cout << "1. laser: $650" << endl;
                cout << "Which item would you like to purchase (0-1): ";
                cin >> item;
                price = item == 0 ? 1250 : 650;
                amount = get_int(0, player.money / price,
                                 "How many would you like to purchase:");
                bought = purchase(amount, price);
                if (item == 0) {
                    player.powerups.nukes += amount;
                } else {
                    player.powerups.lasers += amount;
                }
                break;
            case 2:
                cout << "Token Shop" << endl;
                cout << "----------------------" << endl;
                cout << "cost per token: $10" << endl;
                price = 10;
                amount = get_int(0, player.money / price,
                                 "How many would you like to purchase:");
                bought = purchase(amount, price);
                player.tokens += amount;
                break;
            case 3:
                cout << "Item Shop" << endl;
                cout << "----------------------" << endl;
                cout << "First Aid Kit: $50" << endl;
                price = 50;
                amount = get_int(0, player.money / price,
                                 "How many would you like to purchase:");
                bought = purchase(amount, price);
                player.hp += amount * 10;
                break;
        }
    }
}

void battle() {
    stats();

    int enemy_troops = enemygen();
    int earn = 0;

    if (enemy_troops == -5) {
        cout << "Enemy Fled" << endl;
        system("PAUSE");
        return;
    }
    cout << "Enemy Troops: " << enemy_troops << endl;
    if (player.powerups.nukes > 0 || player.powerups.lasers > 0) {
        bool prompt;
        bool nuke;
        bool laser;

        prompt = get_bool("Would you like to use a powerup?");
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (prompt && player.powerups.nukes > 0) {
            nuke = get_bool("Would you like to use a nuke?");
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            if (nuke) {
                player.powerups.nukes--;
                earn += enemy_troops * 50;
                enemy_troops = 0;
            }
        } else if (prompt && player.powerups.lasers > 0) {
            laser = get_bool("Would you like to use a laser?");
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            if (laser) {
                player.powerups.lasers--;
                player.money += 5 * 50;
                enemy_troops -= 5;
            }
        }
    }
    if (debug)
        cout << "Enemy Troops: " << enemy_troops << endl;
    if (player.troops.active_duty == 0)
        player.hp -= 10;
    if (enemy_troops == ceil(player.troops.active_duty * 1.5)) {
        cout << "Sir, they attacked before we had the chance." << endl;
        cout << "We lost a HALF of our soldiers." << endl;
        if (player.troops.active_duty != 0) {
            player.troops.active_duty /= 2;
            player.hp -= 3;
        }
        system("PAUSE");
    } else if (enemy_troops > player.troops.active_duty) {
        cout << "Sir, they attacked before we had the chance." << endl;
        cout << "We lost a member of our family today" << endl;
        if (player.troops.active_duty != 0) {
            player.troops.active_duty--;
            player.hp--;
        }
        system("PAUSE");
    } else if (enemy_troops < player.troops.active_duty && enemy_troops > 0) {
        cout << "Sir, We have won the battle." << endl;
        earn += enemy_troops * 10;
        cout << "We have earned: $" << earn << endl;
        player.money += earn;
        player.battles_won++;
        cout << "Checking for extra rewards" << endl;
        loot();
        system("PAUSE");
    } else if (enemy_troops <= 0) {
        cout << "Checking for extra rewards" << endl;
        loot();
        system("PAUSE");
    } else {
        cout << "It was a tie" << endl;
        cout << "Auto re-rolling" << endl;
        system("PAUSE");
        battle();
    }

    player.total_battles++;
    return;
}

void scout() {
    srand(time(NULL));
    int scout = rand() % 10 + 1;
    if (scout % 3 == 0) {
        loot();
        system("PAUSE");
    } else if (scout % 4 == 0) {
        cout << "You entountered an enemy!" << endl;
        cout << "Engaging enemy" << endl;
        system("PAUSE");
        battle();
    } else {
        cout << "Nothing to report" << endl;
        system("PAUSE");
    }
}

void gamble() {
    srand(time(NULL));
    int gamble = rand() % 10 + 1;
    if (player.money == 0) {
        cout << "Come back when you have money to loose!" << endl;
        system("PAUSE");
    } else if (player.tokens == 0) {
        cout << "You Dont have any tokens to gamble right now!" << endl;
        system("PAUSE");
    } else {
        if (player.tokens > 0 && gamble % 2 != 0) {
            loot();
        } else if (player.tokens > 0 && gamble == 1) {
            cout << "You Lost $100" << endl;
            player.money -= 100;
        } else if (player.tokens > 0 && gamble == 3) {
            cout << "You Lost $200" << endl;
            player.money -= 200;
        } else {
            cout << "Better luck next time" << endl;
        }
        system("PAUSE");
        player.tokens--;
    }
}

void hospital() {
    int cost = 225;
    int heal = 15;
    int time;
    stats();
    cout << "Hospital" << endl;
    cout << "----------------------" << endl;
    cout << "The cost to visit is: $" << cost << "/hr" << endl;
    cout << "This will heal at a rate of: " << heal << endl;
    time = get_int(0, player.money / cost, "How long would you like to stay for:");
    player.hp += heal * time;
    player.money -= cost * time;
}

void debugger(int var) {
    int int_max = std::numeric_limits<int>::max();
    cout << "----------------------" << endl;
    switch (var) {
        case 0:
            cout << fixed << "Current Username: " << player.username << endl;
            cout << "New Username: ";
            cin >> player.username;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            break;
        case 1:
            cout << fixed << "Current Balance: " << player.money << endl;
            player.money = get_int(0, int_max, "New Balance:");
            break;
        case 2:
            cout << fixed << "Current Troops: " << player.troops.active_duty << endl;
            cout << fixed << "Current Reservist: " << player.troops.reserve << endl;
            player.troops.active_duty =
                get_int(0, int_max, "New Troops (anything over 10 will go to reserves):");
            break;
        case 3:
            cout << fixed << "Current Battles Won: " << player.battles_won << endl;
            player.battles_won = get_int(0, int_max, "New Battles Won:");
            break;
        case 4:
            cout << fixed << "Current Number of battles: " << player.total_battles
                 << endl;
            player.total_battles = get_int(0, int_max, "New number of battles:");
            break;
        case 5:
            cout << fixed << "Current Tokesn: " << player.tokens << endl;
            player.tokens = get_int(0, int_max, "New Tokens:");
            break;
        case 6:
            cout << fixed << "Current HP: " << player.hp << endl;
            player.hp = get_int(0, int_max, "New HP:");
            break;
        case 7:
            cout << fixed << "Current Nukes: " << player.powerups.nukes << endl;
            cout << fixed << "Current Lasers: " << player.powerups.lasers << endl;
            player.powerups.nukes = get_int(0, int_max, "New Nukes:");
            player.powerups.lasers = get_int(0, int_max, "New Lasers:");
            break;
    }
}

void changeMenu(Menu* menu) {
    menu_to_show = menu;
}

void save() {
    player.savePlayer();
}

void initialize() {
    // Method to initialize the menu system
    main_menu.addMenuOption("Store", std::bind(changeMenu, &store_menu));
    main_menu.addMenuOption("Battle", battle);
    main_menu.addMenuOption("Scout", scout);
    main_menu.addMenuOption("Gamble", gamble);
    main_menu.addMenuOption("Hospital", hospital);
    if (debug) {
        main_menu.addMenuOption("Debug", std::bind(changeMenu, &debug_menu));
    }
    main_menu.addMenuOption("Quit & Save", retire);

    store_menu.addMenuOption("Troops", std::bind(store, 0));
    store_menu.addMenuOption("Powerup", std::bind(store, 1));
    store_menu.addMenuOption("Token", std::bind(store, 2));
    store_menu.addMenuOption("Items", std::bind(store, 3));

    if (debug) {
        debug_menu.addMenuOption("Username", std::bind(debugger, 0));
        debug_menu.addMenuOption("Money", std::bind(debugger, 1));
        debug_menu.addMenuOption("Troops", std::bind(debugger, 2));
        debug_menu.addMenuOption("Battles Won", std::bind(debugger, 3));
        debug_menu.addMenuOption("Total Battles", std::bind(debugger, 4));
        debug_menu.addMenuOption("Tokens", std::bind(debugger, 5));
        debug_menu.addMenuOption("HP", std::bind(debugger, 6));
        debug_menu.addMenuOption("Powerups", std::bind(debugger, 7));
        debug_menu.addMenuOption("Save", save);
    }

    menu_to_show = &main_menu;
}

int menu(Menu* menu) {
    while (true) {
        stats();

        menu->printMenu();
        int choice = get_int(0, menu->getSize(), "Enter an option:");
        if (choice <= menu->getSize() && choice >= 0) {
            if ((menu->menuId == store_menu.menuId ||
                 menu->menuId == debug_menu.menuId) &&
                choice == menu->getSize()) {
                menu_to_show = menu->getParent();
            } else {
                menu->callMenuOption(choice);
            }
        }
        return choice;
    }
}

int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if (arg == "--debug") {
            debug = true;
        }
    }
    system("CLS");
    cout << "Text Wars V" << VERSION << endl;
    if (debug) {
        cout << "Debugging is enabled" << endl;
    }
    cout << endl;
    cout << "Lets start with a few questions!" << endl;
    cout << "What is your name: ";
    cin >> player.username;

    bool yes_no;
    yes_no = get_bool("Have you played before?");

    if (yes_no) {
        player.played_before = true;
        player.loadPlayer();
        cout << "Loaded your save file. To start a new game delete your old one." << endl;
        system("PAUSE");
    } else {
        player.played_before = false;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    initialize();

    int choice;

    while (true) {
        choice = menu(menu_to_show);
    }
}