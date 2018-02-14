#!/bin/bash
set -x

make codegen

for i in `seq 1 9`;
do
    bin/codegen test/test0${i}.ir > test/test0${i}.asm
done

for i in `seq 0 1`;
do
    bin/codegen test/test1${i}.ir > test/test1${i}.asm
done

for i in `seq 1 5`;
do
    bin/codegen test/error${i}.ir > test/error${i}.asm
done

make clean
