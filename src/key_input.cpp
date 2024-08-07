#include<stdio.h>
#include<termios.h>
#include<unistd.h>
#include "key_input.h"

struct termios oldt,newt;

namespace blue{
Key_input::Key_input(){
ch[3]={0};//キー入力格納用

tcgetattr(STDIN_FILENO,&oldt);//現在の端末設定保存
newt=oldt;

newt.c_lflag &= ~(ICANON|ECHO);
tcsetattr(STDIN_FILENO,TCSANOW,&newt);
}

Key_input::~Key_input(){
tcsetattr(STDIN_FILENO,TCSANOW,&oldt);//端末設定をリセット
}

void Key_input::get_keyinput(int &mode){
ch[0]=getchar();
if(ch[0]==0x1b){
    ch[1]=getchar();
    if(ch[1]==0x5b){
    ch[2]=getchar();
    switch (ch[2]){
    case 0x41://up
        mode=1;
        break;
    case 0x42://down
        mode=2;
        break;
    case 0x43://right
        mode=3;
        break;
    case 0x44://left
        mode=4;
        break;
    }
    }
}
}
}//namespace blue
