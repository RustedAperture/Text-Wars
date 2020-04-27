#include <iostream>
#include <vector>

#include "Include/tsl/ordered_map.h"

using namespace std;

typedef void (*menu_method)(void);

class Menu
{
public:
    string name = "Main";
    vector<string> item_names;
    tsl::ordered_map<string, Menu *> submenus;
    vector<menu_method> item_methods;
    Menu *parent;
    Menu *self;

    void blank_method()
    {
    }

    void add_items(tsl::ordered_map<string, menu_method> items)
    {
        for (auto i : items)
        {
            this->item_names.push_back(i.first);
            this->item_methods.push_back(i.second);
        }
    }

    Menu new_sub_menu(string name, Menu *parent, Menu *self)
    {
        Menu submenu;
        submenu.name = name;
        submenu.parent = parent;
        submenu.self = self;
        this->submenus.insert({name, self});
        return submenu;
    }

    void display_menu()
    {
        string line(22, '-');
        cout << this->name << " Menu" << endl;
        cout << line << endl;
        for (int i = 0; i < this->item_names.size(); i++)
        {
            if (submenus.find(this->item_names[i]) != submenus.end())
            {
                cout << i << ". " << submenus.at(this->item_names[i])->name << endl;
            }
            else
            {
                cout << i << ". " << this->item_names[i] << endl;
            }
        }
    }
};