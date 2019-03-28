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


int main () {

    if (10100 == translate(20)) {
        printf("函数正确.\n");
    }
    else
    {
        printf("错了，接着写.\n");
    }
    
    

    return 0;
}