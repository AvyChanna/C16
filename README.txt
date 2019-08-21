# C16

8085.tbl contains all mnemonics and their respective hex codes.

For eg, ADC{5B3}^88: means take 1st operand (3 bit) and add it such that leftmost digit of operand comes under 6th digit from the MSB of 88's binary representation.

```
MNEMONIC{START,?,SIZE}^BASE_HEX
```

```
POSITION    =   01234567
88          =   10001000
c(1)        =        001
=============================
ADC C       =   10001001    = 89 (in hex)
=============================
```


Detailed list is available in all_opcodes.txt.

## TODO

-[] Preprocess input for ASM.txt
-[] Make SYM.txt in Pass1
-[] Make OBJ.txt in Pass2
-[] Preety print OBJ.txt to make HEX.txt
