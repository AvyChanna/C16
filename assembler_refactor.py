import argparse
import json
import re
import sys
import pprint
import ast

class Assembler:
	opcodes = None
	regex = None
	asm = None
	parsed_line = None
	symbols = None
	hexcodes = None
	hexline = None
	def __init__(self, opcodes, regex, asm):
		self.opcodes = opcodes
		self.regex = regex
		self.asm = asm
		# self.asm = []
		self.parsed_line = []
		self.symbols = {}
		self.hexcodes = {}
		self.hexline = []
	def __repr__(self):
		s = {}
		# s["opcodes"] = self.opcodes
		s["regex"] = self.regex.pattern
		s["asm"] = self.asm
		s["parsed_line"] = self.parsed_line
		s["symbols"] = self.symbols
		s["hexline"] = self.hexline
		return json.dumps(s,  indent = "\t", ensure_ascii=False)
	def pass1(self):
		org = 0
		for i, line in enumerate(self.asm, 1):
			stripped_line = line.strip()
			a = self.regex.match(line)
			if a is None:
				print(f"Error at line{i}: Syntax Error")
				print(stripped_line)
				exit()
			label = a.group("label")
			opc = a.group("opc")
			op1 = a.group("op1")
			op2 = a.group("op2")
			if opc is not None:
				opc = opc.lower()
			if op1 is None:
				opno = 0
			elif op2 is None:
				opno = 1
			else:
				opno = 2
			if label is None and opc is None:
				continue

			if label is not None:
				if label in self.symbols:
					print(f"Error at line {i}: Address of {label} already declared to be {self.symbols[label]}")
					print(stripped_line)
					exit()
				if opc is not None and opc == "equ":
					if opno != 1:
						print(f"Error at line {i}: \"EQU\" needs exactly 1 operand")
						print(stripped_line)
						exit()
					temp_hex = self.parse_number(op1)
					if temp_hex is None or temp_hex < 0 or temp_hex > 0xFFFF:
						print(f"Error at line {i}: Value of operand {label} is invalid")
						print(stripped_line)
						exit()
					self.symbols[label] = temp_hex
				elif opc is not None and opc == "org":
					if opno != 1:
						print(f"Error at line {i}: \"ORG\" needs exactly 1 operand")
						print(stripped_line)
						exit()
					temp_hex = self.parse_number(op1)
					if temp_hex is None or temp_hex < 0 or temp_hex >0xFFFF:
						print(f"Error at line {i}: Value of operand {op1} is invalid")
						print(stripped_line)
						exit()
					self.symbols[label] = temp_hex
					org = temp_hex
				else:
					self.symbols[label] = org
			if opc is not None:
				if opc != "org" and opc != "equ":
					tup = (i, org, opc, opno, op1, op2, stripped_line)
					self.parsed_line.append(tup)
				if opc in self.opcodes:
					org += self.opcodes[opc]["size"]
				elif opc == "org":
					if label is None:
						if opno != 1:
							print(f"Error at line {i}: \"ORG\" needs exactly 1 operand")
							print(stripped_line)
							exit()
						temp_hex = self.parse_number(op1)
						if temp_hex is None or temp_hex < 0 or temp_hex >0xFFFF:
							print(f"Error at line {i}: Value of operand {label} is invalid")
							print(stripped_line)
							exit()
						org = temp_hex
				elif opc == "equ":
					if label is None:
						print(f"Error at line {i}, \"EQU\" does not have any label to associate value to")
						print(stripped_line)
						exit()
				else:
					print(f"Error at line {i}: Unknown opcode {opc}")
					print(stripped_line)
					exit()
	def parse_number(self, string):
		s = string.upper()
		if s[0]<"0" or s[0]>"9":
			return None
		if s.endswith("H"):
			try:
				i = int(s[:-1], 16)
				return i
			except:
				return None
		elif s.endswith("D"):
			try:
				i = int(s[:-1], 10)
				return i
			except:
				return None
		elif s.endswith("O"):
			try:
				i = int(s[:-1], 8)
				return i
			except:
				return None
		elif s.endswith("B"):
			try:
				i = int(s[:-1], 2)
				return i
			except:
				return None
		else:
			try:
				i = int(s, 10)
				return i
			except:
				return None
	def pass2(self):
		for i, adr, opc, opno, op1, op2, line in self.parsed_line:
			if opc not in self.opcodes:
				print(f"Error at line {i}: Unknown opcode {opc})")
				print(line)
				exit()
			temp = self.opcodes[opc]
			no = temp["no"]
			lst = temp["list"]
			op1type = temp["op1type"]
			op2type = temp["op2type"]
			if opno != no:
				print(f"Error at line {i}: \"{opc.upper()}\" needs exactly {no} operand(s)")
				print(line)
				exit()

			if op1type is None and op2type is None:
				self.hexcodes[adr] = lst[0]["val"]
			elif op1type is not None and op2type is None:
				if op1type == "reg":
					op1 = op1.lower()
					for d in lst:
						reg = d["op1"]
						val = d["val"]
						if reg == op1:
							break
					self.hexcodes[adr] = val
				elif op1type == "8bit":
					op1 = op1.lower()
					temp_hex = self.parse_number(op1)
					if temp_hex is None or temp_hex < 0 or temp_hex > 0xFF:
						print(f"Error at line {i}: Value of operand {op1} is invalid")
						print(line)
						exit()
					self.hexcodes[adr] = lst[0]["val"]
					self.hexcodes[adr+1] = temp_hex
				elif op1type == "16bit":
					temp_hex = self.parse_number(op1)
					if temp_hex is None:
						if op1 in self.symbols:
							temp_hex = self.symbols[op1]
						else:
							print(f"Error at line {i}: Value of operand {op1} is invalid")
							print(line)
							exit()
					elif temp_hex < 0 or temp_hex > 0xFFFF:
						print(f"Error at line {i}: Value of operand {op1} is invalid")
						print(line)
						exit()
					else:
						temp_hex = temp_hex
					self.hexcodes[adr] = lst[0]["val"]
					self.hexcodes[adr+1] = temp_hex % 0x100
					self.hexcodes[adr+2] = temp_hex >> 8
			elif op1type is not None and op2type is not None:
				if op2type == "reg":
					op1 = op1.lower()
					op2 = op2.lower()
					found = False
					for d in lst:
						o1 = d["op1"]
						o2 = d["op2"]
						val = d["val"]
						if o1 == op1 and o2 == op2:
							found = True
							break
					if found:
						self.hexcodes[adr] = val
					else:
						print(f"Error at line {i}: Value of operands {op1}, {op2} is invalid")
						print(line)
						exit()
				elif op2type == "8bit":
					op1 = op1.lower()
					op2 = op2.lower()
					found = False
					for d in lst:
						o1 = d["op1"]
						val = d["val"]
						if o1 == op1:
							found = True
							break
					if found:
						temp_hex = self.parse_number(op2)
						if temp_hex is None or temp_hex < 0 or temp_hex > 0xFF:
							print(f"Error at line {i}: Value of 2nd operand {op2} is invalid")
							print(line)
							exit()
						self.hexcodes[adr] = val
						self.hexcodes[adr+1] = temp_hex
					else:
						print(f"Error at line {i}: Value of operands {op1}, {op2} is invalid")
						print(line)
						exit()
				elif op2type == "16bit":
					op1 = op1.lower()
					found = False
					for d in lst:
						o1 = d["op1"]
						val = d["val"]
						if o1 == op1:
							found = True
							break
					if found:
						temp_hex = self.parse_number(op2)
						if temp_hex is None:
							# print(op2)
							if op2 in self.symbols:
								temp_hex = self.symbols[op2]
								# print("sym=",temp_hex[2:4])
							else:
								print(f"Error at line {i}: Value of operand {op1} is invalid")
								print(line)
								exit()
						elif temp_hex < 0 or temp_hex > 0xFFFF:
							print(f"Error at line {i}: Value of operands {op1}, {op2} is invalid")
							print(line)
							exit()
						self.hexcodes[adr] = val
						self.hexcodes[adr+1] = temp_hex % 0x100
						self.hexcodes[adr+2] = temp_hex >> 8

					else:
						print(f"Error at line {i}: Value of operands {op1}, {op2} is invalid")
						print(line)
						exit()
	def to_hexline(self):
		curr_addr = 0
		start_addr = 0
		curr_hex = None
		curr_sum = None
		length = 0
		self.hexline = []
		# tpl = (length, start_addr, string)
		for addr, hexx in sorted(self.hexcodes.items()):
			if length == 0:
				start_addr = addr
				curr_addr = addr
				curr_hex = format(hexx, "02X")
				curr_sum = hexx
				length = 1
			elif curr_addr+1 == addr and length < 0x10:
				curr_addr += 1
				curr_hex = curr_hex + format(hexx, "02X")
				curr_sum += hexx
				length += 1
			else:
				length_hex = format(length, "02X")
				start_addr_hex = format(start_addr%0xFFFF, "04X")
				sum_mod_0x100 = (curr_sum+length+start_addr+(start_addr>>8)) % 0x100
				checksum_hex = format((0x100 - sum_mod_0x100), "02X")
				tpl = ":" + length_hex + start_addr_hex + "00" + curr_hex + checksum_hex
				self.hexline.append(tpl)
				start_addr = addr
				curr_addr = addr
				curr_hex = format(hexx, "02X")
				curr_sum = hexx
				length = 1
		if length != 0:
			length_hex = format(length, "02X")
			start_addr_hex = format(start_addr%0xFFFF, "04X")
			sum_mod_0x100 = (curr_sum+length+start_addr+(start_addr>>8)) % 0x100
			checksum_hex = format((0x100 - sum_mod_0x100), "02X")
			tpl = ":" + length_hex + start_addr_hex + "00" + curr_hex + checksum_hex
			self.hexline.append(tpl)
		dummy_addr = (start_addr+length)%0xFFFF
		dummy_addr_hex = format(dummy_addr, "04X")
		dummy_sum_mod_0x100 = (start_addr+2+(start_addr>>8)) % 0x100
		dummy_checksum_hex = format( 0x100 - dummy_sum_mod_0x100, "02X")
		tpl = ":00" + dummy_addr_hex + "01" + dummy_checksum_hex
		self.hexline.append(tpl)

def main(opcodes, asmfile, hexfile):
	if opcodes is None:
		opc = json.loads('{"aci":{"list":[{"val":206}],"no":1,"op1type":"8bit","op2type":null,"size":2},"adc":{"list":[{"op1":"b","val":136},{"op1":"c","val":137},{"op1":"d","val":138},{"op1":"e","val":139},{"op1":"h","val":140},{"op1":"l","val":141},{"op1":"m","val":142},{"op1":"a","val":143}],"no":1,"op1type":"reg","op2type":null,"size":1},"add":{"list":[{"op1":"b","val":128},{"op1":"c","val":129},{"op1":"d","val":130},{"op1":"e","val":131},{"op1":"h","val":132},{"op1":"l","val":133},{"op1":"m","val":134},{"op1":"a","val":135}],"no":1,"op1type":"reg","op2type":null,"size":1},"adi":{"list":[{"val":198}],"no":1,"op1type":"8bit","op2type":null,"size":2},"ana":{"list":[{"op1":"b","val":160},{"op1":"c","val":161},{"op1":"d","val":162},{"op1":"e","val":163},{"op1":"h","val":164},{"op1":"l","val":165},{"op1":"m","val":166},{"op1":"a","val":167}],"no":1,"op1type":"reg","op2type":null,"size":1},"ani":{"list":[{"val":230}],"no":1,"op1type":"8bit","op2type":null,"size":2},"call":{"list":[{"val":205}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cc":{"list":[{"val":220}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cm":{"list":[{"val":252}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cma":{"list":[{"val":47}],"no":0,"op1type":null,"op2type":null,"size":1},"cmc":{"list":[{"val":63}],"no":0,"op1type":null,"op2type":null,"size":1},"cmp":{"list":[{"op1":"b","val":184},{"op1":"c","val":185},{"op1":"d","val":186},{"op1":"e","val":187},{"op1":"h","val":188},{"op1":"l","val":189},{"op1":"m","val":190},{"op1":"a","val":191}],"no":1,"op1type":"reg","op2type":null,"size":1},"cnc":{"list":[{"val":212}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cnz":{"list":[{"val":196}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cp":{"list":[{"val":244}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cpe":{"list":[{"val":236}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cpi":{"list":[{"val":254}],"no":1,"op1type":"8bit","op2type":null,"size":2},"cpo":{"list":[{"val":228}],"no":1,"op1type":"16bit","op2type":null,"size":3},"cz":{"list":[{"val":204}],"no":1,"op1type":"16bit","op2type":null,"size":3},"daa":{"list":[{"val":39}],"no":0,"op1type":null,"op2type":null,"size":1},"dad":{"list":[{"op1":"b","val":9},{"op1":"d","val":25},{"op1":"h","val":41},{"op1":"sp","val":57}],"no":1,"op1type":"reg","op2type":null,"size":1},"dcr":{"list":[{"op1":"b","val":5},{"op1":"c","val":13},{"op1":"d","val":21},{"op1":"e","val":29},{"op1":"h","val":37},{"op1":"l","val":45},{"op1":"m","val":53},{"op1":"a","val":61}],"no":1,"op1type":"reg","op2type":null,"size":1},"dcx":{"list":[{"op1":"b","val":11},{"op1":"d","val":27},{"op1":"h","val":43},{"op1":"sp","val":59}],"no":1,"op1type":"reg","op2type":null,"size":1},"di":{"list":[{"val":243}],"no":0,"op1type":null,"op2type":null,"size":1},"ei":{"list":[{"val":251}],"no":0,"op1type":null,"op2type":null,"size":1},"hlt":{"list":[{"val":118}],"no":0,"op1type":null,"op2type":null,"size":1},"in":{"list":[{"val":219}],"no":1,"op1type":"8bit","op2type":null,"size":2},"inr":{"list":[{"op1":"b","val":4},{"op1":"c","val":12},{"op1":"d","val":20},{"op1":"e","val":28},{"op1":"h","val":36},{"op1":"l","val":44},{"op1":"m","val":52},{"op1":"a","val":60}],"no":1,"op1type":"reg","op2type":null,"size":1},"inx":{"list":[{"op1":"b","val":3},{"op1":"d","val":19},{"op1":"h","val":35},{"op1":"sp","val":51}],"no":1,"op1type":"reg","op2type":null,"size":1},"jc":{"list":[{"val":218}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jm":{"list":[{"val":250}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jmp":{"list":[{"val":195}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jnc":{"list":[{"val":210}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jnz":{"list":[{"val":194}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jp":{"list":[{"val":242}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jpe":{"list":[{"val":234}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jpo":{"list":[{"val":226}],"no":1,"op1type":"16bit","op2type":null,"size":3},"jz":{"list":[{"val":202}],"no":1,"op1type":"16bit","op2type":null,"size":3},"lda":{"list":[{"val":58}],"no":1,"op1type":"16bit","op2type":null,"size":3},"ldax":{"list":[{"op1":"b","val":10},{"op1":"d","val":26}],"no":1,"op1type":"reg","op2type":null,"size":1},"lhld":{"list":[{"val":42}],"no":1,"op1type":"16bit","op2type":null,"size":3},"lxi":{"list":[{"op1":"b","val":1},{"op1":"d","op2":"16bit","val":17},{"op1":"h","op2":"16bit","val":33},{"op1":"sp","op2":"16bit","val":49}],"no":2,"op1type":"reg","op2type":"16bit","size":3},"mov":{"list":[{"op1":"b","op2":"b","val":64},{"op1":"b","op2":"c","val":65},{"op1":"b","op2":"d","val":66},{"op1":"b","op2":"e","val":67},{"op1":"b","op2":"h","val":68},{"op1":"b","op2":"l","val":69},{"op1":"b","op2":"m","val":70},{"op1":"b","op2":"a","val":71},{"op1":"c","op2":"b","val":72},{"op1":"c","op2":"c","val":73},{"op1":"c","op2":"d","val":74},{"op1":"c","op2":"e","val":75},{"op1":"c","op2":"h","val":76},{"op1":"c","op2":"l","val":77},{"op1":"c","op2":"m","val":78},{"op1":"c","op2":"a","val":79},{"op1":"d","op2":"b","val":80},{"op1":"d","op2":"c","val":81},{"op1":"d","op2":"d","val":82},{"op1":"d","op2":"e","val":83},{"op1":"d","op2":"h","val":84},{"op1":"d","op2":"l","val":85},{"op1":"d","op2":"m","val":86},{"op1":"d","op2":"a","val":87},{"op1":"e","op2":"b","val":88},{"op1":"e","op2":"c","val":89},{"op1":"e","op2":"d","val":90},{"op1":"e","op2":"e","val":91},{"op1":"e","op2":"h","val":92},{"op1":"e","op2":"l","val":93},{"op1":"e","op2":"m","val":94},{"op1":"e","op2":"a","val":95},{"op1":"h","op2":"b","val":96},{"op1":"h","op2":"c","val":97},{"op1":"h","op2":"d","val":98},{"op1":"h","op2":"e","val":99},{"op1":"h","op2":"h","val":100},{"op1":"h","op2":"l","val":101},{"op1":"h","op2":"m","val":102},{"op1":"h","op2":"a","val":103},{"op1":"l","op2":"b","val":104},{"op1":"l","op2":"c","val":105},{"op1":"l","op2":"d","val":106},{"op1":"l","op2":"e","val":107},{"op1":"l","op2":"h","val":108},{"op1":"l","op2":"l","val":109},{"op1":"l","op2":"m","val":110},{"op1":"l","op2":"a","val":111},{"op1":"m","op2":"b","val":112},{"op1":"m","op2":"c","val":113},{"op1":"m","op2":"d","val":114},{"op1":"m","op2":"e","val":115},{"op1":"m","op2":"h","val":116},{"op1":"m","op2":"l","val":117},{"op1":"m","op2":"a","val":119},{"op1":"a","op2":"b","val":120},{"op1":"a","op2":"c","val":121},{"op1":"a","op2":"d","val":122},{"op1":"a","op2":"e","val":123},{"op1":"a","op2":"h","val":124},{"op1":"a","op2":"l","val":125},{"op1":"a","op2":"m","val":126},{"op1":"a","op2":"a","val":127}],"no":2,"op1type":"reg","op2type":"reg","size":1},"mvi":{"list":[{"op1":"b","val":6},{"op1":"c","op2":"8bit","val":14},{"op1":"d","op2":"8bit","val":22},{"op1":"e","op2":"8bit","val":30},{"op1":"h","op2":"8bit","val":38},{"op1":"l","op2":"8bit","val":46},{"op1":"m","op2":"8bit","val":54},{"op1":"a","op2":"8bit","val":62}],"no":2,"op1type":"reg","op2type":"8bit","size":2},"nop":{"list":[{"val":0}],"no":0,"op1type":null,"op2type":null,"size":1},"ora":{"list":[{"op1":"b","val":176},{"op1":"c","val":177},{"op1":"d","val":178},{"op1":"e","val":179},{"op1":"h","val":180},{"op1":"l","val":181},{"op1":"m","val":182},{"op1":"a","val":183}],"no":1,"op1type":"reg","op2type":null,"size":1},"ori":{"list":[{"val":246}],"no":1,"op1type":"8bit","op2type":null,"size":2},"out":{"list":[{"val":211}],"no":1,"op1type":"8bit","op2type":null,"size":2},"pchl":{"list":[{"val":233}],"no":0,"op1type":null,"op2type":null,"size":1},"pop":{"list":[{"op1":"b","val":193},{"op1":"h","val":225},{"op1":"psw","val":241}],"no":1,"op1type":"reg","op2type":null,"size":1},"popd":{"list":[{"val":209}],"no":0,"op1type":null,"op2type":null,"size":1},"push":{"list":[{"op1":"b","val":197},{"op1":"d","val":213},{"op1":"h","val":229},{"op1":"psw","val":245}],"no":1,"op1type":"reg","op2type":null,"size":1},"ral":{"list":[{"val":23}],"no":0,"op1type":null,"op2type":null,"size":1},"rar":{"list":[{"val":31}],"no":0,"op1type":null,"op2type":null,"size":1},"rc":{"list":[{"val":216}],"no":0,"op1type":null,"op2type":null,"size":1},"ret":{"list":[{"val":201}],"no":0,"op1type":null,"op2type":null,"size":1},"rim":{"list":[{"val":32}],"no":0,"op1type":null,"op2type":null,"size":1},"rlc":{"list":[{"val":7}],"no":0,"op1type":null,"op2type":null,"size":1},"rm":{"list":[{"val":248}],"no":0,"op1type":null,"op2type":null,"size":1},"rnc":{"list":[{"val":208}],"no":0,"op1type":null,"op2type":null,"size":1},"rnz":{"list":[{"val":192}],"no":0,"op1type":null,"op2type":null,"size":1},"rp":{"list":[{"val":240}],"no":0,"op1type":null,"op2type":null,"size":1},"rpe":{"list":[{"val":232}],"no":0,"op1type":null,"op2type":null,"size":1},"rpo":{"list":[{"val":224}],"no":0,"op1type":null,"op2type":null,"size":1},"rrc":{"list":[{"val":15}],"no":0,"op1type":null,"op2type":null,"size":1},"rst":{"list":[{"op1":"0","val":199},{"op1":"1","val":207},{"op1":"2","val":215},{"op1":"3","val":223},{"op1":"4","val":231},{"op1":"5","val":239},{"op1":"6","val":247},{"op1":"7","val":255}],"no":1,"op1type":"reg","op2type":null,"size":1},"rz":{"list":[{"val":200}],"no":0,"op1type":null,"op2type":null,"size":1},"sbb":{"list":[{"op1":"b","val":152},{"op1":"c","val":153},{"op1":"d","val":154},{"op1":"e","val":155},{"op1":"h","val":156},{"op1":"l","val":157},{"op1":"m","val":158},{"op1":"a","val":159}],"no":1,"op1type":"reg","op2type":null,"size":1},"sbi":{"list":[{"val":222}],"no":1,"op1type":"8bit","op2type":null,"size":2},"shld":{"list":[{"val":34}],"no":1,"op1type":"16bit","op2type":null,"size":3},"sim":{"list":[{"val":48}],"no":0,"op1type":null,"op2type":null,"size":1},"sphl":{"list":[{"val":249}],"no":0,"op1type":null,"op2type":null,"size":1},"sta":{"list":[{"val":50}],"no":1,"op1type":"16bit","op2type":null,"size":3},"stax":{"list":[{"op1":"b","val":2},{"op1":"d","val":18}],"no":1,"op1type":"reg","op2type":null,"size":1},"stc":{"list":[{"val":55}],"no":0,"op1type":null,"op2type":null,"size":1},"sub":{"list":[{"op1":"b","val":144},{"op1":"c","val":145},{"op1":"d","val":146},{"op1":"e","val":147},{"op1":"h","val":148},{"op1":"l","val":149},{"op1":"m","val":150},{"op1":"a","val":151}],"no":1,"op1type":"reg","op2type":null,"size":1},"sui":{"list":[{"val":214}],"no":1,"op1type":"8bit","op2type":null,"size":2},"xchg":{"list":[{"val":235}],"no":0,"op1type":null,"op2type":null,"size":1},"xra":{"list":[{"op1":"b","val":168},{"op1":"c","val":169},{"op1":"d","val":170},{"op1":"e","val":171},{"op1":"h","val":172},{"op1":"l","val":173},{"op1":"m","val":174},{"op1":"a","val":175}],"no":1,"op1type":"reg","op2type":null,"size":1},"xri":{"list":[{"val":238}],"no":1,"op1type":"8bit","op2type":null,"size":2},"xthl":{"list":[{"val":227}],"no":0,"op1type":null,"op2type":null,"size":1}}')
	else:
		try:
			with open(opcodes, "r") as f:
				opc = json.load(f)
		except IOError:
			print(f"[IOERROR] Could not read opcodes from file:{opcodes}")
			exit()
		except json.JSONDecodeError:
			print(f"[JSONDecodeError]Bad file content in: {opcodes}")
	try:
		with open(asmfile, "r") as f:
			asm = f.readlines()
	except IOError:
		print(f"[IOERROR] Could not read asm from file:{asmfile}")
		exit()
	regex = re.compile(r"^[ \t]*((?P<label>([a-zA-Z_][a-zA-Z0-9_]*))[ \t]*:)?[ \t]*((?P<opc>[a-zA-Z]+)[ \t]*([ \t](?P<op1>[a-zA-Z0-9_]+)([ \t]*\,[ \t]*(?P<op2>[a-zA-Z0-9_]+))?)?)?[ \t\f\v]*(;.*)?$")
	a = Assembler(opc, regex, asm)
	a.pass1()
	a.pass2()
	a.to_hexline()
	print("================= Symbols =================")
	for key, value in sorted(a.symbols.items()):
		print(f"label[\"{key}\"] = {format(value, '02X')}")
	print("================= HexFile =================")
	for i in a.hexline:
		print(i)
	try:
		if hexfile is not None:
			with open(hexfile, "w") as f:
				for i in a.hexline:
					f.write(i+"\n")
	except IOError:
		print(f"[IOERROR] Could not write to: {hexfile}")


if __name__ == "__main__":
	opcodes = ""
	asmfile = ""
	parser = argparse.ArgumentParser(description="8085 Assembler for MPS 85-3", allow_abbrev=True)
	# parser.add_argument("-l", "--listfile", type=str, nargs="?",  help="Location of lst file", dest="lstfile", default=argparse.SUPPRESS)
	parser.add_argument("-o", "--output", type=str, nargs="?",  help="Location of hex file", dest="hexfile", default=argparse.SUPPRESS)
	parser.add_argument("-c", "--code", type=str,  help="Location of opcodes file", dest="opcodes", default=argparse.SUPPRESS)
	parser.add_argument("-i", "--input", type=str, help="Location of asm file", dest="asmfile",  required=True)
	args = parser.parse_args()
	if not args.__contains__("opcodes"):
		args.__setattr__("opcodes", None)
	if not args.asmfile.endswith(".asm"):
		print("[WARNING]	ASM file does NOT have .asm extension. Continuing anyways ......")
	if args.__contains__("hexfile"):
		if args.hexfile is None:
			args.hexfile = args.asmfile.rsplit(".", 1)[0]+".hex"
		print(f"[INFO]	Saving hexcode to file: {args.hexfile}")
	else:
		args.hexfile = None
	main(args.opcodes, args.asmfile, args.hexfile)
	
	