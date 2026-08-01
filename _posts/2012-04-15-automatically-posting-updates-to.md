---
title: 'Automatically posting updates to Twitter'
date: 2012-04-15 16:10:00 +01:00
tags: [asp, csharp, dotnet, social-networking]
redirect_from:
  - /2012/04/automatically-posting-updates-to.html
---

## Automatic tweets from .net!

Anyway... I wanted to get my website [www.GoOffPiste.com](http://www.gooffpiste.com/) to automatically post updates to twitter because I thought it would be a good way to keep people informed of changes to the site (new articles, videos, that sort of thing) and getting additional links to the website from Twitter is a great tactic for SEO.

### 1. Get Twitterizer

There is a great open source source .net library for interacting with Twitter called [Twitterizer](http://www.twitterizer.net/), so the first thing to do is to head over to [http://www.twitterizer.net/](http://www.twitterizer.net/) and download the [binaries](https://github.com/Twitterizer/Twitterizer/downloads). You are going to need Twitterizer2.dll and Newtonsoft.Json.dll, but put them to the side, as there is something important we need to do first.

### 2. Create a Twitter App

In order for you to post updates to your twitter account you need to create an app in twitter, so goto [http://dev.twitter.com](http://dev.twitter.com/) and sign in with your twitter account. Click on your username on the top right, select my applications and choose create application.

You will need to give your application a name, description, a fully quality URL (e.g. http://www.url.com); the call back url isn't required if you only want to post updates.

Once you've created your application you need to the application type to read & write and then authorize your application (if you authorize your application before changing the type you will only have read-only access)

Goto Settings -> Application Type, change the application type to "Read & Write" and update.

![Change application type](/assets/img/2012/04/test.gooffpiste---twitter-developers---access-rights.png)

Goto Details -> Authorize this application and "create my access token".

![Authorize this application](/assets/img/2012/04/test.gooffpiste---twitter-developers.png---authorize.png)

You have now got 4 really important keys:

- Consumer key
- Consumer secret
- Access token
- Access token secret

These keys allow you to interact with your twitter application (consumer key & consumer secret) and update your twitter account (access token & access token secret), so keep them save as you are going to need them.

### 3. Write some code

Include the Twitterizer dll's (Twitterizer2.dll & Newtonsoft.Json.dll) you downloaded earlier into your .net project.

Create a function to call Twitterizer using your twitter application keys:

```csharp
using Twitterizer;
public class twitterFunctions
{
    public void updateTwitterStatus(string twitterStatusUpdate)
    {
        OAuthTokens tokens = new OAuthTokens();
        tokens.AccessToken = "access token";
        tokens.AccessTokenSecret = "access token secret";
        tokens.ConsumerKey = "consumer key";
        tokens.ConsumerSecret = "consumer secret";

        TwitterResponse<TwitterStatus> tweetResponse
            = TwitterStatus.Update(tokens, twitterStatusUpdate);
        if (tweetResponse.Result != RequestResult.Success)
        {
            // Something went wrong! raise an exception
        }
    }
}
```

Call the updateTwitterStatus method from your application passing in a new update for twitter as a string and thats it!

```text
twitterFunctions.updateTwitterStatus("StuffAboutCode rocks");
```

### 4. Jobs a good un!
