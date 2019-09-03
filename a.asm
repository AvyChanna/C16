; cpu "8085.tbl"
; hof "int8"
; l2555:equ 0ffh; 255
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
l1:			org 1234h
rz;		c8
rst 	1;	cf
	dad  	 	b;	09
mov c        		,	     	 m; 4e
   	   pop psw; f1
mvi a, 45h;	3e 45
			    adi 60d; c6 3c
; org 9000h
	lxi b, l1;	01 34 12
lxi h, 				0000000000000000000000007890h;	21 90 78
sta l1; 32 34 12 [RANDOM COMMENT AHEAD] vpnawevioaw vqiuawlv.sn yuvws yuabv wyqb6vwbywayoqb67vyul sabcw u67vbwayws8ap basyvup87aws iyp78wavbvjiuyp7w8vs jiuawbpbv waiuwbv7u wbv[uia]
sta 1234h; 32 34 12
; org 9500h
inx b; 03                                                   

; For comparision->

; C8 CF 09 4E F1 3E 45 C6 3C 01 34 12 21 90 78 32 34 12 32 34 12 03
; C8CF094EF13E45C63C01341221907832341232341203

; C8
; CF
; 09
; 4E
; F1
; 3E
; 45
; C6
; 3C
; 01
; 34
; 12
; 21
; 90
; 78
; 32
; 34
; 12
; 32
; 34
; 12
; 03


