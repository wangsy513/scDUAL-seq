#!/usr/bin/env python3

import sys
import getopt

opt = {}

try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["read=", "tsv=", "qual=", "help"])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o in ("-h", "--help"):
        print("Usage: python script.py --read read.txt --tsv sample.tsv --qual 27")
        sys.exit()
    else:
        opt[o.lstrip("-")] = a

if not opt:
    print("Usage: python script.py --read read.txt --tsv sample.tsv --qual 27")
    sys.exit()

in_file = opt.get("tsv")
qual = int(opt.get("qual"))

T_to_A = 0
T_to_C = 0
T_to_G = 0
T_to_T = 0
total_T = 0

A_to_A = 0
A_to_C = 0
A_to_G = 0
A_to_T = 0
total_A = 0

G_to_A = 0
G_to_C = 0
G_to_G = 0
G_to_T = 0
total_G = 0

C_to_A = 0
C_to_C = 0
C_to_G = 0
C_to_T = 0
total_C = 0

in2 = opt.get("read")
hash_dict = {}
with open(in2) as f:
    for line in f:
        columns = line.strip().split(",")
        key, value = columns[0], columns[1]
        hash_dict[key] = value

with open(in_file) as f, open(f"{in_file}_q{qual}_gene_anno_stat.txt", "w") as out:
    for line in f:
        line = line.strip()
        array = line.split("\t")
        if array[0] in hash_dict:
            strand = hash_dict[array[0]]
            if ord(array[5]) - 33 > qual:
                if strand == '-':  # negative strand
                    if "A" in array[7]:
                        total_T += 1
                        T_to_T += 1 if "A" in array[4] else 0
                        T_to_G += 1 if "C" in array[4] else 0
                        T_to_C += 1 if "G" in array[4] else 0
                        T_to_A += 1 if "T" in array[4] else 0
                    elif "G" in array[7]:
                        total_C += 1
                        C_to_T += 1 if "A" in array[4] else 0
                        C_to_G += 1 if "C" in array[4] else 0
                        C_to_C += 1 if "G" in array[4] else 0
                        C_to_A += 1 if "T" in array[4] else 0
                    elif "C" in array[7]:
                        total_G += 1
                        G_to_T += 1 if "A" in array[4] else 0
                        G_to_G += 1 if "C" in array[4] else 0
                        G_to_C += 1 if "G" in array[4] else 0
                        G_to_A += 1 if "T" in array[4] else 0
                    elif "T" in array[7]:
                        total_A += 1
                        A_to_T += 1 if "A" in array[4] else 0
                        A_to_G += 1 if "C" in array[4] else 0
                        A_to_C += 1 if "G" in array[4] else 0
                        A_to_A += 1 if "T" in array[4] else 0
                else:  # positive strand
                    if "A" in array[7]:
                        total_A += 1
                        A_to_T += 1 if "T" in array[4] else 0
                        A_to_G += 1 if "G" in array[4] else 0
                        A_to_C += 1 if "C" in array[4] else 0
                        A_to_A += 1 if "A" in array[4] else 0
                    elif "G" in array[7]:
                        total_G += 1
                        G_to_T += 1 if "T" in array[4] else 0
                        G_to_G += 1 if "G" in array[4] else 0
                        G_to_C += 1 if "C" in array[4] else 0
                        G_to_A += 1 if "A" in array[4] else 0
                    elif "C" in array[7]:
                        total_C += 1
                        C_to_T += 1 if "T" in array[4] else 0
                        C_to_G += 1 if "G" in array[4] else 0
                        C_to_C += 1 if "C" in array[4] else 0
                        C_to_A += 1 if "A" in array[4] else 0
                    elif "T" in array[7]:
                        total_T += 1
                        T_to_T += 1 if "T" in array[4] else 0
                        T_to_G += 1 if "G" in array[4] else 0
                        T_to_C += 1 if "C" in array[4] else 0
                        T_to_A += 1 if "A" in array[4] else 0

    out.write(f"total_T\t{total_T}\n")
    out.write(f"T_to_A\t{T_to_A}\n")
    out.write(f"T_to_G\t{T_to_G}\n")
    out.write(f"T_to_C\t{T_to_C}\n")
    out.write(f"T_to_T\t{T_to_T}\n")

    out.write(f"total_A\t{total_A}\n")
    out.write(f"A_to_A\t{A_to_A}\n")
    out.write(f"A_to_G\t{A_to_G}\n")
    out.write(f"A_to_C\t{A_to_C}\n")
    out.write(f"A_to_T\t{A_to_T}\n")

    out.write(f"total_G\t{total_G}\n")
    out.write(f"G_to_A\t{G_to_A}\n")
    out.write(f"G_to_G\t{G_to_G}\n")
    out.write(f"G_to_C\t{G_to_C}\n")
    out.write(f"G_to_T\t{G_to_T}\n")

    out.write(f"total_C\t{total_C}\n")
    out.write(f"C_to_A\t{C_to_A}\n")
    out.write(f"C_to_G\t{C_to_G}\n")
    out.write(f"C_to_C\t{C_to_C}\n")
    out.write(f"C_to_T\t{C_to_T}\n")
    out
    