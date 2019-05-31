# DeepInstinct - Code Challenge

An automation program that gets a path to a report file in the following format:

**[Date] [Time] [Guard #X] [Action (begin shift\falls asleep\wakes up)]**

The program finds which guard is most likely to fall asleep (the guard that has slept most minutes in total) and the time he most likely to be asleep.

In order to execute the whole test set, run this command:

> python -m unittest main.py


A brief explenation of my solution:
For every guard detected in the log file, there is a related dictionary contains the sum of the sleeping times of that guard and an array of 60 cells (cell per minute because a guard can be asleep between 00:00-01:00). each time a sleeping time is detected, the relevant cells are filled (like a counter).
So eventually, we can find the most sleepy guard (according to its sum of sleep time) and for that guard, find the cell (the minute) he was sleeping the most number of times.
