#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
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
write(r(2));
}