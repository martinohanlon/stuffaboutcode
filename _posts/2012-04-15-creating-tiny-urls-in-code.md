---
title: 'Creating Tiny URLs in code'
date: 2012-04-15 21:36:00 +01:00
tags: [asp, csharp, dotnet, social-networking]
redirect_from:
  - /2012/04/creating-tiny-urls-in-code.html
---

## Calling TinyURL.com api from asp.net

Anyway... I needed to dynamically create short urls from the long urls which are so useful in my website [www.gooffpiste.com](http://www.gooffpiste.com/) but so cumbersome when dealing with things like twitter, so I looked round for an easy to integrate solution and choose [tinyurl.com](http://tinyurl.com/) predominantly because of its simple interface and long standing reputation.

TinyURL has a really simple api which

is called by passing a the long url as a query string to

http://tinyurl.com/api-create.php?url={0} (e.g. [http://tinyurl.com/api-create.php?url=www.google.com](http://tinyurl.com/api-create.php?url=www.google.com))

and

returns a link to a TinyURL in the format

http://tinyurl.com/#####.

I created a .net function which used the HttpWebRequest class to call the TinyURL api and then strip out the response.

```html
public string getTinyURL(string longURL)
    {
        string shortUrl = "";

        try
        {
 // build TinyURL api URL
string tinyURLApiUrl
                = "
http://tinyurl.com/api-create.php?url={0}";
            tinyURLApiUrl
                = tinyURLApiUrl.Replace("{0}", longURL);

            // call the URL and get the response
HttpWebRequest request
                = (HttpWebRequest)WebRequest.Create(tinyURLApiUrl);
            WebResponse response = request.GetResponse();
            // put the response into a stream
Stream responseStream
                = request.GetResponse().GetResponseStream();
            // read the short URL from the stream
StreamReader reader
                = new StreamReader(responseStream);

            shortUrl = reader.ReadToEnd();
        }
        catch (Exception e)
        {
            // something went wrong!
        }

        return shortUrl;
    }
```

So call this function passing in a Long URL and it returns a corresponding TinyURL.
