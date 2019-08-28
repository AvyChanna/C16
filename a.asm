; cpu "8085.tbl"
; hof "int8"
; l2555:equ 0FFh; 255
; org 0fffh; 
; l4095:mov a,b
; l4096:mov a,b
; l4099:mov a,b
; labe2l:mov a,b
; labe3l:mov a,b
; labe4l:mov a,b
; mov a,b
; jz 1h
; l9:jz labe2l
l1:
l2:org 0fffh
l3:mov a, b
cpi 11h
mvi a, 02H
cma
hlt
nop
;
; 4095=78=78
; 4096=FE=fe
; 4097=11=11
; 4098=3E=3e
; 4099=02=02
; 4100=2F=2f
; 4101=76=76
; 4102=00=00