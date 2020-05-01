cmake_minimum_required(VERSION 3.15)
project(igra)

set(CMAKE_CXX_STANDARD 14)

add_executable(igra source/main.cpp include/domain/world.h include/domain/hero.h include/domain/warrior.h include/domain/indian.h include/domain/indian_team.h include/domain/fire.h include/domain/bad_guy.h include/domain/tree.h)