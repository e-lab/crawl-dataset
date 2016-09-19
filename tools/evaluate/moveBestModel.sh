#!bin/bash
echo "Make file $1"
mkdir $1
echo "Moving test.log"
cp test.log $1;
echo "Moving train.log"
cp train.log $1;
echo "Moving $2"
cp $2 $1;
echo "Moving aux.t7"
cp aux.t7 $1
echo "Moving classes.t7"
cp classes.t7 $1
echo "Moving categoris.t7"
cp categories.txt $1;
echo "Moving optimState_.t7"
cp optimState_*.t7 $1;
echo "Moving stat.t7"
cp stat.t7 $1;
