import requests

# Replace 'your_access_token' with your actual Pinterest API access token
ACCESS_TOKEN = 'your_access_token'
BASE_URL = 'https://api.pinterest.com/v1/'

def get_pinterest_account_info(username):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Fetch user profile
    profile_url = f'{BASE_URL}users/{username}/'
    response = requests.get(profile_url, headers=headers)
    
    if response.status_code != 200:
        return f"Error fetching profile: {response.status_code}, {response.text}"
    
    profile = response.json()['data']

    # Fetch user pins
    pins_url = f'{BASE_URL}boards/{profile["id"]}/pins/'
    response = requests.get(pins_url, headers=headers)

    if response.status_code != 200:
        return f"Error fetching pins: {response.status_code}, {response.text}"

    pins = response.json()['data']
    
    pin_details = []
    for pin in pins:
        pin_details.append({
            'id': pin['id'],
            'url': pin['url'],
            'image_url': pin['image']['original']['url'],
            'note': pin['note'],
            'link': pin['link'],
            'repin_count': pin['repin_count'],
            'like_count': pin['like_count']
        })
    
    highest_engagement_pin = max(pin_details, key=lambda x: x['repin_count'] + x['like_count'])
    lowest_engagement_pin = min(pin_details, key=lambda x: x['repin_count'] + x['like_count'])
    
    account_info = {
        'username': profile['username'],
        'full_name': profile['full_name'],
        'bio': profile['bio'],
        'followers': profile['counts']['followers'],
        'following': profile['counts']['following'],
        'pins': profile['counts']['pins'],
        'profile_image_url': profile['image']['60x60']['url'],
        'highest_engagement_pin': highest_engagement_pin,
        'lowest_engagement_pin': lowest_engagement_pin
    }
    
    return account_info

# Example usage
username = 'example_username'
account_info = get_pinterest_account_info(username)
print(account_info)
