#include <stdio.h>

int translate(int shi){
    int a,b=0,c[20],er;
    while(shi!=0){
        a=shi%2;
        c[b]=a;
        b++;
        shi=shi/2;
    }
    b--;
    for(;b>=0;b--){
       er=printf("%d",c[b]); 
    }
    return er;

}
long long convertDecimalToBinary(int num)
{
    long long binaryNumber = 0;
    int remainder, i = 1;
 
    while (num != 0)
    {
        remainder = num % 2;
        num /= 2;
        binaryNumber += remainder * i;
        i *= 10;
    }
    return binaryNumber;
}

int main () {

    printf("%d", convertDecimalToBinary(100));
    

    return 0;
}