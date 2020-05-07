#include "player.h"

#include <config4cpp/Configuration.h>

#include <sstream>

using namespace config4cpp;

Player::Player() {
    this->played_before = false;
    this->money = 500;
    this->troops = {1, 0};
    this->battles_won = 0;
    this->total_battles = 0;
    this->tokens = 1;
    this->hp = 50;
    this->powerups = {0, 0};
}

Player::~Player() {}

int Player::loadPlayer() {
    std::stringstream ss;
    ss << this->username << ".cfg";

    Configuration* cfg = Configuration::create();
    const char* cfgFile = ss.str().c_str();
    const char* scope = this->username.c_str();

    try {
        cfg->parse(cfgFile);
        this->played_before = cfg->lookupBoolean(scope, "played_before");
        this->money = cfg->lookupInt(scope, "money");
        this->troops.active_duty = cfg->lookupInt(scope, "troops.active_duty");
        this->troops.reserve = cfg->lookupInt(scope, "troops.reserve");
        this->battles_won = cfg->lookupInt(scope, "battles_won");
        this->total_battles = cfg->lookupInt(scope, "total_battles");
        this->tokens = cfg->lookupInt(scope, "tokens");
        this->hp = cfg->lookupInt(scope, "hp");
        this->powerups.nukes = cfg->lookupInt(scope, "powerups.nukes");
        this->powerups.lasers = cfg->lookupInt(scope, "powerups.lasers");
    } catch (const ConfigurationException& ex) {
        std::cerr << ex.c_str() << std::endl;
        cfg->destroy();
        return 1;
    }
    cfg->destroy();
    return 0;
}

int Player::savePlayer() {
    std::stringstream ss;
    ss << this->username << ".cfg";

    std::ofstream cfgFile;
    cfgFile.open(ss.str());
    cfgFile << this->username << " {" << std::endl;
    if (this->played_before) {
        cfgFile << "\tplayed_before = \"true\";" << std::endl;
    } else {
        cfgFile << "\tplayed_before = \"false\";" << std::endl;
    }
    cfgFile << "\tmoney = \"" << this->money << "\";" << std::endl;
    cfgFile << "\ttroops {" << std::endl;
    cfgFile << "\t\tactive_duty = \"" << this->troops.active_duty << "\";" << std::endl;
    cfgFile << "\t\treserve = \"" << this->troops.reserve << "\";" << std::endl;
    cfgFile << "\t};" << std::endl;
    cfgFile << "\tbattles_won = \"" << this->battles_won << "\";" << std::endl;
    cfgFile << "\ttotal_battles = \"" << this->total_battles << "\";" << std::endl;
    cfgFile << "\ttokens = \"" << this->tokens << "\";" << std::endl;
    cfgFile << "\thp = \"" << this->hp << "\";" << std::endl;
    cfgFile << "\tpowerups {" << std::endl;
    cfgFile << "\t\tnukes = \"" << this->powerups.nukes << "\";" << std::endl;
    cfgFile << "\t\tlasers = \"" << this->powerups.lasers << "\";" << std::endl;
    cfgFile << "\t};" << std::endl;
    cfgFile << "};" << std::endl;
}