---
title: 'Raspberry Pi - Python - Installing modules'
date: 2012-10-17 20:42:00 +01:00
tags: [python, raspberry-pi]
redirect_from:
  - /2012/10/raspberry-pi-python-installing-modules.html
---

Anyway, I've been using python on my raspberry pi to create some small programs and I've got a little more advanced I wanted to use some open source modules written by others. Most python modules will come with a setup program, setup.py, which when called should install the module in the right place and configure the environment.

However whenever I tried to do this, I was presented with the following error:

```text
"No module named setuptools"
```

Some google searches and a read of the python.org website told be I was missing the python setup tools component [distribute](http://pypi.python.org/pypi/distribute).

So the first step is to install distribute:

```bash
mkdir python-setuptools
cd python-setuptools
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python
```

Then download whatever module you need and run the setup.py program using the command:

```bash
sudo python setup.py install
```

Then with a bit of luck, your module should be setup and ready to use.
