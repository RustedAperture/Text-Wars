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
    save << "\t<property name=\"played_before\" value=\""
         << this->testing["played_before"] << "\"/>" << std::endl;
    save << "\t<property name=\"money\" value=\"" << this->testing["money"] << "\"/>"
         << std::endl;
    save << "\t<property name=\"troops.active_duty\" value=\""
         << this->testing["troops.active_duty"] << "\"/>" << std::endl;
    save << "\t<property name=\"troops.reserve\" value=\""
         << this->testing["troops.reserve"] << "\"/>" << std::endl;
    save << "\t<property name=\"battles_won\" value=\"" << this->testing["battles_won"]
         << "\"/>" << std::endl;
    save << "\t<property name=\"total_battles\" value=\""
         << this->testing["total_battles"] << "\"/>" << std::endl;
    save << "\t<property name=\"tokens\" value=\"" << this->testing["tokens"] << "\"/>"
         << std::endl;
    save << "\t<property name=\"hp\" value=\"" << this->testing["hp"] << "\"/>"
         << std::endl;
    save << "\t<property name=\"powerups.nukes\" value=\""
         << this->testing["powerups.nukes"] << "\"/>" << std::endl;
    save << "\t<property name=\"powerups.lasers\" value=\""
         << this->testing["powerups.lasers"] << "\"/>" << std::endl;
    save << "</player>" << std::endl;
    return 0;
}