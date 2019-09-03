import sys
i = sys.argv[1]
k = 0
for j in range(0, len(i), 2):
	k += int(i[j:j+2], 16)
k = k%0x100
if k == 0:
	print("OK")
else:
	print(f"ERROR, need {format((0x100-k), '02X')}")