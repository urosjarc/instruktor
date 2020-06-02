#include <cmath>
#include <iostream>
#include <cmath>


#include "domain/world.h"
#include "app/utils.h"

using namespace std;

bool World::isDestroyed() {
    if(!this->hero->isAlive) return true;
    if(this->iterationsRunning >= this->iterationsToLive) return true;

    float treesDest = 0;

    for (int i = 0; i < this->trees.size(); ++i) {
        if(!this->trees[i]->isAlive) treesDest++;
    }

    return treesDest/this->trees.size() > 0.75;
}
void World::checkWarriorCollisions() {
    /**
     * Bad guys invincible status
     */
    for (int i = 0; i < this->badGuys.size(); ++i) {
        bool isFound = false;
        auto pBadGuy0 = this->badGuys[i];
        for (int j = 0; j < this->badGuys.size(); ++j) {
            auto pBadGuy1 = this->badGuys[j];
            float dx = pBadGuy0->x - pBadGuy1->x;
            float dy = pBadGuy0->y - pBadGuy1->y;
            float dist = pow(pow(dx, 2) + pow(dy, 2), 0.5);
            if(i!=j && pBadGuy0->invincibleRadius >= dist){
                pBadGuy0->invincible = true;
                cout << "bad guy " << i << " is now invincible" << endl;
                isFound = true;
                break;
            }
        }
        if (!isFound) {
            pBadGuy0->invincible = false;
            cout << "bad guy " << i << " is now  not invincible" << endl;
        }
    }

    bool heroIn = false;
    for (int i = 0; i < this->indianTeams.size(); i++) {
        for (int j = 0; j < indianTeams[i]->indians.size(); j++) {
            bool isFound = false;
            Indian* indian0 = indianTeams[i]->indians[j];
            float hd = sqrt(pow(indian0->x - hero->x, 2) + pow(indian0->y - hero->y, 2));
            if (hd <= hero->invincibleRadius) {
                hero->invincible = true;
                cout << "hero is now invincible" << endl;
                indian0->invincible = true;
                cout << "indian " << j << " is now invincible" << endl;
                heroIn = true;
                break;
            }
            for (int k = 0; k < this->indianTeams.size(); k++) {
                for (int l = 0; l < indianTeams[k]->indians.size(); l++) {
                    Indian* indian1 = indianTeams[k]->indians[l];

                    float dx = indian0->x - indian1->x;
                    float dy = indian0->y - indian1->y;
                    float dist = sqrt(pow(dx, 2) + pow(dy, 2));
                    if (j != l && indian0->invincibleRadius >= dist) {
                        indian0->invincible = true;
                        cout << "indian " << j << " is now invincible" << endl;
                        isFound = true;
                        break;
                    }
                }
                if (isFound)
                    break;
            }
            if (!isFound) {
                indian0->invincible = false;
                cout << "indian" << j << " is now not invincible" << endl;
            }
                
        }

    }
    if (!heroIn) {
       hero->invincible=false;
       cout << "hero  is now not invincible" << endl;
   }

    int badGuysSize = this->badGuys.size();
   for (int i = 0; i < badGuysSize; i++)
   {
       float distance, dx, dy;

       dx = hero->x - badGuys[i]->x;
       dy = hero->y - badGuys[i]->y;

       distance = sqrt(pow(dx, 2) + pow(dy, 2));

       if (distance < hero->killRadius) {
           if (hero->invincible == true && badGuys[i]->invincible == false) {
               badGuys.erase(badGuys.begin() + i);
               badGuysSize--;
               hero->reputation++;
               cout << "bad guys" << i << " is dead" << endl;
               i--;
               continue;
           }

           else if (hero->invincible == false && badGuys[i]->invincible == true) {
               hero->isAlive = false;
               cout << "hero is dead" << endl;
           }

           else {
               badGuys.erase(badGuys.begin() + i);
               badGuysSize--;
               hero->reputation++;
               cout << "bad guys" << i << " is dead" << endl;
               i--;
               continue;
           }
       }
       bool deadBadGuy = false;
       for (int k = 0; k < this->indianTeams.size(); k++) {
           int indianSize = indianTeams[k]->indians.size();
           for (int l = 0; l < indianSize; l++) {
               Indian* indian1 = indianTeams[k]->indians[l];

               float dx = badGuys[i]->x - indian1->x;
               float dy = badGuys[i]->y - indian1->y;
               float dist = sqrt(pow(dx, 2) + pow(dy, 2));

               if (dist < indian1->killRadius) {
                   if (indian1->invincible == true && badGuys[i]->invincible == false) {
                       badGuys.erase(badGuys.begin() + i);
                       badGuysSize--;
                       cout << "bad guys" << i << " is dead" << endl;
                       i--;
                       deadBadGuy = true;
                       break;
                   }

                   else {
                       indianTeams[k]->indians.erase(indianTeams[k]->indians.begin() + l);
                       indianSize--;
                       cout << "indian" << l << " is dead" << endl;
                       l--;
                       continue;
                   }
               }



           }
           if (deadBadGuy == true)
               break;
       }    
   }

   
 }

void World::checkFireCollisions() {
    for ( Fire* it:fires) {

        float distance = sqrt(pow(it->x - hero->x, 2) + pow(it->y - hero->y, 2));
        if (it->radius > distance) {
            it->isAlive = false;
            hero->reputation += it->radius;
            cout << "ogenj je pogasen" << endl;
            
        }
        for (IndianTeam* iteam : this->indianTeams) {
            for (Indian* indian : iteam->indians) {
                distance = sqrt(pow(indian->x - it->x, 2) + pow(indian->y - it->y, 2));
                if (it->radius > distance) {
                    it->isAlive = false;
                    cout << "ogenj je pogasen" << endl;
                    
                }
            }
        }
        
        for (Tree* tree : trees) {
            distance = sqrt(pow(it->x - tree->x, 2) + pow(it->y - tree->y, 2));
            if (distance < it->radius) {
                tree->isAlive = false;
            }
        }
    }
    for (int i = 0; i < fires.size(); i++) {
        if (fires[i]->isAlive == false) {
            fires.erase(fires.begin() + i);
            i--;
        }
    }
}
void World::nextIteration() {
    this->iterationsRunning++;

    for (int i = 0; i < this->badGuys.size(); ++i) {
        int dx = randomInt(-1, 1);
        int dy = randomInt(-1, 1);
        this->badGuys[i]->x += dx; //Todo implement this in .move()
        this->badGuys[i]->y += dy; //Todo implement this in .move()

        if (badGuys[i]->x < 0)
            badGuys[i]->x = 0;
        if (badGuys[i]->x >= this->width)
            badGuys[i]->x = this->width - 1;
        if (badGuys[i]->y < 0)
            badGuys[i]->y = 0;
        if (badGuys[i]->y >= this->height)
            badGuys[i]->y = this->height - 1;
    }

    for (int i = 0; i < this->indianTeams.size(); ++i) {
        for (int j = 0; j < this->indianTeams[i]->indians.size(); ++j) {
            auto pIndian = this->indianTeams[i]->indians[j];
            int dx = randomInt(-1, 1);
            int dy = randomInt(-1, 1);
            pIndian->x += dx; //Todo implement this in .move()
            pIndian->y += dy; //Todo implement this in .move()

            if (pIndian->x < 0)
                pIndian->x = 0;
            if (pIndian->x >= this->width)
                pIndian->x = this->width - 1;
            if (pIndian->y < 0)
                pIndian->y = 0;
            if (pIndian->y >= this->height)
                pIndian->y = this->height - 1;
        }
    }

    for (int i = 0; i < this->fires.size(); ++i) {
        this->fires[i]->radius += 0.1 * this->fireIndex;
    }

    if (hero->x < 0)
        hero->x = 0;
    if (hero->x >= this->width)
        hero->x = this->width - 1;
    if (hero->y < 0)
        hero->y = 0;
    if (hero->y >= this->height)
        hero->y = this->height - 1;

    auto p = new Point(hero->x, hero->y);
    hero->history.push_back(p);

    this->checkWarriorCollisions();
    this->checkFireCollisions();
}

World::World(Hero *hero, int fireIndex, int badGuysIndex, int indiansIndex, int waterIndex, int width, int height, int iterationsToLive) {

    this->hero = hero;
    this->fireIndex = fireIndex;
    this->badGuysIndex = badGuysIndex;
    this->indiansIndex = indiansIndex;
    this->waterIndex = waterIndex;
    this->width = width;
    this->height = height;
    this->iterationsToLive= iterationsToLive;

    for (int x = 0; x < this->width; ++x) {
        for (int y = 0; y < this->height; ++y) {
            auto tree = new Tree(x, y);
            this->trees.push_back(tree);
        }
    }
}

bool World::checkForNextLevel() {
    return badGuys.size() == 0 && fires.size() == 0 && hero->isAlive;
}
