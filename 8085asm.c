#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<stddef.h>
#include<ctype.h>

typedef struct
{
unsigned char value;
unsigned short int addr;
}Mem;

Mem mem[65535];

typedef struct
{
 char nome[100];
 int value;
} Symbol;

Symbol labels[250];
typedef struct
{
  int  opc;
  char men[5];
  int  nargs;
  char arg1[4];
  char arg2[4];
  int  uargs;		/* 0 - no arg, 1 - byte, 2 - word */
} Opcode;





static Opcode opcode[] = {
  /*
   * { 0x, "", 0, " ", " " },
   */
  {0xCE, "ACI", 0, " ", " ", 1},
  {0x8F, "ADC", 1, "A", " ", 0},
  {0x88, "ADC", 1, "B", " ", 0},
  {0x89, "ADC", 1, "C", " ", 0},
  {0x8A, "ADC", 1, "D", " ", 0},
  {0x8B, "ADC", 1, "E", " ", 0},
  {0x8C, "ADC", 1, "H", " ", 0},
  {0x8D, "ADC", 1, "L", " ", 0},
  {0x8E, "ADC", 1, "M", " ", 0},
  {0x87, "ADD", 1, "A", " ", 0},
  {0x80, "ADD", 1, "B", " ", 0},
  {0x81, "ADD", 1, "C", " ", 0},
  {0x82, "ADD", 1, "D", " ", 0},
  {0x83, "ADD", 1, "E", " ", 0},
  {0x84, "ADD", 1, "H", " ", 0},
  {0x85, "ADD", 1, "L", " ", 0},
  {0x86, "ADD", 1, "M", " ", 0},
  {0xC6, "ADI", 0, " ", " ", 1},
  {0xA7, "ANA", 1, "A", " ", 0},
  {0xA0, "ANA", 1, "B", " ", 0},
  {0xA1, "ANA", 1, "C", " ", 0},
  {0xA2, "ANA", 1, "D", " ", 0},
  {0xA3, "ANA", 1, "E", " ", 0},
  {0xA4, "ANA", 1, "H", " ", 0},
  {0xA5, "ANA", 1, "L", " ", 0},
  {0xA6, "ANA", 1, "M", " ", 0},
  {0xE6, "ANI", 0, "M", " ", 1},
  {0xCD, "CALL", 0, "M", " ", 2},
  {0xDC, "CC", 0, "M", " ", 2},
  {0xFC, "CM", 0, "M", " ", 2},
  {0x2F, "CMA", 0, "M", " ", 0},
  {0x3F, "CMC", 0, "M", " ", 0},
  {0xBF, "CMP", 1, "A", " ", 0},
  {0xB8, "CMP", 1, "B", " ", 0},
  {0xB9, "CMP", 1, "C", " ", 0},
  {0xBA, "CMP", 1, "D", " ", 0},
  {0xBB, "CMP", 1, "E", " ", 0},
  {0xBC, "CMP", 1, "H", " ", 0},
  {0xBD, "CMP", 1, "L", " ", 0},
  {0xBE, "CMP", 1, "M", " ", 0},
  {0xD4, "CNC", 0, "M", " ", 2},
  {0xC4, "CNZ", 0, "M", " ", 2},
  {0xF4, "CP", 0, "M", " ", 2},
  {0xEC, "CPE", 0, "M", " ", 2},
  {0xFE, "CPI", 0, "M", " ", 1},
  {0xE4, "CPO", 0, "M", " ", 2},
  {0xCC, "CZ", 0, "M", " ", 2},
  {0x27, "DAA", 0, "M", " ", 0},
  {0x09, "DAD", 1, "B", " ", 0},
  {0x19, "DAD", 1, "D", " ", 0},
  {0x29, "DAD", 1, "H", " ", 0},
  {0x39, "DAD", 1, "SP", " ", 0},
  {0x3D, "DCR", 1, "A", " ", 0},
  {0x05, "DCR", 1, "B", " ", 0},
  {0x0D, "DCR", 1, "C", " ", 0},
  {0x15, "DCR", 1, "D", " ", 0},
  {0x1D, "DCR", 1, "E", " ", 0},
  {0x25, "DCR", 1, "H", " ", 0},
  {0x2D, "DCR", 1, "L", " ", 0},
  {0x35, "DCR", 1, "M", " ", 0},
  {0x0B, "DCX", 1, "B", " ", 0},
  {0x1B, "DCX", 1, "D", " ", 0},
  {0x2B, "DCX", 1, "H", " ", 0},
  {0x3B, "DCX", 1, "SP", " ", 0},
  {0xF3, "DI", 0, " ", " ", 0},
  {0xFB, "EI", 0, " ", " ", 0},
  {0x76, "HLT", 0, " ", " ", 0},
  {0xDB, "IN", 0, " ", " ", 1},
  {0x3C, "INR", 1, "A", " ", 0},
  {0x04, "INR", 1, "B", " ", 0},
  {0x0C, "INR", 1, "C", " ", 0},
  {0x14, "INR", 1, "D", " ", 0},
  {0x1C, "INR", 1, "E", " ", 0},
  {0x24, "INR", 1, "H", " ", 0},
  {0x2C, "INR", 1, "L", " ", 0},
  {0x34, "INR", 1, "M", " ", 0},
  {0x03, "INX", 1, "B", " ", 0},
  {0x13, "INX", 1, "D", " ", 0},
  {0x23, "INX", 1, "H", " ", 0},
  {0x33, "INX", 1, "SP", " ", 0},
  {0xDA, "JC", 0, " ", " ", 2},
  {0xFA, "JM", 0, " ", " ", 2},
  {0xC3, "JMP", 0, " ", " ", 2},
  {0xD2, "JNC", 0, " ", " ", 2},
  {0xC2, "JNZ", 0, " ", " ", 2},
  {0xF2, "JP", 0, " ", " ", 2},
  {0xEA, "JPE", 0, " ", " ", 2},
  {0xE2, "JPO", 0, " ", " ", 2},
  {0xCA, "JZ", 0, " ", " ", 2},
  {0x3A, "LDA", 0, " ", " ", 2},
  {0x0A, "LDAX", 1, "B", " ", 0},
  {0x1A, "LDAX", 1, "D", " ", 0},
  {0x2A, "LHLD", 0, " ", " ", 2},
  {0x01, "LXI", 1, "B", " ", 2},
  {0x11, "LXI", 1, "D", " ", 2},
  {0x21, "LXI", 1, "H", " ", 2},
  {0x31, "LXI", 1, "SP", " ", 2},
  {0x7F, "MOV", 2, "A", "A", 0},
  {0x78, "MOV", 2, "A", "B", 0},
  {0x79, "MOV", 2, "A", "C", 0},
  {0x7A, "MOV", 2, "A", "D", 0},
  {0x7B, "MOV", 2, "A", "E", 0},
  {0x7C, "MOV", 2, "A", "H", 0},
  {0x7D, "MOV", 2, "A", "L", 0},
  {0x7E, "MOV", 2, "A", "M", 0},
  {0x47, "MOV", 2, "B", "A", 0},
  {0x40, "MOV", 2, "B", "B", 0},
  {0x41, "MOV", 2, "B", "C", 0},
  {0x42, "MOV", 2, "B", "D", 0},
  {0x43, "MOV", 2, "B", "E", 0},
  {0x44, "MOV", 2, "B", "H", 0},
  {0x45, "MOV", 2, "B", "L", 0},
  {0x46, "MOV", 2, "B", "M", 0},
  {0x4F, "MOV", 2, "C", "A", 0},
  {0x48, "MOV", 2, "C", "B", 0},
  {0x49, "MOV", 2, "C", "C", 0},
  {0x4A, "MOV", 2, "C", "D", 0},
  {0x4B, "MOV", 2, "C", "E", 0},
  {0x4C, "MOV", 2, "C", "H", 0},
  {0x4D, "MOV", 2, "C", "L", 0},
  {0x4E, "MOV", 2, "C", "M", 0},
  {0x57, "MOV", 2, "D", "A", 0},
  {0x50, "MOV", 2, "D", "B", 0},
  {0x51, "MOV", 2, "D", "C", 0},
  {0x52, "MOV", 2, "D", "D", 0},
  {0x53, "MOV", 2, "D", "E", 0},
  {0x54, "MOV", 2, "D", "H", 0},
  {0x55, "MOV", 2, "D", "L", 0},
  {0x56, "MOV", 2, "D", "M", 0},
  {0x5F, "MOV", 2, "E", "A", 0},
  {0x58, "MOV", 2, "E", "B", 0},
  {0x59, "MOV", 2, "E", "C", 0},
  {0x5A, "MOV", 2, "E", "D", 0},
  {0x5B, "MOV", 2, "E", "E", 0},
  {0x5C, "MOV", 2, "E", "H", 0},
  {0x5D, "MOV", 2, "E", "L", 0},
  {0x5E, "MOV", 2, "E", "M", 0},
  {0x67, "MOV", 2, "H", "A", 0},
  {0x60, "MOV", 2, "H", "B", 0},
  {0x61, "MOV", 2, "H", "C", 0},
  {0x62, "MOV", 2, "H", "D", 0},
  {0x63, "MOV", 2, "H", "E", 0},
  {0x64, "MOV", 2, "H", "H", 0},
  {0x65, "MOV", 2, "H", "L", 0},
  {0x66, "MOV", 2, "H", "M", 0},
  {0x6F, "MOV", 2, "L", "A", 0},
  {0x68, "MOV", 2, "L", "B", 0},
  {0x69, "MOV", 2, "L", "C", 0},
  {0x6A, "MOV", 2, "L", "D", 0},
  {0x6B, "MOV", 2, "L", "E", 0},
  {0x6C, "MOV", 2, "L", "H", 0},
  {0x6D, "MOV", 2, "L", "L", 0},
  {0x6E, "MOV", 2, "L", "M", 0},
  {0x77, "MOV", 2, "M", "A", 0},
  {0x70, "MOV", 2, "M", "B", 0},
  {0x71, "MOV", 2, "M", "C", 0},
  {0x72, "MOV", 2, "M", "D", 0},
  {0x73, "MOV", 2, "M", "E", 0},
  {0x74, "MOV", 2, "M", "H", 0},
  {0x75, "MOV", 2, "M", "L", 0},
  {0x3E, "MVI", 1, "A", " ", 1},
  {0x06, "MVI", 1, "B", " ", 1},
  {0x0E, "MVI", 1, "C", " ", 1},
  {0x16, "MVI", 1, "D", " ", 1},
  {0x1E, "MVI", 1, "E", " ", 1},
  {0x26, "MVI", 1, "H", " ", 1},
  {0x2E, "MVI", 1, "L", " ", 1},
  {0x36, "MVI", 1, "M", " ", 1},
  {0x00, "NOP", 0, "M", " ", 0},
  {0xB7, "ORA", 1, "A", " ", 0},
  {0xB0, "ORA", 1, "B", " ", 0},
  {0xB1, "ORA", 1, "C", " ", 0},
  {0xB2, "ORA", 1, "D", " ", 0},
  {0xB3, "ORA", 1, "E", " ", 0},
  {0xB4, "ORA", 1, "H", " ", 0},
  {0xB5, "ORA", 1, "L", " ", 0},
  {0xB6, "ORA", 1, "M", " ", 0},
  {0xF6, "ORI", 0, "M", " ", 1},
  {0xD3, "OUT", 0, "M", " ", 1},
  {0xE9, "PCHL", 0, "M", " ", 0},
  {0xC0, "RNZ", 0, "B", " ", 0},
  {0xC1, "POP", 1, "B", " ", 0},
  {0xD1, "POP", 1, "D", " ", 0},
  {0xE1, "POP", 1, "H", " ", 0},
  {0xF1, "POP", 1, "PSW", " ", 0},
  {0xC5, "PUSH", 1, "B", " ", 0},
  {0xD5, "PUSH", 1, "D", " ", 0},
  {0xE5, "PUSH", 1, "H", " ", 0},
  {0xF5, "PUSH", 1, "PSW", " ", 0},
  {0x17, "RAL", 0, "M", " ", 0},
  {0x1F, "RAR", 0, "M", " ", 0},
  {0xD8, "RC", 0, "M", " ", 0},
  {0xC9, "RET", 0, "M", " ", 0},
  {0x20, "RIM", 0, "M", " ", 0},
  {0x07, "RLC", 0, "M", " ", 0},
  {0xF8, "RM", 0, "M", " ", 0},
  {0xD0, "RNC", 0, "M", " ", 0},
  {0xF0, "RP", 0, "M", " ", 0},
  {0xE8, "RPE", 0, "M", " ", 0},
  {0xE0, "RPO", 0, "M", " ", 0},
  {0x0F, "RRC", 0, "M", " ", 0},
  {0xC7, "RST", 1, "0", " ", 0},
  {0xCF, "RST", 1, "1", " ", 0},
  {0xD7, "RST", 1, "2", " ", 0},
  {0xDF, "RST", 1, "3", " ", 0},
  {0xE7, "RST", 1, "4", " ", 0},
  {0xEF, "RST", 1, "5", " ", 0},
  {0xF7, "RST", 1, "6", " ", 0},
  {0xFF, "RST", 1, "7", " ", 0},
  {0xC8, "RZ", 0, " ", " ", 0},
  {0x9F, "SBB", 1, "A", " ", 0},
  {0x98, "SBB", 1, "B", " ", 0},
  {0x99, "SBB", 1, "C", " ", 0},
  {0x9A, "SBB", 1, "D", " ", 0},
  {0x9B, "SBB", 1, "E", " ", 0},
  {0x9C, "SBB", 1, "H", " ", 0},
  {0x9D, "SBB", 1, "L", " ", 0},
  {0x9E, "SBB", 1, "M", " ", 0},
  {0xDE, "SBI", 0, "M", " ", 1},
  {0x22, "SHLD", 0, "M", " ", 2},
  {0x30, "SIM", 0, "M", " ", 0},
  {0xF9, "SPHL", 0, "M", " ", 0},
  {0x32, "STA", 0, "M", " ", 2},
  {0x02, "STAX", 1, "B", " ", 0},
  {0x12, "STAX", 1, "D", " ", 0},
  {0x37, "STC", 0, "M", " ", 0},
  {0x97, "SUB", 1, "A", " ", 0},
  {0x90, "SUB", 1, "B", " ", 0},
  {0x91, "SUB", 1, "C", " ", 0},
  {0x92, "SUB", 1, "D", " ", 0},
  {0x93, "SUB", 1, "E", " ", 0},
  {0x94, "SUB", 1, "H", " ", 0},
  {0x95, "SUB", 1, "L", " ", 0},
  {0x96, "SUB", 1, "M", " ", 0},
  {0xD6, "SUI", 0, "M", " ", 1},
  {0xEB, "XCHG", 0, "M", " ", 0},
  {0xAF, "XRA", 1, "A", " ", 0},
  {0xA8, "XRA", 1, "B", " ", 0},
  {0xA9, "XRA", 1, "C", " ", 0},
  {0xAA, "XRA", 1, "D", " ", 0},
  {0xAB, "XRA", 1, "E", " ", 0},
  {0xAC, "XRA", 1, "H", " ", 0},
  {0xAD, "XRA", 1, "L", " ", 0},
  {0xAE, "XRA", 1, "M", " ", 0},
  {0xEE, "XRI", 0, "M", " ", 1},
  {0xE3, "XTHL", 0, "M", " ", 0},
  {0xFF, "ENDO", 0, " ", " ", 0}
};


int lc=1;

void
ucase (char * str)
{
int i;
  if(str != NULL)
  {
    for(i=0; i < strlen(str);i++)
      str[i]=toupper(str[i]);
  }
}

int addr=0;
int addi=0;
unsigned char prg[256];
int labelsc=0;
int pass;
int memc;


int
parsearg(char* arg, char * line)
{
int i;

  if(arg == NULL)
  {
    printf("Error at line %i !!!!\n%s\n",lc+1,line);
    exit(-1);
  };

  for(i=0;i<labelsc;i++)
  {
     if(strcmp(labels[i].nome,arg)==0)
     {
       return labels[i].value;
     };
  }

  sscanf(arg,"%X",&i);
  return i;
};


int parse(char * line)
{
int i=0;
int t;
char sline[256];
char* label;
char* men;
char* arg1;
char* arg2;
int err;

  addi=0;
  if((line[0]=='\n')||(line[0]=='\r')) return 0;

  label= strtok(line,";\n\r");
  strcpy(sline,label);
  if((sline[0] != ' ')&&(sline[0]!='\t'))
  {
    label= strtok(sline," \t:,\n");
    men= strtok(NULL," \t:,\n");

    if(pass==1)
    {
      //printf("label=%s  %04X\n",label,addr);
      ucase(label);
      strcpy(labels[labelsc].nome,label);
      labels[labelsc].value=addr;
      labelsc++;
    }

  }
  else
  {
    label=NULL;
    men= strtok(sline," \t:,\n");
  }

 if(men == NULL)return 0;
 arg1= strtok(NULL," \t:,\n");
 arg2= strtok(NULL," \t:,\n");

 ucase(men);
 if(arg1 != NULL) ucase(arg1);
 if(arg2 != NULL) ucase(arg2);
 //printf("addr=%04X label=%s  opcode=%s  arg1=%s  arg2=%s\n",addr,label,men,arg1,arg2);


  err=0;
//busca opcodes
  do
  {
      if(strcmp(opcode[i].men,men)==0)
      {
        if(opcode[i].nargs == 0)
	{
          addi=opcode[i].uargs;
          prg[0]=opcode[i].opc;
	  if(pass ==2)
          switch(addi)
	  {
	    case 0:
              return 1;
	    case 1:
              prg[1]=parsearg(arg1,line);
              return 1;
            case 2:
	      t=parsearg(arg1,line);
	      prg[1]=0x00FF&t;
	      prg[2]=(0xFF00&t)>>8;
              return 1;
	  }
          return 1;
	}
	else
	{
	  if(arg1 == NULL)
	  {
            printf("Error at line %i !!!!\n%s\n",lc,line);
            exit(-1);
	  }
          if(strcmp(opcode[i].arg1,arg1)==0)
	  {
	    if(opcode[i].nargs == 1)
	    {
	      addi=opcode[i].uargs;
	      prg[0]=opcode[i].opc;
	      if(pass ==2)
              switch(addi)
	      {
	       case 0:
                  return 1;
	        case 1:
                  prg[1]=parsearg(arg2,line);
                  return 1;
                case 2:
	          t=parsearg(arg2,line);
	          prg[1]=0x00FF&t;
	          prg[2]=(0xFF00&t)>>8;
                  return 1;
	      }
	      return 1;
	    }
	    else
	    {
	      if(strcmp(opcode[i].arg2,arg2)==0)
	      {
	        addi=opcode[i].uargs;
		prg[0]=opcode[i].opc;
	        return 1;
	      }
	    }
	  }
	  err=1;
	}
      }
      else
      {
        if(err)
	{
          printf("Error at line %i !!!!\n%s\n",lc,line);
          exit(-1);
	}
      }
  }
  while(strcmp(opcode[i++].men,"ENDO") != 0);

//busca pseudo
    if(strcmp("ORG",men)==0)
    {
       addr=parsearg(arg1,line);
//       printf("org ===> %04X\n",i);
       return 0;
    };

    if((label != NULL )&&(pass==1))
    {
    if(strcmp("EQU",men) == 0)
    {
      sscanf(arg1,"%x",&i);
      labels[labelsc-1].value=i;
      return 0;
    }
    }

    if(strcmp("DB",men)==0)
    {
      addi=0;
      prg[addi]=parsearg(arg1,line);

      if(arg2 != NULL)
      {
       addi++;
       prg[addi]=parsearg(arg2,line);
      }

      arg1= strtok(NULL," \t:,\n");
      while(arg1 != NULL)
      {
       ucase(arg1);
       addi++;
       prg[addi]=parsearg(arg1,line);
       arg1= strtok(NULL," \t:,\n");
      }


      return 1;
    }

    if(strcmp("DS",men)==0)
    {
       i=parsearg(arg1,line);
      addr+=i;
    }
  return 0;
}

int
main(int argc,char** argv)
{
char fname[256];
char fname2[256];
FILE* fin;
char line[256];
int i;
unsigned char sum;
unsigned char nb;
unsigned short iaddr;
char values[100];
char *fnamep;
FILE *fout;
FILE *fout2;


  if(argc == 2)
  {
    strcpy(fname,argv[1]);
  }
  else
  {
   printf("Enter the file name: ");
   scanf("%s",fname);
   getchar();
  }

  fin=fopen(fname,"r");

  if(!fin)
  {
     printf("Error opening file:%s\n",fname);
     return -1;
  }

  fnamep=strtok(fname,".");

  strcpy(fname2,fnamep);
  strcat(fname2,".map");
  fout=fopen(fname2,"w");

  if(!fout)
  {
     printf("Error opening file:%s\n",fname2);
     return -1;
  }

  pass=1;
  while(fgets(line,256,fin))
  {

     if(line[0] == ';')
     {
//       printf("%5i                           ==> %s",lc,line);
     }
     else
     {

       if(parse(line))
       {
//         printf("%5i     %04X    ",lc,addr);
//	 for(i=0;i<=addi;i++)printf("%02X ",prg[i]);
//	 for(i=addi;i<3;i++)printf("   ");
//	 printf("  ==> %s\n",line);
         addr+=1+addi;
       }
       else
       {
//         if(strtok(line,"\n\r") != NULL)
//           printf("%5i                           ==> %s\n",lc,line);
//         else
//           printf("%5i                           ==> \n",lc);
       }
     }

     lc++;
  }

  rewind(fin);
  pass=2;
  addr=0;
  lc=0;
  while(fgets(line,256,fin))
  {

     if(line[0] == ';')
     {
       fprintf(fout,"%5i                           ==> %s",lc,line);
     }
     else
     {

       if(parse(line))
       {
         fprintf(fout,"%5i     %04X    ",lc,addr);
	 for(i=0;i<=addi;i++)
	 {
	   fprintf(fout,"%02X ",prg[i]);
	   mem[memc].addr=addr+i;
	   mem[memc].value=prg[i];
	   memc++;
	}
	 for(i=addi;i<3;i++)fprintf(fout,"   ");
	 fprintf(fout,"  ==> %s\n",line);
         addr+=1+addi;
       }
       else
       {
         if(strtok(line,"\n\r") != NULL)
           fprintf(fout,"%5i                           ==> %s\n",lc,line);
         else
           fprintf(fout,"%5i                           ==> \n",lc);
       }
     }

     lc++;
  }

  fprintf(fout,"\n\nSYMBOLIC TABLE:\n\n");
  for(i=0;i<labelsc;i++)
  {
    fprintf(fout," %-10s  %04XH\n",labels[i].nome,labels[i].value);
  }


  fprintf(fout,"\n\nMEMORY = (%i bytes)\n\n",memc);

  printf("\nMEMORY = (%i bytes)\n\n",memc);


  strcpy(fname2,fnamep);
  strcat(fname2,".hex");
  fout2=fopen(fname2,"w");

  if(!fout2)
  {
     printf("Error opening file:%s\n",fname2);
     return -1;
  }

  nb=0;
  sum=0;
  int final = 0;
  for(i=0;i<memc;i++)
  {
  //  printf(" %04XH  %02XH\n",mem[i].addr,mem[i].value);

    if(nb==0)
    {
      iaddr=mem[i].addr;
      sprintf(values,"%02X",mem[i].value);
    }
    else
    {
      sprintf(values,"%s%02X",values,mem[i].value);
    }
    nb++;
    sum+=mem[i].value;
    if((mem[i+1].addr != (mem[i].addr+1))||(nb==16))
    {
      sum+=nb;
      sum+=(iaddr&0x00FF);
      sum+=((iaddr&0xFF00)>>8);

      // printf("sum=%02X %02X %02X\n",sum,~sum,(~sum)+1);
      sum=(~sum)+1;
      fprintf(fout2,":%02X%04X00%s%02X\n",nb,iaddr,values,sum);
      fprintf(fout,":%02X%04X00%s%02X\n",nb,iaddr,values,sum);
      final = nb+iaddr;
      nb=0;
      sum=0;
    }
  }
  sum = (final&0x00FF) + ((final&0xFF00)>>8) + 1;
  sum = (~sum)+1;
  fprintf(fout2,":00%04X01%02X\n", final, sum);
  fprintf(fout,":00%04X01%02X\n", final, sum);

  fclose(fout);
  fclose(fout2);
return 1;
}
