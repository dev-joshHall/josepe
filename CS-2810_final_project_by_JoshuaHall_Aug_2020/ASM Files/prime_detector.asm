; File name: prime_detector.asm
; Creator: Joshua Hall (10787004)
; Last edited: Aug 7, 2020
; Assembly language: LC-3
; File description: Determines whether an input number is prime or not. Results are displayed to the console.
;                   Works for numbers 1 - 9,999. Until the user enters "0", the program will
;                   continue to prompt the user for input.
; Error handling: If the user enters any non-integer input, an invalid input string will be displayed, and the user will
;                 be prompted to try again. The user will not be able to enter a number larger than 4 digits long.
; Dependencies: read.asm (x4000), multiply.asm (x4100), string2num.asm (x4200), get_chars_sub.asm (x4300).
.ORIG x3000

WELCOME
    LEA R0, WELCOMESTR; load address for welcome string to R0 for output
    PUTS; output string

CLEARREGS
    AND R0, R0, x0; clear R0
    AND R1, R1, x0; clear R1
    AND R2, R2, x0; clear R2
    AND R3, R3, x0; clear R3
    AND R4, R4, x0; clear R4
    AND R5, R5, x0; clear R5
    AND R6, R6, x0; clear R6

GETCHARACTERS
    LD R0, GETCHARS
    JSRR R0
    ADD R3, R0, x0; copy input to R3

VALIDATE
    ADD R1, R1, x0; check if R1 is negative
    BRn INVALIDINPUT; a negative error code means an invalid input
    AND R1, R1, x0; clear R1
    ADD R3, R3, x0; check if 0 was entered
    BRz EXITPROGRAM; if 'Enter' or '0' was entered, exit the program
    ADD R6, R3, x-2; check if input is less than 2
    BRn NOTPRIME; if input is lower than 2, the number is not prime by definition
    AND R6, R6, x0; clear R6
    ADD R2, R2, x2; start R2 at 2

LOOP
    ADD R0, R3, x0; copy input number into R0

NEGATENUM
    NOT R5, R2; not R2 as first step of two's compliment. Store in R5
    ADD R5, R5, x1; R5 holds negated number. Used to check if input number is greater than the number
    ADD R4, R3, R5; R4 = INPUT - NUMBER
    BRz PRIME; R4 is zero when the number is the input. If so, the input number is not evenly divisible by any lower numbers and therefore is also prime
    BRp DIVAGAIN; if input is larger than the number, branch to DIVAGAIN
    ADD R2, R2, x1; increment R2
    BRnzp LOOP; rerun the loop with a number one higher

DIVAGAIN; dividing is not done to find the quotient, but only the remainder
    ADD R0, R0, R5; decrement R0 by the current prime number
    BRn DIVFINISH; if R0 is negative exit the subtracting loop
    BRzp DIVAGAIN; continue subtracting

DIVFINISH
    ADD R0, R0, R2; R0 is the remainder
    BRz NOTPRIME; if remainder is 0, the number is not prime
    ADD R2, R2, x1; increment R2 to be the next number
    BRnzp LOOP; rerun the loop using the next value of the PRIMES array

NOTPRIME
    LEA R0, NOTPRIMESTR; load not prime string address into R0
    PUTS; output string
    BRnzp CLEARREGS; rerun the program

PRIME
    LEA R0, PRIMESTR; load prime string address into R0
    PUTS; output string
    BRnzp CLEARREGS; rerun the program

INVALIDINPUT
    LEA R0, INVALIDSTR; load invalid string address into R0
    PUTS; output string
    BRnzp WELCOME; rerun the program

EXITPROGRAM
    LEA R0, EXITSTR; load exit program string address into R0
    PUTS; output string
    HALT; halt the program

GETCHARS
    .FILL x4300; memory location for the get characters subroutine

ASCIISHIFT
    .FILL x-30; negative shift value to convert an ascii character to an integer

SHIFTEDQ
    .FILL x-21; the shifted ascii value of an uppercase 'Q'

SHIFTEDLOWERq; the shifted ascii value of a lowercase 'q'
    .FILL x-41

WELCOMESTR
    .STRINGZ "Enter a number to see if it is prime. Enter '0' to exit.\n> "

NOTPRIMESTR
    .STRINGZ "\nThe number is not prime.\n\nEnter another number or '0' to exit.\n> "

PRIMESTR
    .STRINGZ "\nThe number is prime.\n\nEnter another number or '0' to exit.\n> "

INVALIDSTR
    .STRINGZ "\nInvalid Input. Try again.\n\n"

EXITSTR
    .STRINGZ "\nExiting Program.\n"

.END
