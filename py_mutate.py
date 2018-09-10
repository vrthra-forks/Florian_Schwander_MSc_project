#!/usr/bin/env python3
import sys
sys.path.append('.')
from generate_reject import main as gen
from find_mutation_lines import main as mutate
from check_results import main as check

def main(argv):
    # The argument order is: program path, number of pychains iterations, binary in- and output file
    if len(argv) < 2:
        raise SystemExit("Please specifiy a .py file as argument.")
    prog = argv[1] if argv[1].endswith(".py") else argv[1] + ".py"
    iterations = 1000 if len(argv) < 3 else argv[2]
    binfile = "rejected_" + prog[prog.rfind("/")+1:prog.rfind(".py")] + ".bin" if len(argv) < 4 else argv[3]
    print("Generating input for:", prog, "...")
    gen([None, prog, iterations, binfile])
    print("Starting mutation...", prog)
    mutate([None, prog, binfile])
    print("Testing result integrity...")
    check([None, prog, binfile])

if __name__ == "__main__":
    print("The argument order is: program path [, number of pychains iterations, binary in- and output file]")
    main(sys.argv)