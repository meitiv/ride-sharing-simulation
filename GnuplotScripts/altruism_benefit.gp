set datafile sep comma
set key left Left reverse autotitle columnhead samplen 1

set yran [0:4]
set xran [0.5:2.25]
set xtics 0.5,0.5
set ytics 0,1
set ylabel 'Delay'
set xlabel 'Throughput'
# set out 'network_effect.png'
# set term pngcairo

rl = 7.33
nv = 20
plot 'MinimizeTotalDelay/results.csv' \
     us ($4/$2*rl):($3 == 3 && $2 == nv ? ($5 + $7)/rl : 1/0) \
     pt 5 ps 1.5 title 'Altruistic', \
     'KeepCurrentRideDelay/results.csv' \
     us ($4/$2*rl):($3 == 3 && $2 == nv ? ($5 + $7)/rl : 1/0) \
     pt 7 ps 1.5 title 'Selfish'
     