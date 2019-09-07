l1:org 1234h
rz			;	c8
rst 1		;	cf
dad b		;	09
mov c, m	;	4e
pop psw		; f1
mvi a, 45h	;	3e 45
adi 60d		;	c6 3c
lxi b, l1	;	01 34 12
lxi h,7890h	;	21 90 78
sta l1		; 32 34 12
sta 1234h	; 32 34 12
inx b		; 03
; For comparision-> C8 CF 09 4E F1 3E 45 C6 3C 01 34 12 21 90 78 32 34 12 32 34 12 03