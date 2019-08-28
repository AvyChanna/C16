import json, re

j = json.loads("{}")
m = {}
with open("all_opcodes.txt") as f:
	q = f.readlines()
for l in q:
	l = l.lower()
	l = re.split(r'\s|,',l)
	l = list(filter(None, l))
	size = 1
	val = ""
	operands = 0
	op1 = ""
	op2 = ""
	w=""
	for i, word in enumerate(l):
		
		if i==0:
			size = int(word)
		elif i==1:
			val = int(word, 16)
		elif i==2:
			w = word
		elif i==3:
			op1 = word
			operands = 1
		elif i==4:
			op2 = word
			operands = 2
	# print("i=", i, "w=",w)
	# print(operands, size, op1, op2, val, w, word)
	if val in m:
			continue
	else:
		m[val] = ""
		# print(val)
	if operands==1:
		if w in j:
			j[w]["list"].append({"op1":op1, "val":val})
		else:
			if "bit" in op1:
				j[w] = {"no":operands, "size":size, "op1type":op1, "op2type":None, "list":[ {"val":val} ]}
			
			else:
				j[w] = {"no":operands, "size":size, "op1type":"reg", "op2type":None, "list":[ {"op1":op1,"val":val} ]}
	elif operands==2:
		if  w in j:
			j[w]["list"].append({"op1":op1, "op2":op2, "val":val})
		elif "bit" in op2:
			j[w] = {"no":operands, "size":size, "op1type":"reg", "op2type":op2 , "list":[ {"op1":op1, "val":val} ]}
		else:
			j[w] = {"no":operands, "size":size, "op1type":"reg", "op2type":"reg", "list":[ {"op1":op1, "op2":op2, "val":val} ]}
	else:
		j[w] = {"no":operands, "size":size, "op1type":None, "op2type":None, "list":[ {"val":val} ]}		

# print(j)
with open('opcodes.json', 'w') as fp:
    json.dump(j, fp, ensure_ascii=True, indent=None, separators=(',',':'), sort_keys=True)
with open('opcodes_expanded.json', 'w') as fp:
	json.dump(j, fp, ensure_ascii=True, indent="\t", separators=(', ',':'), sort_keys=True)

