#!/bin/bash

# Use: <num-vars> <num-clauses> <clause-length> <num_files> <dst_directory>

variables=$1
clauses=$2
len_clauses=$3
num_cnf=$4
dst_d=$5
seed=0

i=0
while [ $i -lt $num_cnf ]; do
	./rnd-cnf-gen.py $variables $clauses $len_clauses $seed > $dst_d/$i-cnf-$1-$2-$3-$seed.cnf
	res=$(./minisat $dst_d/$i-cnf-$1-$2-$3-$seed.cnf)
	if [[ $res = SATISFIABLE ]]; then
		rm $dst_d/$i-cnf-$1-$2-$3-$seed.cnf
	fi
	echo $res

	while [ $res = SATISFIABLE ]; do
		./rnd-cnf-gen.py $variables $clauses $len_clauses $seed > $dst_d/$i-cnf-$1-$2-$3-$seed.cnf
		res=$(./minisat $dst_d/$i-cnf-$1-$2-$3-$seed.cnf)
		if [[ $res = SATISFIABLE ]]; then
			rm $dst_d/$i-cnf-$1-$2-$3-$seed.cnf
		fi
		echo $res
		seed=$(expr $seed + 1)
	done

	i=$(expr $i + 1)
	seed=$(expr $seed + 1)
	echo
done