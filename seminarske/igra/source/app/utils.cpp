#include "../../include/app/utils.h"

#include <stdio.h>
#include <ctime>
#include <cstdlib>

int randomInt(int min, int max){
    srand(time(NULL));
    return min + ( std::rand() % ( max - min + 1 ) );
}

