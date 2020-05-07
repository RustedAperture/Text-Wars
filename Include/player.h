#ifndef PLAYER_H
#define PLAYER_H

#include <algorithm>
#include <fstream>
#include <iostream>

struct Troops {
    int active_duty;
    int reserve;
};

struct Powerups {
    int nukes;
    int lasers;
};

class Player {
  public:
    std::string username;

    bool played_before;

    float money;

    Troops troops;

    int battles_won;
    int total_battles;
    int tokens;
    int hp;

    Powerups powerups;

    Player();
    ~Player();

    int loadPlayer();
    int savePlayer();

  private:
};

#endif