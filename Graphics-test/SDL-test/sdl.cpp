#include <stdio.h>
#include <cstdlib>
#include <iostream>
#include <SDL/SDL.h>
#include <SDL/SDL_ttf.h>
#include <SDL_image.h>

SDL_Surface* screen;
SDL_Surface* message;
SDL_Surface* image;
SDL_Rect messageRect;
TTF_Font* font;
const SDL_Color textColor = {200, 200, 200};

int main( int argc, char* args[] ) {
    if (SDL_Init(SDL_INIT_VIDEO) !=0)
    {
        std::cerr << "SDL_Init failed\n";
        exit(EXIT_FAILURE);
    }
    if (TTF_Init() != 0) {
        std::cerr << "TTF_Init failed\n";
        exit(EXIT_FAILURE);
    }
    const SDL_VideoInfo* videoInfo = SDL_GetVideoInfo();
    int systemX = videoInfo->current_w;
    int systemY = videoInfo->current_h;
    Uint8 bpp = videoInfo->vfmt->BitsPerPixel;
    screen = SDL_SetVideoMode(systemX, systemY, bpp, SDL_SWSURFACE); // SDL_HWSURFACE | SDL_DOUBLEBUF
    if (!screen)
    {
        std::cerr << "SDL_SetVideoMode failed\n";
        exit(EXIT_FAILURE);
    }

    SDL_Rect r1_1 = {0,0,100,100};
    SDL_FillRect(screen, &r1_1, SDL_MapRGB(screen->format, 255,0,0));
    SDL_Rect r1_2 = {100,0,100,100};
    SDL_FillRect(screen, &r1_2, SDL_MapRGB(screen->format, 0,255,0));
    SDL_Rect r1_3 = {200,0,100,100};
    SDL_FillRect(screen, &r1_3, SDL_MapRGB(screen->format, 0,0,255));
    
    SDL_Rect r2_1 = {0,100,100,100};
    SDL_FillRect(screen, &r2_1, SDL_MapRGB(screen->format, 0,255,0));
    SDL_Rect r2_2 = {100,100,100,100};
    SDL_FillRect(screen, &r2_2, SDL_MapRGB(screen->format, 0,0,255));
    SDL_Rect r2_3 = {200,100,100,100};
    SDL_FillRect(screen, &r2_3, SDL_MapRGB(screen->format, 255,0,0));
    
    SDL_Rect r3_1 = {0,200,100,100};
    SDL_FillRect(screen, &r3_1, SDL_MapRGB(screen->format, 0,0,255));
    SDL_Rect r3_2 = {100,200,100,100};
    SDL_FillRect(screen, &r3_2, SDL_MapRGB(screen->format, 255,0,0));
    SDL_Rect r3_3 = {200,200,100,100};
    SDL_FillRect(screen, &r3_3, SDL_MapRGB(screen->format, 0,255,0));
    
    font = TTF_OpenFont("fonts/verdana.ttf",72);
    if(!font){
        std::cerr << "TTF_OpenFont failed\n";
        exit(EXIT_FAILURE);
    }
    message = TTF_RenderUTF8_Blended(font,"Hello!",textColor);
    if(!message){
        std::cerr << "TTF_Render failed\n";
        exit(EXIT_FAILURE);
    }
    messageRect.x = (systemX / 2) - (message->w / 2);
    messageRect.y = (systemY / 2) - (message->h / 2);
    SDL_BlitSurface(message, NULL, screen, &messageRect);
    
    SDL_Surface* loaded = IMG_Load("logo.png");
    if(!loaded){
        std::cerr << "IMG_Load failed\n";
        exit(EXIT_FAILURE);
    }
    image = SDL_DisplayFormatAlpha(loaded);
    SDL_FreeSurface(loaded);
    SDL_BlitSurface(image, NULL, screen, NULL);

    SDL_Flip(screen);
    
    SDL_Event event;
    bool quit = false;
    while(!quit) {
        SDL_WaitEvent(&event);
        switch (event.type) {
            case SDL_QUIT : quit = true; break;
            case SDL_KEYDOWN: {
                printf("The %s key was pressed!\n", SDL_GetKeyName(event.key.keysym.sym));
                switch( event.key.keysym.sym ) {
                    case SDLK_ESCAPE :  quit = true; break;
                    default : break;
                }
            }
            default : break;
        }
    }
    
    //SDL_Delay(10000);
    
    TTF_CloseFont(font);
    TTF_Quit();
    SDL_FreeSurface(message);
    SDL_FreeSurface(image);
    SDL_FreeSurface(screen);
    SDL_Quit();

    return EXIT_SUCCESS;
}
