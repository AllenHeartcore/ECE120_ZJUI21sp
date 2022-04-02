#include <stdio.h>
 
int main()
{
    double val1 = -22;
    double val2 = 33;
    double val3 = 12;
    double val4 = 10;
    double val5 = 3;
    int    resa1, resb1, resc1;
    unsigned int  resa2, resb2, resc2;
    float  resa3, resb3, resc3;
    double resa4, resb4, resc4;
 
    resa1 = val1 * val2;
    resa2 = val1 * val2;
    resa3 = val1 * val2;
    resa4 = val1 * val2;
    resb1 = val3 / val5;
    resb2 = val3 / val5;
    resb3 = val3 / val5;
    resb4 = val3 / val5;
    resc1 = val4 / val5;
    resc2 = val4 / val5;
    resc3 = val4 / val5;
    resc4 = val4 / val5;
 
    printf("Res A: I=%d U=%u F=%f D=%lf\n", resa1, resa2, resa3, resa4);
    printf("Res B: I=%d U=%u F=%f D=%lf\n", resb1, resb2, resb3, resb4);
    printf("Res C: I=%d U=%u F=%f D=%lf\n", resc1, resc2, resc3, resc4);
    printf("Bonus: %i %i\n", 12 % 3, -11 % 3);
 
    return 0;
}

