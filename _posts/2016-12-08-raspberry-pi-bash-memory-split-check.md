---
title: 'Raspberry Pi - bash memory split check'
date: 2016-12-08 22:43:00 +00:00
tags: [raspberry-pi]
redirect_from:
  - /2016/12/raspberry-pi-bash-memory-split-check.html
---

I needed a bash script which would only launch a program on a Raspberry Pi if there was enough memory dedicated to the GPU.

I pulled this script together which checks to see if there is at least 128 MB dedicated to the GPU before starting the program.

```bash
#!/bin/bash

#check there is enough gpu memory to start
#get the gpu memory and output to a file called gpu_mem
vcgencmd get_mem gpu > gpu_mem
source gpu_mem
#strip last char from the output (i.e. 64M)
gpu=${gpu%?}
if (( $gpu >= 128 )); then
    ./launch_program
else
    echo "The program needs at least 128MB of memory allocated to the GPU"
    echo "Use sudo raspi-config (Advanced Options > Memory Split) to change"
fi
#remove the gpu_mem file
rm gpu_mem
```
