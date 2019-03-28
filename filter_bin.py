import sys
import imp
import pickle

if __name__ == "__main__":
	prog = sys.argv[1]
	orig = sys.argv[2]
	res = sys.argv[3]
	valid = []
	rej = []
	bin_arr = pickle.load(open(orig, "rb"))
	_mod = imp.load_source('mymod', prog)
	for (_, vs) in bin_arr:
		try:
			_mod.main(vs)
		except:
			pass
		else:
			valid.append(vs)

	if not valid:
		raise SystemExit("No valid inputs for:", prog, "in:", orig)

	for (ivs, _) in bin_arr:
		try:
			_mod.main(ivs)
		except:
			rej.append(ivs)

	if not rej:
		raise SystemExit("No invalid inputs for:", prog, "in:", orig)

	final_len = min(len(valid), len(rej))
	valid = valid[:final_len]
	rej = rej[:final_len]
	combined = []
	for i in range(final_len):
		combined.append((rej[i], valid[i]))

	with open(res, mode="wb") as pick_file:
		pickle.dump(combined, pick_file)