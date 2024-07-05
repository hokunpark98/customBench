#!/bin/bash

cd /home/dnc/master/customBench/service/a
docker build -t hokunpark/paper2:serviceA2 .
docker push hokunpark/paper2:serviceA2

cd /home/dnc/master/customBench/service/b
docker build -t hokunpark/paper2:serviceB2 .
docker push hokunpark/paper2:serviceB2


cd /home/dnc/master/customBench/service/c
docker build -t hokunpark/paper2:serviceC2 .
docker push hokunpark/paper2:serviceC2


cd /home/dnc/master/customBench/service/d
docker build -t hokunpark/paper2:serviceD2 .
docker push hokunpark/paper2:serviceD2

cd /home/dnc/master/customBench/service/e
docker build -t hokunpark/paper2:serviceE2 .
docker push hokunpark/paper2:serviceE2