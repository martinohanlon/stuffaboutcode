---
title: 'Get the weather using Python'
date: 2018-06-09 21:58:00 +01:00
tags: [python]
redirect_from:
  - /2018/06/get-weather-using-python.html
---

I recently spent a hour or so hacking a lucky cat so that it would only wave when it was sunny.

> At [@Raspberry_Pi](https://twitter.com/Raspberry_Pi?ref_src=twsrc%5Etfw) 's MakerDay I hacked a lucky cat so it only waves when it's sunny. [pic.twitter.com/JUED5nYadt](https://twitter.com/martinohanlon/status/1005342439874486273)
>
> — Martin O'Hanlon (@martinohanlon) [June 9, 2018](https://twitter.com/martinohanlon/status/1005342439874486273?ref_src=twsrc%5Etfw)

It did this by pulling the weather data from [Open Weather Map](https://openweathermap.org/) using the Python module [pyowm](https://github.com/csparpa/pyowm).

**1.**[Sign up for a free API key in Open Weather Map](https://home.openweathermap.org/users/sign_up).

**2.** Install the pyown Python module, open a **Terminal** or **Command Prompt** and run:

*Windows*

```bash
pip install pyown
```

*Raspberry Pi / Linux*

```bash
sudo pip3 install pyown
```

*MacOS*

```bash
pip3 install pyown
```

**3.** Create a Python program using the following code, inserting your API key:

```python
import pyowm

owm = pyowm.OWM('put api key here')

observation = owm.weather_at_place('Cambridge,GB')
w = observation.get_weather()

clouds = w.get_clouds()
wind = w.get_wind()
humidity = w.get_humidity()
temp = w.get_temperature('celsius')

print("{}, {}, {}, {}".format(clouds, wind, humidity, temp)
```

Note - it can take up to 60 minutes for your API key to be activated.

There is a lot more information which can be pulled back - have a look at the [weather module documentation](https://pyowm.readthedocs.io/en/latest/pyowm.webapi25.html#module-pyowm.webapi25.weather) for more details.
