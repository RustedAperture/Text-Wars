#include "menu.h"

#include <stdlib.h>
#include <time.h>

Menu::Menu() {}

Menu::Menu(std::string menu_title, Menu* parentMenu) :
  _menuTitle(menu_title), _parentMenu(parentMenu) {
    if (this->_parentMenu != NULL) {
        this->hasParent = true;
    }
    srand(time(NULL));
    this->menuId = rand() % 100;
}

Menu::~Menu(){};

void Menu::addMenuOption(std::string text, MenuPointer function) {
    int id = this->_menuOptions.size();
    MenuOption menuOption = {id, text, function};
    this->_menuOptions.push_back(menuOption);
}

void Menu::callMenuOption(int id) {
    this->_menuOptions[id].function();
}

void Menu::printMenu() {
    std::cout << this->_menuTitle << std::endl;
    std::cout << "--------------------" << std::endl;
    for (MenuOption entry : this->_menuOptions) {
        std::cout << entry.id << ". " << entry.text << std::endl;
    }
    if (this->hasParent) {
        std::cout << this->_menuOptions.size() << ". Previous Menu" << std::endl;
    } else {
        std::cout << this->_menuOptions.size() << ". Quit" << std::endl;
    }
}

int Menu::getSize() {
    return this->_menuOptions.size();
}

Menu* Menu::getParent() {
    return this->_parentMenu;
}