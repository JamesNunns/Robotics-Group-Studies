##Runs the interface and will save a plot of the angle against time
##First run chmod +x /path/to/run.sh
##To run in terminal ./run.sh


set -e

echo python Interface_2020.py $1
python Interface_2020.py $1

echo cd ../Analysis
cd ../Analysis

echo python3 plot_angle.py $1
python3 plot_angle.py $1