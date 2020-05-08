#ifndef STORE_H
#define STORE_H

#include <string>
#include <vector>

struct Item {
    std::string category;
    std::string name;
    std::string var;

    int cost;
};

class Store {
  public:
    Store();
    ~Store();

    void parseStoreCFG();
    void addItem(Item item);
    void addCategory(std::string category);
    void showCategory(std::string category);
    void showItem(Item item);

    std::vector<std::string> getCategories();
    std::vector<Item> getItems(std::string category);

  private:
    std::vector<std::string> _categories;
    std::vector<Item> _items;
};

#endif