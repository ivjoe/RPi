#! /bin/bash

g++ `sdl-config --cflags` `sdl-config --libs` -lSDL_image -lSDL_ttf -o sdl sdl.cpp
