#include <utility>

//
// Created by urosjarc on 2. 06. 20.
//

#ifndef IGRA_SCORE_H
#define IGRA_SCORE_H

class Score {
public:
    Score(std::string name, int score, std::string date = currentDateTime()) {
        this->name = std::move(name);
        this->score = score;
        this->date = date;
    }

    std::string name;
    int score;
    std::string date;
};

#endif //IGRA_SCORE_H
