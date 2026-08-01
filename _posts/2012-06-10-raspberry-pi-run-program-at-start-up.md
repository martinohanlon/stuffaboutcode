---
title: 'Raspberry Pi - run program at start-up'
date: 2012-06-10 20:44:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/06/raspberry-pi-run-program-at-start-up.html
---

Anyway, I wanted to get my Raspberry Pi to start [no-ip dynamic dns service](http://www.no-ip.com/) when it started-up, so I wouldn't have to remember to start it every time it was powered up. For details on how to [install no-ip on the Pi](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-access-from-internet-using.html), see this [post](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-access-from-internet-using.html).

There are loads of ways of running a command at start-up in Linux but my favoured approach is to create an initialisation script in /etc/init.d and register it using update-rc.d. This way the application is started and stopped automatically when the system boots / shutdowns.

**Create script in /etc/init.d**

```bash
sudo nano /etc/init.d/NameOfYourScript
```

The following is an example based on starting up the no-ip service \[/usr/local/bin/noip\], but change the name of the script and the command to start and stop it and it would work for any command.

```yaml
#! /bin/sh
# /etc/init.d/noip

### BEGIN INIT INFO
# Provides:          noip
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       A simple script from
```

[`www.stuffaboutcode.com`](http://www.stuffaboutcode.com/)

```bash
 which will start / stop a program a boot / shutdown.
### END INIT INFO
# If you want a command to always run, put it here
# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting noip"
    # run application you want to start
    /usr/local/bin/noip2
    ;;
  stop)
    echo "Stopping noip"
    # kill application you want to stop
    killall noip2
    ;;
  *)
    echo "Usage: /etc/init.d/noip {start|stop}"
    exit 1
    ;;
esac

exit 0
```

Warning

- its important you test your script first and make sure it doesn't need a user to provide a response, press "y" or similar, because you may find it hangs the raspberry pi on boot waiting for a user (who's not there) to do something!

**Make script executable**

```bash
sudo chmod 755 /etc/init.d/NameOfYourScript
```

**Test starting the program**

```bash
sudo /etc/init.d/NameOfYourScript start
```

**Test stopping the program**

```bash
sudo /etc/init.d/NameOfYourScript stop
```

**Register script to be run at start-up**
 To register your script to be run at start-up and shutdown, run the following command:

```bash
sudo update-rc.d NameOfYourScript defaults
```

Note - The header at the start is to make the script LSB compliant and provides details about the start up script and you should only need to change the name. If you want to know more about creating LSB scripts for managing services, see [http://wiki.debian.org/LSBInitScripts](http://wiki.debian.org/LSBInitScripts)

If you ever want to remove the script from start-up, run the following command:

```bash
sudo update-rc.d -f NameOfYourScript remove
```
