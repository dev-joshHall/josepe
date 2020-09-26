; File name: multiply.asm
; File description: A subroutine that implements integer multiplication
; PARAMETERS: R0 - multiplicand, R1 - multiplier
; RETURN VALUES: R0 - product
; LIMITATIONS: Only works with positive numbers
; ERROR CHECKING: If either multiplicand or multiplier is negative, returns -1
.ORIG x4100

	BR multiply
SaveR1  .FILL #0
SaveR2	.FILL #0
SaveR6	.FILL #0
SaveR7	.FILL #0
ErrorCode   .FILL #-1
multiply
	; save registers and return address
  ST R1, SaveR1
	ST R2, SaveR2
	ST R7, SaveR7
	ADD R2, r0, #0		; copy multiplicand to R2
	BRn error			; check multiplicand < 0
	BRz zero			;
	AND R0, r0, #0		; clear r0 to initialize product
	ADD R1, R1, #0
	BRn error			; check multiplier < 0
	BRz zero
again
	ADD R0, R0, R2		; add multiplicand
	ADD R1, R1, #-1		; count additions
	BRp again			; add again
	BR done
error
	LD r0, ErrorCode	; error code
	BR done
zero
	AND R0, R0, #0		; product is zero
done
	; retrieve registers and return address
	LD R1, SaveR1
	LD R2, SaveR2
	LD R7, SaveR7
	RET

.END
