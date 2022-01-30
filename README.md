# Smart Baby Monitor

Goal: This application enables parents to watch their baby in real-time, see if they are awake or asleep, and to know exactly when their child went to bed.

## Why make this?
Two Reasons:
1. Keeping track of what time my son finally fell asleep for the night required continuous monitoring of his existing baby monitor.
2. My son started to wake up in the middle of the night. He would play quietly in his crib for sometinmes as long as 45 minutes and then go back to sleep. He would be tired the next day, and we didn't know why.

## What does this application do?
This web application uses OpenCV to determine if a baby is awake or asleep. It also keeps a running log of each time the child wakes up and goes back to bed, enabling you to track your baby's movements.

## How do I run it?
I use a Raspberry Pi 4 with a Camera. The requirements.txt file shows the necessary packages and version number. On your Pi, enter the babyMonitor directory and use "sudo python main.py" to run the app.

Logo is from:
https://www.iconfinder.com/icons/4751672/baby_feminine_maternity_newborn_infant_pregnancy_icon
Available under: https://creativecommons.org/licenses/by/3.0/
