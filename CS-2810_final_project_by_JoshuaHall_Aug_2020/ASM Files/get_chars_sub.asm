; File name: get_chars_sub.asm
; Creator: Joshua Hall (10787004)
; Last edited: Aug 7, 2020
; Assembly language: LC-3
; File description: Reads the users input for up to four characters or until they press 'Enter'. Converts that input
;                   into binary and leaves that value in R0. If a non-integer is entered, a negative error code will be
;                   in R1. Does not print prompt.
; Dependencies: read.asm (x4000), multiply.asm (x4100), string2num.asm (x4200).
; Parameters: None
; Return values: binary input number in R0, error code in R1
.ORIG x4300

ST R2, SAVER2; store R2
ST R3, SAVER3; store R3
ST R4, SAVER4; store R4
ST R5, SAVER5; store R5
ST R6, SAVER6; store R6
ST R7, SAVER7; store R7

START
    LEA R0, BUFFER; load the address for the buffer into R0
    LD R1, SIZE; load size of buffer into R1
    LD R2, READ; load address for read subroutine
    JSRR R2; execute read subroutine
    ADD R1, R0, x0; move R0 to R1 (the number of characters read)
    LEA R0, BUFFER; load the address for the buffer into R0
    LD R2, STRING2NUM; load address for the string2num subroutine
    JSRR R2; execute string2num subroutine
    ADD R3, R0, x0; save number to R3
    AND R2, R2, x0; clear R2
    LEA R0, BUFFER; load the address for the buffer into R0
    STR R2, R0, x0; clear first part of buffer
    STR R2, R0, x1; clear second part of buffer
    STR R2, R0, x2; clear third part of buffer
    STR R2, R0, x3; clear forth part of buffer
    ADD R0, R3, x0; move input to R0
    LD R2, SAVER2; load old register value for R2
    LD R3, SAVER3; load old register value for R3
    LD R4, SAVER4; load old register value for R4
    LD R5, SAVER5; load old register value for R5
    LD R6, SAVER6; load old register value for R6
    LD R7, SAVER7; load old register value for R7
    BR FINISH; go to end of subroutine

SAVER2 .FILL x0; location that R2 is saved to
SAVER3 .FILL x0; location that R3 is saved to
SAVER4 .FILL x0; location that R4 is saved to
SAVER5 .FILL x0; location that R5 is saved to
SAVER6 .FILL x0; location that R6 is saved to
SAVER7 .FILL x0; location that R7 is saved to

READ .FILL x4000; memory location for the read subroutine
STRING2NUM .FILL x4200; memory location for the string2num subroutine

BUFFER .BLKW x4; placeholder for a number string that is up to four digits long
POSTBUFFER .BLKW x2; used to ensure values after buffer are not cleared
SIZE .FILL x4; the size of the buffer is 4 memory spaces

FINISH
    RET

.END
