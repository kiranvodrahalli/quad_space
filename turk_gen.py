# Kiran Vodrahalli
# Independent Work
# generate Mech Turk stuff

from home_path import path 
from home_path import path_ending as pe 


nc_list = path + "IW_code" + pe + "99_nouncompounds.txt"

ncs = []
with open(nc_list, 'r') as f:
	for line in f:
		line = line.strip()
		ncs.append(line)

pairs = [] 

for i in range(0, len(ncs)):
	for j in range(i+1, len(ncs)):
		pairs.append((ncs[i], ncs[j]))

def build_csv():
	file_str = "noun_compound1, noun_compound2\n"
	for nc_pair in pairs:
		a, b = nc_pair
		file_str += a + "," + b + "\n"
	with open(path + "mech_turk_inputs" + pe + "ncs.csv", 'w') as f:
		f.write(file_str)


# older versions, don't use
'''
def build_csv():
	# a HIT has 10 noun compound PAIRS
	# thus a total of 20 noun compounds
	# thus we need 20 vars per HIT
	first_line = ""
	for i in range(0, 20):
		first_line += "nc" + str(i) + "a," + "nc" + str(i) + "b,"
	# each variable name is like nc1a, nc1b (we will compare ia to ib)
	file_str = ""
	line_count = 0
	for (nc_a, nc_b) in pairs:
		if line_count < 20:
			file_str += nc_a + "," + nc_b + ","
			line_count += 2
		else:
			file_str += "\n"
			file_str += nc_a + "," + nc_b + ","
			line_count = 2
	total_file = first_line + "\n" + file_str
	with open("ncs.csv", 'w') as f:
		f.write(total_file)
'''
'''
def build_csv():
	# a HIT has 9 noun compound pairs
	# each will be its own var
	first_line = ""
	for i in range(0, 9):
		first_line += "nc_pair" + str(i) + ","
	file_str = ""
	line_count = 0
	for nc_pair in pairs:
		if line_count < 9:
			file_str += str(nc_pair) + ","
			line_count += 1
		else:
			file_str += "\n" + str(nc_pair) + ","
			line_count = 1
	total_file = first_line + "\n" + file_str
	with open("ncs.csv", 'w') as f:
		f.write(total_file)
'''



