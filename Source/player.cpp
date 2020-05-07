#include <iostream>

using namespace std;

class Player {
  public:
    string username;
    bool played_before = false;
    float money = 500;
    int troops[2] = {1, 0};
    int battles_won = 0;
    int total_battles = 0;
    int tokens = 1;
    int hp = 50;
    int powerups[2] = {0, 0};
};