set datafile sep comma
set key left Left reverse autotitle columnhead samplen 1

rl = 7.33
set yran [0:4]
set xran [0.2:1.8]
set xtics 0.5,0.5
set ytics 0,1
set ylabel 'Delay'
set xlabel 'Throughput'
set out 'sharing_benefit.png'
set term pngcairo
plot 'KeepCurrentRideDelay/results.csv' \
     us ($4/$2*rl):($3 == 1 ? ($5 + $7)/rl : 1/0) pt 9 ps 1.5 title '1 seat',\
     '' us ($4/$2*rl):($3 == 2 ? ($5 + $7)/rl : 1/0) \
     pt 5 ps 1.5 title '2 seats',\
     '' us ($4/$2*rl):($3 == 3 ? ($5 + $7)/rl : 1/0) \
     pt 7 ps 1.5 title '3 seats'
