#!/bin/bash

variables=$1
clauses=$2
len_clauses=$3
num_cnf=$4

i=0
while [ $i -lt $num_cnf ]; do
	./rnd-cnf-gen.py $variables $clauses $len_clauses $(($RANDOM%99)) > cnf-$1-$2-$3-$i.cnf
	res=$(./minisat cnf-$1-$2-$3-$i.cnf)
	echo $res

	while [ $res = UNSATISFIABLE ]; do
		./rnd-cnf-gen.py $variables $clauses $len_clauses $(($RANDOM%99)) > cnf-$1-$2-$3-$i.cnf
		res=$(./minisat cnf-$1-$2-$3-$i.cnf)
		echo $res
	done
	i=$(expr $i + 1)
	echo
done