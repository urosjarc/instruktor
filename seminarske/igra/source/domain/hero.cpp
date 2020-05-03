//
// Created by urosjarc on 1. 05. 20.
//


#include "../../include/domain/hero.h"
#include <iostream>


void Hero::move(int dx, int dy) {
    this->y += dy;
    this->x += dx;
}
Tree* Hero::plantTree(int x, int y) {
    std::cout << this << " plantTree" << std::endl;
    static auto tree = Tree(x, y);
    return &tree;
}



