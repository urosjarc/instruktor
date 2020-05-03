cmake_minimum_required(VERSION 3.15)
project(igra)

set(CMAKE_CXX_STANDARD 14)


find_package(SDL2 REQUIRED)
include_directories(PUBLIC include)

add_executable(igra
        source/domain/bad_guy.cpp
        source/domain/fire.cpp
        source/domain/hero.cpp
        source/domain/indian.cpp
        source/domain/indian_team.cpp
        source/domain/tree.cpp
        source/domain/warrior.cpp
        source/domain/world.cpp
        source/app/game.cpp
        source/app/terminal.cpp
        source/app/window.cpp
        source/app/utils.cpp
        source/main.cpp)

target_link_libraries(igra ${SDL2_LIBRARIES})
