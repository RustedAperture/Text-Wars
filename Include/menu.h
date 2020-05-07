#ifndef MENU_H
#define MENU_H

#include <functional>
#include <iostream>
#include <vector>

typedef std::function<void()> MenuPointer;

struct MenuOption {
    int id;
    std::string text;
    MenuPointer function;
};

class Menu {
  public:
    bool hasParent = false;

    int menuId;

    Menu();
    Menu(std::string menuTitle, Menu* parentMenu = NULL);
    ~Menu();

    void addMenuOption(std::string text, MenuPointer function);
    void callMenuOption(int id);
    void printMenu();

    int getSize();

    Menu* getParent();

  private:
    std::string _menuTitle;

    std::vector<MenuOption> _menuOptions;

    Menu* _parentMenu;
};

#endif