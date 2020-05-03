//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_TREE_H
#define IGRA_TREE_H

class Tree {
public:
    Tree(int x, int y) {
        this->x = x;
        this->y = y;
    }
    bool isAlive = true;
    int x;
    int y;
};

#endif //IGRA_TREE_H
