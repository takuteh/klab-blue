#include "blue_control.h"
#include <unistd.h>
#include <iostream>
using namespace std;

int main(){
blue::Blue_control blue_control;
int mode;
while(1){
   cout<<"input voltage:";
    cin>>motor.voltage;
   cout>>"1:forward,2:backward,3:right,4:left->";
cin>>mode;

if(mode==1){
blue_control.forward();
}else if(mode==2){
blue_control.backward();
}else if(mode==3){
blue_control.right();
}else if(mode==4){
blue_control.left();
}
}
return 0;
}
