#ifndef BLUE_CONTROL_H
#define BLUE_CONTROL_H

namespace blue{
class Blue_control{
    public:
        void forward(float voltage,float time);
        void backward(float voltage,float time);
        void right(float voltage,float time);
        void left(float voltage,float time);
};
}//namespace blue

#endif
