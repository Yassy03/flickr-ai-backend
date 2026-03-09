import random

def get_authentic_flickr_images(target_count=25):
    print("Initializing Hyper-Randomized Vintage Proxy Fetcher...")
    
    # A massive pool of highly specific, mid-2000s aesthetic tags
    aesthetic_tags = [
        'digicam', '2005', 'myspace', 'flash', 'candid', 'snapshot',
        '2006', '2007', '2008', '2009', '2010', '2011', 'y2k',
        'party', 'nightout', 'friends', 'bedroom', 'mirrorpic',
        'digitalcamera', 'pointandshoot', 'disposable', 'polaroid',
        'webcam', 'photobooth', 'mall', 'basement', 'glare', 'neon',
        'vintagecam', 'ccd', 'nostalgia', 'throwback'
    ]
    
    # Shuffle the massive pool and slice out exactly our target count (25).
    # This guarantees NO TWO IMAGES use the same search tag in a single run.
    random.shuffle(aesthetic_tags)
    selected_tags = aesthetic_tags[:target_count]
    
    unique_urls = []
    
    for tag in selected_tags:
        # Generate a massive random lock number to bypass proxy caching
        lock_id = random.randint(1, 999999)
        
        # Construct the LoremFlickr URL using the unique tag and lock
        url = f"https://loremflickr.com/500/500/{tag}?lock={lock_id}"
        
        unique_urls.append(url)
        
    print(f"\nSuccessfully generated {len(unique_urls)} highly diverse vintage URLs.")
    return unique_urls

if __name__ == "__main__":
    urls = get_authentic_flickr_images()
    print("Test output for 5 URLs:")
    for u in urls[:5]:
        print(u)