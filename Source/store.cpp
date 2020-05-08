#include "store.h"

#include "tinyxml2.h"

#include <iostream>
#include <sstream>

using namespace tinyxml2;

Store::Store() {}

Store::~Store() {}

void Store::parseStoreCFG() {
    XMLDocument doc;
    std::stringstream ss;
    ss << "Config/store.xml";
    doc.LoadFile(ss.str().c_str());

    XMLElement* pScope = doc.FirstChildElement("scope");
    XMLElement* pCategory = pScope->FirstChildElement("category");

    if (pCategory != NULL) {
        while (pCategory) {
            std::string pCategoryName = pCategory->Attribute("name");
            this->addCategory(pCategoryName);

            XMLElement* pItem = pCategory->FirstChildElement("item");
            if (pItem != NULL) {
                while (pItem) {
                    std::string pItemName = pItem->Attribute("name");
                    std::string pItemVar = pItem->Attribute("var");
                    int pItemCost = pItem->IntAttribute("cost");

                    Item item = {pCategoryName, pItemName, pItemVar, pItemCost};
                    this->addItem(item);
                    pItem = pItem->NextSiblingElement("item");
                }
            }
            pCategory = pCategory->NextSiblingElement("category");
        }
    }
}

void Store::addItem(Item item) {
    this->_items.push_back(item);
}

void Store::addCategory(std::string category) {
    this->_categories.push_back(category);
}

void Store::showCategory(std::string category) {
    for (int i = 0; i < this->getItems(category).size(); i++) {
        std::cout << i << ". " << this->getItems(category)[i].name << std::endl;
    }
}

void Store::showItem(Item item) {
    std::cout << item.name << " for $" << item.cost << " each." << std::endl;
}

std::vector<std::string> Store::getCategories() {
    return this->_categories;
}

std::vector<Item> Store::getItems(std::string category) {
    std::vector<Item> items;
    for (Item item : this->_items) {
        if (item.category == category)
            items.push_back(item);
    }
    return items;
}