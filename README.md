# BronzeLang
BronzeLang is a simple compiled programming language that emphasizes quick typing.
Most keywords are symbols, except for the booleans (true and false). Code is written in the `.brz` file. 

BronzeLang currently includes :
- Variable declaration and assignments
- If statements
- For loops
- While loops
- Functions
- Classes
- Imports
- Standard Library

## Design Choices
There were several difficult choices that we had to make while writing BronzeLang, and in this preface, I would like to explain them.

A major one of these was the choice of compiled vs. interpreted. I chose compiled, because I genuinely prefer statically typed programming languages over dynamically typed programming language. I wanted to bring out the best I could in BronzeLang

Another choice came to either compiled with llvm or transpiled. Due to the time crunch, I ended up choosing transpiled. I hope to improve this later on, but it is questionable.

Probably the most difficult choice was which symbols to use and which to ignore. I spent many hours mulling over this idea. 

Eventually, I decided on a select few symbols that almost nobody uses seperately on their own.
 
# Syntax

## Hello world!
Let's get started with the classic Hello world!
```
--> ./bronze/io.brz

printf("Hello world!")
```
Output:
```
> Hello world!
```
To get a a better understanding of this code, we must understand what each line does.
Line one is an import statement, which gets the bronze standard lib. Because of this, the file gets access to all of the C++ standard library. This then lets us use `printf` to write "Hello world!" to the screen.

This should display "Hello world!". Otherwise, there might be some problem with the version of BronzeLang you are using.
## Variables
Variables in BronzeLang are statically typed. There are currently 4 basic types : String, Integer, Float, and Boolean (If you want to you can add your own types later on, because of the ability to write cpp code while in a .brz file). Below is the example code on how to define variables!
```
; Comment

# integer = 1 ; Integer
## floating_point = 1.0; Float
$ string = "Hello world" ; String 
% boolean = false ; boolean

# MATH = 1+1/1%2*100
```
Let's step through this file. The first line is a comment, which gets ignored by the lexer(yes comments are written after semicolons. This was also one of the reasons BronzeLang doesn't require users to add semicolons at the end of lines).

The next few lines are variable declarations. This transpiles to the following C++ code:
```
int integer = 1;
float float = 1.0;
std::string string = "Hello world";
bool boolean = false;

int MATH = 1+1/1%2*100;
```

## If Statements
If statements in bronze are fairly straight forward. Below is the general syntax:
```
? <condition>
    <do stuff here>
.
```
Another thing to remember is that tabs and spaces are not required in an if statement. But, doing that is a good practice and it makes code more readable. So, I will continue to add tabs throughout this entire tutorial.

Now that that's out of the way, let's look at another one of the examples :
```
--> ./bronze/io.brz

; If statements
# number = 10

? number == 1 
  write("the number is equal to 1!")
.
write(number)
```
This should display only `The number was... 10.000000!` Otherwise, double check you have the right code.

## For loops
Next we have, for loops. The general syntax is below:
```
@ <variable> <start>|<end>
  <do stuff here>
.
```
The example that comes along with BronzeLang is below:
```
--> ./bronze/io.brz 

; For loop
; goes from the range of 1 - 4 (excluding 4)
@ i 1|4
  write("%i\n", i)
.
```
This should display the number 1-3 (because 4 is excluded) on the screen when run.

But, that's not where it ends. A for loop can also have an increment (though this is entirely optional). The example below prints all even numbers from 0-20 (once again, excluding 20):
```
--> ./bronze/io.brz 

; increment is optional
@ i 0|20|2
  write(i)
.
```

## While loops
While loops are another feature of BronzeLang. The general syntax of a while loop is below:
```
@@ <condition>
  <do stuff here>
.
```
Here is an example:
```
--> ./bronze/io.brz

; While loop
# a = 0
@@ a < 10
  write(a)
  a = a + 1
.
```
This should print the number 0-9.
## Functions
```
;Functions

^ # add(#a, #b) ; the # means that this function will return either null or an integer
  >> a + b; return statement
.
```
```
; Function call
#sum = add(1,2);
```
## Imports and Standard Library
```
; Standard Library
; Bronze has a simple standard library and access to the cpp standard library
--> ./bronze/io.brz
--> ./bronze/random.brz
--> ./bronze/math.brz
```
Bronze has a simple standard library. It features only a few functions, many of which can be used for math.

### write()
```
; write() function
; displays text on the screen
write("Hello Bronze!")
```
The `write()` function is used for output. It takes 1 argument of any type.
### get()
```
; get() function
; gets user input
write("What is your name")
$ name = get()
```
The `get()` function "gets" input from the user.
It return a string, thus you can do something like the following.
```
write("Hello, "+name)
```
### Random
- `random()` - This function returns a andom number
- `randint(x)` - This function returns a random number between 0 and that number.

### Math
- `square(x)` - This function returns the parameter squared
- `sqrt(x)` or `square_root(x)` - This function returns the sqrt of the value of the argument
- `logarithm(x)` or `log(x)` - This function returns the natural logarithm of the argument.
- `exp(x)` or `e_xp(x)` - This function returns the `e` to the power of the parameter
- `sin(x)` , `cos(x)`, `tan(x)`, `sinh(x)`, `tanh(x)`, `cosh(x)` - Trigonometry functions
- `PI` - A variable holding the value of pi.
## Classes
Last, but not least, we have classes and object oriented programming.

Here is the syntax:
```
^^ <classname>
  _ <public variable>
  __ <protected variable>
  ___ <private variable>

  _ ^ <public function>(<args>)
    ; stuff
  .

  __ ^ <protected function>(<args>)
    ; more stuff
  .

  ___ ^ <private function>(<args>)
    ; secret stuff
  .

.  
```
And here's and example class. This should print out "Viper".
```
--> ./bronze/std.brz

^^ Programmer
  _ $ name = "Your average programmer..."

  ^ Programmer()

  .

  ^ Programmer($username)
    ? username == "Viper2211"
      username = "Aniruth A"
    .
    name = username
  .

  ^ # printname()
    write(name)
  .
.

Programmer me = Programmer("Viper2211")
me.printname()
```

# Credits
Team :
- @Viper2211 (Aniruth Ananthanarayanan)
- @Aaku (Aakarshan Kumar)
- @SupraJ1 (Suprasada Jagadeeshi)

Work : 
- Lexer - @Viper2211
- Parser - @Viper2211 
- Comments - @Aaku
- Stdlib - @Aaku
- Syntax - @Viper2211 and @SupraJ1
