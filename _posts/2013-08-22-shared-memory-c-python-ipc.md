---
title: 'Shared Memory C & Python IPC'
date: 2013-08-22 22:23:00 +01:00
tags: [c, python]
redirect_from:
  - /2013/08/shared-memory-c-python-ipc.html
---

I had a problem whereby I needed to use a C program to capture video, in this case RaspiVid (the raspberry pi camera capture program), but I wanted to sync the video with data being capture by a Python program; in order to get the sync right I need to grab data about the video capture as it was running.

To do this I had to find a method of doing Inter Process Communication (IPC), very quickly, with a very low performance impact on the C program. I explored several IPC options between C and Python (stdin/stdout, named pipes, tcp, shared memory) and found that using Shared Memory was the only way to deliver the performance I needed.

I pulled together a quick proof of concept to learn the basics.

**C - Writing to Shared Memory**
 I created a C program which writes data into a shared memory segment and then waits (to allow me time to run the python program to read it out). See [http://www.cs.cf.ac.uk/Dave/C/node27.html](http://www.cs.cf.ac.uk/Dave/C/node27.html) for a description of how to use shared memory and this video [http://www.youtube.com/watch?v=QPxcOwMmpnw](http://www.youtube.com/watch?v=QPxcOwMmpnw) for a tutorial.

**shmwriter.c**

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

int main(int argc, const char **argv)
{
   int shmid;
   // give your shared memory an id, anything will do
   key_t key = 123456;
   char *shared_memory;

   // Setup shared memory, 11 is the size
   if ((shmid = shmget(key, 11, IPC_CREAT | 0666)) < 0)
   {
      printf("Error getting shared memory id");
      exit(1);
   }
   // Attached shared memory
   if ((shared_memory = shmat(shmid, NULL, 0)) == (char *) -1)
   {
      printf("Error attaching shared memory id");
      exit(1);
   }
   // copy "hello world" to shared memory
   memcpy(shared_memory, "Hello World", sizeof("Hello World"));
   // sleep so there is enough time to run the reader!
   sleep(10);
   // Detach and remove shared memory
   shmdt(shmid);
   shmctl(shmid, IPC_RMID, NULL);
}
```

Compile using:

```bash
gcc -o shmwriter shmwriter.c
```

**Python - Reading from Shared Memory**
 I found a great module for python, [sysv_ipc](http://semanchuk.com/philip/sysv_ipc/), which greatly simplifies the interaction with shared memory, see [http://semanchuk.com/philip/sysv_ipc/](http://semanchuk.com/philip/sysv_ipc/) for more information, download and install instructions.

**shmreader.py**

```python
import sysv_ipc

# Create shared memory object
memory = sysv_ipc.SharedMemory(123456)

# Read value from shared memory
memory_value = memory.read()

# Find the 'end' of the string and strip
i = memory_value.find('\0')
if i != -1:
    memory_value = memory_value[:i]

print memory_value
```

Run using:

```bash
python shmreader.py
```

You can download the code from github, [https://github.com/martinohanlon/c_python_ipc.git](https://github.com/martinohanlon/c_python_ipc.git).
