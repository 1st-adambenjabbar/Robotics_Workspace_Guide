#!/bin/bash
echo "Checking WSL Environment..."
lsb_release -a
echo "Checking Python version..."
python3 --version
echo "Checking Git installation..."
git --version
echo "WSL Setup verified!"
