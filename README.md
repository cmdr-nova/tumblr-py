# tumblr-py

I wanted to find a way to make Tumblr seem a bit more connected to the Fediverse. Since Matt Mullenweg is too busy self-destructing and bringing Wordpress down with him (as of writing this, October 18th, 2024), Tumblr's apparently *eventual* ActivityPub integration seems to never be coming. Fear not! Python's got your back, homie. So, I made this little script that looks at the top trending posts across Tumblr, then picks an image post, and finally, drops that mother-freaker right onto Mastodon.

Simple.

Steps:

Setup an environment

```
python3 -m venv your-environment
```

Activate the environment, and then install the Mastodon code.

```
pip install mastodon.py
```

Put the script into the same directory, and then set us up a cronjob to pull just once, per day.

```
0 17 * * * tumblr-bot/tumblr-env/bin/python3 tumblr-py/tumblr-py.py
```
(this is an example that posts at 5pm each day)

The reason you only want to do this *once* per day, is because, in order to pull a larger base of image posts, you need to make *numerous* API calls, which will rate limit you in seconds. So, instead, just have it make an API call once a day, and post the result. If the result turns out to be the same every single day, then maybe that's something for me to investigate further.

But, there you go!
