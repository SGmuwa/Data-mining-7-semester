#!/bin/bash
rm output.log
echo Task 1 >> output.log
echo 1 | python3 treesTask.py >> output.log
for var in 2 3 4 5 6 7
do echo Task $var >> output.log
echo $var | python3 treesTask.py -q >> output.log
done