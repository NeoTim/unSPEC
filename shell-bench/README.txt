I used R for the statistics.  The commands for that look like this:

prelink1noff <- read.csv(file='prelink-1-no-firefox.csv', header=F)
noprelink1noff <- read.csv(file='no-prelink-1-no-firefox.csv', header=F)
t.test(prelink1noff$V1, noprelink1noff$V1)

It turns out that user time is not useful because it's not cumulative (doesn't
include spawned child processes), so I ran the statistics over the first column
only (that's the $V1 business).
