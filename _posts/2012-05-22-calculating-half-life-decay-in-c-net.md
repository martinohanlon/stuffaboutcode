---
title: 'Calculating half-life decay in c# .net'
date: 2012-05-22 22:15:00 +01:00
tags: [csharp, dotnet]
redirect_from:
  - /2012/05/calculating-half-life-decay-in-c-net.html
---

Anyway, Im working on a new project which has a game and scoring element to it and I wanted to use a scoring system that would exponentially reduce based on how quickly the user was to respond to an action. E.g. If you respond really quick you will get a high score, but only a short time later you are going to get a much lower score, but as time goes on the score decreases slow and slower.

So I remembered back to my physic days and remembered half-life decay of radio-active material and I thought, I can do that; write a c# function which starts with an initial number, a start date time, an end date time and a half life time.

A google search revealed loads of examples of the equations needed, see [http://lpc1.clpccd.cc.ca.us/lpc/hanna/HistoricalGeology/HalfLifeEquations.pdf](http://lpc1.clpccd.cc.ca.us/lpc/hanna/HistoricalGeology/HalfLifeEquations.pdf) for some more thorough examples and descriptions!

Now my maths isn't great, but even I was amazed by how long it took me to write the following function, particularly as it looks so simple now its completed... Definitely a case of its easy when you know how and all that!

```csharp
    public static double calculateHalfLifeDecay(int startingValue, DateTime startTime, DateTime endTime, int halfLifeInSecs)
        {
            TimeSpan timeSince = endTime.Subtract(startTime);

            double value = startingValue / Math.Pow(2, (timeSince.TotalSeconds / halfLifeInSecs));
            if (value < 1) value += 1;
            value = Math.Round(value);

            return value;
        }
```

The function also includes some additional logic to ensure the value is never less than 1 and to round it.
