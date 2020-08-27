```
; Comment

# integer = 1 ; Integer
$ string = "Hello world" ; String 
% boolean = false ; boolean


;` If statements
? integer == 1 
  ; is one
.

; For loop
; goes from the range of 1 - 4
@ i 1|4

.

; increment is optional
@ i 1|20|2

.

; While loop
# a = 0
@@ a < 10
  a = a + 10
.

;Functions

^ # add(#a, #b) ; the # means that this function will return either null or an integer
  >> a + b; return statement
.

; Function call
#sum = add(1,2);


; Import
--> ./this_file_doesnt.exist

; Let's say that the file we imported had a function for multiplication!
; We can now use it here
#sum = multiplication_function(100)
```