##Runs the interface and will save a plot of the angle against time
##First run chmod +x /path/to/run.sh
##To run in terminal ./run.sh


set -e

echo python2.7 new_interface.py $1
python2.7 new_interface.py $1

echo cd Analysis
cd Analysis

echo python2.7 plot_angle.py $1
python2.7 plot_angle.py $1