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

## Camera Streaming:

Flask enables streaming of data, including image data, to the browser. Streaming to the browser is unnecessary for image detection, but of course I want to see the baby. Image streaming doesn’t include sound; however, I don’t need sound since the image detection will log if he is awake or asleep.

## Image Detection:

The camera sends video at 30 fps. I’d like to see if the baby moves once per second, so I grab every 30th frame and compare the baby’s position to a frame 29 frames later. If the baby’s position is identical, he did not move. If the position is not identical, I store that the baby has moved at least once. If the baby moves 10 times in one minute, he is considered awake. This does lead to the occasional false positive; however, at higher thresholds, I encountered too many false negatives.


Logo is from:
https://www.iconfinder.com/icons/4751672/baby_feminine_maternity_newborn_infant_pregnancy_icon
Available under: https://creativecommons.org/licenses/by/3.0/
