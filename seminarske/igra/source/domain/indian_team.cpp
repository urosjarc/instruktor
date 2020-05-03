#include "domain/indian_team.h"

IndianTeam::IndianTeam(int x, int y) {
    this->x = x;
    this->y = y;

    auto indian = new Indian(x, y);
    this->indians.push_back(indian);
}
