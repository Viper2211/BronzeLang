# BronzeLang
BronzeLang is a simple compiled programming language that emphasizes quick typing.
Most keywords are symbols, except for the booleans. 
## Design Choices
There were several difficult choices that we had to make while writing BronzeLang, and in this preface, I would like to explain them.

A major one of these was the choice of compiled vs. interpreted. I chose compiled, because I genuinely prefer statically typed programming languages over dynamically typed programming language. I wanted to bring out the best I could in BronzeLang

Another choice came to either compiled with llvm or transpiled. Due to the time crunch, I ended up choosing transpiled. I hope to improve this later on, but it is questionable.

Probably the most difficult choice was which symbols to use and which to ignore. I spent many hours mulling over this idea. 

### Type system
Integers got the `#` symbol because it is often the shorthand for number when taking notes.

Strings got `$` because I thought that $ looked kind of like an S (yes I know that's a bad reason, but it seemed ok at the time).

Booleans got `%` mainly because I had no idea what other symbol I could use.

# Syntax

```
; Comment

# integer = 1 ; Integer
$ string = "Hello world" ; String 
% boolean = false ; boolean

# MATH = 1+1/1%2*100
```

```
; If statements
? integer == 1 
  ; is one
.
```

```
; For loop
; goes from the range of 1 - 4
@ i 1|4

.
```
```
; increment is optional
@ i 1|20|2

.
```
```
; While loop
# a = 0
@@ a < 10
  a = a + 10
.
```
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
```
; Standard Library
; Bronze has a simple standard library and access to the cpp standard library
--> ./bronze/std.brz

; Print function
; displays text on the screen
write("Hello Bronze!")

; Get function
; gets user input
$ name = "John"
write("What is your name")
name = get()
; saying hello!
write("Hello "+name)
```