#!/bin/bash

g++ pcap.cpp -lpcap
./a.out $@ > packet_details.txt

echo "Check packet_details.txt in your folder"
