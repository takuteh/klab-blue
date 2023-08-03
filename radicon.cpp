#include "blue_control.h"
#include <unistd.h>
#include <iostream>
using namespace std;

int main(){
blue::Blue_control blue_control;
int mode;
while(1){
   cout>>"1:forward,2:backward,3:right,4:left->";
cin>>mode;

if(mode==1){
blue_control.forward(1.0,1);
}else if(mode==2){
blue_control.backward(1.0,1);
}else if(mode==3){
blue_control.right(1.0,1);
}else if(mode==4){
blue_control.left(1.0,1);
}
}
return 0;
}
