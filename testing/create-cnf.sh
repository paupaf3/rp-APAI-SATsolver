#!/bin/bash

# Use: <num-vars> <num-clauses> <clause-length> <num_files>

variables=$1
clauses=$2
len_clauses=$3
num_cnf=$4
seed=0

i=0
while [ $i -lt $num_cnf ]; do
	./rnd-cnf-gen.py $variables $clauses $len_clauses $seed > $i-cnf-$1-$2-$3-$seed.cnf
	res=$(./minisat $i-cnf-$1-$2-$3-$seed.cnf)
	if [[ $res = UNSATISFIABLE ]]; then
		rm $i-cnf-$1-$2-$3-$seed.cnf
	fi
	echo $res

	while [ $res = UNSATISFIABLE ]; do
		./rnd-cnf-gen.py $variables $clauses $len_clauses $seed > $i-cnf-$1-$2-$3-$seed.cnf
		res=$(./minisat $i-cnf-$1-$2-$3-$seed.cnf)
		if [[ $res = UNSATISFIABLE ]]; then
			rm $i-cnf-$1-$2-$3-$seed.cnf
		fi
		echo $res
		seed=$(expr $seed + 1)
	done

	i=$(expr $i + 1)
	seed=$(expr $seed + 1)
	echo
done