#include "player.h"

#include "tinyxml2.h"

#include <any>
#include <sstream>

using namespace tinyxml2;

Player::Player() {
    this->testing["played_before"] = 0;
    this->testing["money"] = 500;
    this->testing["troops.active_duty"] = 1;
    this->testing["troops.reserve"] = 0;
    this->testing["battles_won"] = 0;
    this->testing["total_battles"] = 0;
    this->testing["tokens"] = 1;
    this->testing["hp"] = 50;
    this->testing["powerups.nukes"] = 0;
    this->testing["powerups.lasers"] = 0;
}

Player::~Player() {}

int Player::loadPlayer() {
    XMLDocument doc;
    std::stringstream ss;
    ss << this->username << ".save";
    doc.LoadFile(ss.str().c_str());

    XMLElement* pPlayer = doc.FirstChildElement("player");
    XMLElement* pProperty = pPlayer->FirstChildElement("property");

    if (pProperty != NULL) {
        while (pProperty) {
            std::string name = pProperty->Attribute("name");
            int value = pProperty->IntAttribute("value");
            this->testing[name] = value;
            pProperty = pProperty->NextSiblingElement("property");
        }
    }

    return 0;
}

int Player::savePlayer() {
    std::ofstream save;
    std::stringstream ss;
    ss << this->username << ".save";
    save.open(ss.str());

    save << "<player username=\"" << this->username << "\">" << std::endl;
    for (auto const& playerVar : this->testing) {
        save << "\t<property name=\"" << playerVar.first << "\" value=\""
             << playerVar.second << "\"/>" << std::endl;
    }
    save << "</player>" << std::endl;
    return 0;
}