#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
int add  ( int a  , int b  )   {
return a + b ;
}
int write  ( std::string string  ) {
 std::cout<< string << std::endl;
}
int write  ( int string  ) {
 std::cout<< string << std::endl;
}
std::string get  (  ) {
 std::string input = "";
 std::cin >> input;
return input ;
}
int r  ( int i  ) {
 if (isdigit(i)){;
   std::cout << rand() % i;
 };
}
int square  ( int a  ) {
return a * a ;
}
int square_root  ( int a  ) {
 return sqrt(a);
}
int logarithm  ( int a  ) {
 return log(a);
}
int e_xp  ( int a  ) {
 return exp(a);
}

int main(){
int integer = 1  ;
std::string string = "Hello world"  ;
bool boolean = false  ;
if ( integer == 1  ) {
}
for (int i=1 ;i<4 ;i++) {
}
for (int i=1 ;i<20 ;i+=2 ) {
}
int a = 0 ;
while ( a < 10 ) {
a = a + 10 ;
}
int sum = add ( 1 , 2 ) ;
write("Hello Bronze!");
write("What is your name");
std::string name = get ( ) ;
}