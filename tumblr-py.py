import requests
from mastodon import Mastodon
import random

# Input your tumblr consumer API here. This will take some know-how, because you have to register an app with Tumblr
TUMBLR_API_KEY = 'your_tumblr_consumer_code'

# Get your Mastodon API credentials from the account you'll be posting with, in the "Development" tab under preferences.
MASTODON_API_BASE_URL = 'https://your.instance'
MASTODON_ACCESS_TOKEN = 'your_mastodon_api_key'

def get_trending_image_posts_from_tumblr():
    url = f'https://api.tumblr.com/v2/tagged?tag=trending&api_key={TUMBLR_API_KEY}&limit=50'
    response = requests.get(url)
    response.raise_for_status()
    posts = response.json()['response']
    # This is an attempt to filter out posts that aren't images, and only fetch ones that are.
    image_posts = [post for post in posts if 'photos' in post]
    return image_posts

def post_to_mastodon(content, media_urls, hashtags):
    mastodon = Mastodon(
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_API_BASE_URL
    )
    
    media_ids = []
    for media_url in media_urls:
        media_response = requests.get(media_url)
        media_response.raise_for_status()
        media_id = mastodon.media_post(media_response.content, mime_type='image/jpeg')
        media_ids.append(media_id)
    # This status and spoiler text can be made into whatever you want it to be.
    status = f"Trending on Tumblr:\n\n{content}\n\n{' '.join(hashtags)}\n\n[This post pulled from the top trending posts across #Tumblr, via a #Python script, written by @cmdr_nova@mkultra.monster]"
    spoiler_text = "Pulled from Tumblr, potentially NSFW"
    mastodon.status_post(status, media_ids=media_ids, sensitive=True, spoiler_text=spoiler_text)

def main():
    trending_posts = get_trending_image_posts_from_tumblr()
    if not trending_posts:
        print("No trending image posts found.")
        return
    
    selected_post = random.choice(trending_posts)
    
    content = selected_post.get('summary', 'No summary available')
    
    # Extracting the images from the active warzone we all know as the blue hellsite.
    media_urls = [photo['original_size']['url'] for photo in selected_post.get('photos', [])]
    
    # Exctracting links, if there are any! (maybe?)
    if 'trail' in selected_post:
        for item in selected_post['trail']:
            if 'post' in item and 'content' in item['post']:
                content += f"\n{item['post']['content']}"
    
    # Give us your hashtags, so that posts can be classified better via the Mastodon post (this might piss of hashtag purists).
    hashtags = [f"#{tag}" for tag in selected_post.get('tags', [])]
    
    post_to_mastodon(content, media_urls, hashtags)

if __name__ == '__main__':
    main()
