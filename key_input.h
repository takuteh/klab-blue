#ifndef KEY_INPUT_H
#define KEY_INPUT_H

namespace blue{
class Key_input{
    public:
        Key_input();
        ~Key_input();
        int ch[3];
        void get_keyinput(int &mode);
};
}//namespace blue

#endif
