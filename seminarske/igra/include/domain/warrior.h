//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_WARRIOR_H
#define IGRA_WARRIOR_H

class Warrior {
public:
    Warrior(int x, int y, int invincibleRadius = 4){
        this->x = x;
        this->y = y;
        this->invincibleRadius = invincibleRadius;
    }
    int invincibleRadius;
    bool invincible = false;
    int y;

    int x;

    void move();
};


#endif //IGRA_WARRIOR_H
