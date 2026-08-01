---
title: 'Slack command line stream'
date: 2017-11-15 20:56:00 +00:00
tags: [python, social-networking]
redirect_from:
  - /2017/11/slack-command-line-stream.html
---

I thought a Slack console might be useful, a very simple client I could display on an always on screen, so I did some experimenting with the [Slack Developer Kit for Python](https://slackapi.github.io/python-slackclient/) and made a super simple command line program which streams messages.

It is most definitely a starting point rather than a finished solution, but someone might find it useful.

![](/assets/img/2017/11/commandlineslack2.png)

**Setup** (assuming you are using a Raspberry Pi / Linux computer, although it will work on Windows as well).

1. Generate a [security token](https://api.slack.com/custom-integrations/legacy-tokens) for the slack group you want to stream.

2. Create an environment variable SLACK_API_TOKEN and put your security token in it.

Edit /etc/profile adding the export to the bottom:

```bash
sudo nano /etc/profile
export SLACK_API_TOKEN=[my super long token]
```

3. Install slackclient and colorama using pip:

```bash
sudo pip3 install colorama
sudo pip3 install slackclient
```

4. Download the [slack_stream.py from gist](https://gist.github.com/martinohanlon/477b6ea4c3bdc679ddff92dfc3bff4a7):

```bash
wget https://gist.githubusercontent.com/martinohanlon/477b6ea4c3bdc679ddff92dfc3bff4a7/raw/8ec39d08a9501b25d381ac3b008e9cf7be92377a/slack_streamer.py
```

5. Run it:

```bash
python3 slack_streamer.py
```
