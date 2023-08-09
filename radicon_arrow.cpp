#include "blue_control.h" 
#include "key_input.h" 
#include <unistd.h> 
#include <iostream>
using namespace std;

int main(){
blue::Blue_control blue_control;
blue::Key_input key_input;
int mode;
while(1){
   cout<<"select arrow!"<<endl;;
   key_input.get_keyinput(mode);

if(mode==1){
cout<<"forward ↑"<<endl;
blue_control.forward(2.0,1);
}else if(mode==2){
cout<<"backward ↓"<<endl;
blue_control.backward(2.0,1);
}else if(mode==3){
cout<<"right →"<<endl;
blue_control.right(1.5,0.2);
}else if(mode==4){
cout<<"left ←"<<endl;
blue_control.left(1.5,0.2);
}
}
return 0;
}
