cmake_minimum_required(VERSION 3.15)
project(igra)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_CXX_STANDARD 14)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)
find_package(SDL2 REQUIRED)

include_directories(PUBLIC include)

add_executable(igra
        source/gui/MainWindow.cpp
        source/gui/MainWindow.ui
        source/domain/bad_guy.cpp
        source/domain/fire.cpp
        source/domain/hero.cpp
        source/domain/indian.cpp
        source/domain/indian_team.cpp
        source/domain/tree.cpp
        source/domain/warrior.cpp
        source/domain/world.cpp
        source/app/window.cpp
        source/app/utils.cpp
        source/main.cpp
        )

target_include_directories(igra PUBLIC include ${CMAKE_BINARY_DIR})

target_link_libraries(igra Qt5::Widgets)
target_link_libraries(igra ${SDL2_LIBRARIES})
