---
title: 'Facebook comments and asp.net'
date: 2012-05-06 22:08:00 +01:00
tags: [asp, csharp, dotnet, social-networking]
redirect_from:
  - /2012/05/facebook-comments-and-aspnet.html
---

## Using facebook comments plugin on my website

Anyway... I wanted to let users of [www.GoOffPiste.com](http://www.gooffpiste.com/) comment on ski resorts and being a typical developer my first reaction was to start my development environment and start coding; not the best approach - re-usable solutions are 10 a penny, very mature and offer great levels of functionality, a [quick google search](https://www.google.co.uk/search?q=adding+comments+to+web+page&oq=adding+comments+to+web+page02l5l5l0l1l1l0l150l463l1j3l4l0.frgbld.) will bring up loads of potentials.

I choose the implement facebook's comments social plugin as I was already using other facebook functions to allow people to login and I liked the idea that comments would find a wider audience as they could also be posted to people's news feed. See [http://www.gooffpiste.com/St-Anton-offpiste/4](http://www.gooffpiste.com/St-Anton-offpiste/4) for an example.

The facebook developers site has got some great documentation and tools to help implement the comments social plug-in, [http://developers.facebook.com/docs/reference/plugins/comments/](http://developers.facebook.com/docs/reference/plugins/comments/), although I did find some 'anomalies' between the theory and the implementation.

### Include facebook SDK

In order to use any of facebook's api or plug-ins the Javascript SDK is required and the script must be included on each webpage that uses it, see [http://developers.facebook.com/docs/reference/javascript/](http://developers.facebook.com/docs/reference/javascript/).

I was already using the facebook SDK when I was came to implement facebook comments and as I was using it across a good percentage of the site I had included the SDK in the master page. There are, however, a number of potential methods for including the SDK; the simplest if the site is only going to be using comments is probably to just include the following script on each page (or the asp.net master page) where the comments plugin is going to be used.

```html
<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_GB/all.js#xfbml=1";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
```

If however the site is going to make use other facebook functions (particularly login) a facebook application should be created and the complete SDK including a local ChannelURL, see [http://developers.facebook.com/docs/reference/javascript/](http://developers.facebook.com/docs/reference/javascript/).

### Include comments box

Including the comments box was relatively simple, I included the following tag within the webpage:

```html
<div class="fb-comments" href="http://www.gooffpiste.com/St-Anton-offpiste/4" width="735" ></div>
```

**href attribute**
 The href attribute is the url of the page of which the comment plugin appears, but more specifically it is used by the plugin as a unique id and includes any server side (query string) or client side parameters, this is worth noting as the following URL's would be all considered unique:

http://www.example.com/page
 http://www.example.com/page?a=1
 http://www.example.com/page#1

This created me some challenges when implementing the plugin, as the page I wanted to put the plugin was dynamically created passed on a query string value e.g. [http://www.gooffpiste.com/resort.aspx?**resortId=4**](http://www.gooffpiste.com/resort.aspx?resortId=4) but as I was also using "URL re-directing" the URL actually appeared to users as [http://www.gooffpiste.com/St-Anton-offpiste/4](http://www.gooffpiste.com/St-Anton-offpiste/4).

I decided that I would use the URL the user would be familiar with (i.e. whats shown by the browser), so I wrote a function to pull out the actual browser URL:

```html
     public static string getFacebookCommentsURL(HttpRequest request)
    {
        string commentsURL = getFullBrowserURL(request);
        if (commentsURL.IndexOf("?") > 0)
        {
            commentsURL = commentsURL.Substring(0, commentsURL.IndexOf("?"));
        }
        return commentsURL;
    }
    public static string getFullBrowserURL(HttpRequest request)
    {
        return request.Url.GetLeftPart(System.UriPartial.Authority).ToString() + request.RawUrl.ToString();
    }
```

The function also strips out any query string on the URL as I noticed that when a user followed a link from their facebook notifications, facebook would append a fb:comments querystring parameter to the URL e.g.

```text
http://www.gooffpiste.com/St-Anton-offpiste/4?fb:comments=27497124....
```

Which is presumably used by the facebook plugin to take the user to the right comment, but meant that a user didn't see comments as my function included this query string within the href attribute of the control.
 I then called this function in-line in the asp.net page to dynamically build the facebook comment control.

```html
<div class="fb-comments" href="<%=utils.getFacebookCommentsURL(Request)%>" width="735" ></div>
```

### Setup moderation

When it comes to setting up moderation I had 2 options:

- Allow moderation by specific user id
- Allow moderation by facebook application

This was a simple choice as I was already using a facebook application, and all it required was including an additional meta tag on my master page (or any page using the comments plugin).

```html
<meta property="fb:app_id" content="{YOUR_APPLICATION_ID}"/>
```

This then allowed me to modify plugin settings and review and moderate the comments on facebook, [http://developers.facebook.com/tools/comments](http://developers.facebook.com/tools/comments).

I would really suggest you create a facebook application as it gives much greater flexibility but it this isn't an options you can setup moderation by including a meta tag which references a specific facebook user id.

```html
<meta property="fb:admins" content="{YOUR_FACEBOOK_USER_ID}"/>
```

So that's it... Facebook comments on your asp.net website...
