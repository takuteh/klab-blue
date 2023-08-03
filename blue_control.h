#ifndef BLUE_CONTROL_H
#define BLUE_CONTROL_H

namespace blue{
class Blue_control{
    public:
        void forward(float voltage,int mode);
        void backward(float voltage,int mode);
        void right(float voltage,int mode);
        void left(float voltage,int mode);
};
}//namespace blue

#endif