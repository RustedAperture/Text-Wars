#ifndef PLAYER_H
#define PLAYER_H

#include <algorithm>
#include <any>
#include <fstream>
#include <iostream>
#include <map>

class Player {
  public:
    std::map<std::string, int> testing;

    std::string username;

    Player();
    ~Player();

    int loadPlayer();
    int savePlayer();

  private:
};

#endif