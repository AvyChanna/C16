# C16

## TBL, OPCODES, MNEMONICS..... the usual stuff

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

## THE GREAT HEX FORMAT

After further reading and frantic research, I've found the mysteries of c16.

c16 uses a hex format to output data.

A normal program would look something like 

```
; DANCE.HEX
:109000003E82D3433E80D340CD3F903E40D340CDBF
:109010003F903E20D340CD3F903E10D340CD3F9077
:109020003E08D340CD3F903E04D340CD3F903E021A
:10903000D340CD3F903E01D340CD3F90C304900E2E
:0D904000FF16FF15C243900DC24190C97686
:00904D0122
```

First 2 Bits = Length of data in this record.

Next 4 bits = Starting Address of record.

Next 2 bits = Record type ( 00 = Data, 01 = End, 02-05 = Not Applicable to us because we have only simple 2 byte memory addressing )

Next n bits = Data (n = value of first 2 bits)

Last 2 bits = Checksum ( Sum previous n bytes, take 2's complement )

So, if you strip first 4 bytes in data records, sum of next all bytes % 100 == 0


Detailed list is available in all_opcodes.txt.

## ROADMAP

### Preprocessing

-[x] Strip all comments
-[x] Tokenize asmfile
-[] Strip lines "CPU '8085.tbl'" and "HOF 'INT8'", because I will be making this specifically for 8085, so dont need these

### Pass 1

-[] Make lst file ( a must for me. Saved me a ton of time )
-[] Make SYMBOL TABLE

### PASS 2

-[] Use SYMBOL TABLE to substitute label values in lst file
-[] Convert everything to hex and pretty-print in hexfile

## Takeaway

Atleast now i would not have to run a shitty DOS program which

- only runs only in 32bit windows ( no fucks given to win 8 & 10, we have to use win7:32bit )
- has to run as administrator ( still don't know why an assembler would need admin privilege )
- Gives error on almost every 8085 asm program ( even the simple ones )

And I may ( "hopefully" ) learn something new. 

