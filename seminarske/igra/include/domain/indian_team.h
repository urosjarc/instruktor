//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_INDIAN_TEAM_H
#define IGRA_INDIAN_TEAM_H


#include <vector>
#include "indian.h"

class IndianTeam {
public:
    IndianTeam(int x, int y);
    char name[10]{};
    int x;
    int y;

    std::vector<Indian*> indians;
};

#endif //IGRA_INDIAN_TEAM_H
