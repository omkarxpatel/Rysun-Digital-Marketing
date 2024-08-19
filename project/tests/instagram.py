import instaloader

def get_instagram_account_info(username):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Login to Instagram
        loader.login("rysun.api", "Ten37yellow!")  # Replace with your Instagram credentials

        # Load the profile from Instagram
        profile = instaloader.Profile.from_username(loader.context, username)

        # Extract relevant information
        account_info = {
            'username': profile.username,
            'full_name': profile.full_name,
            'biography': profile.biography,
            'followers': profile.followers,
            'followees': profile.followees,
            'posts': profile.mediacount,
            'profile_pic_url': profile.profile_pic_url,
        }

        return account_info, dir(profile)

    except instaloader.exceptions.ProfileNotExistsException:
        return f"Profile with username {username} does not exist."
    except Exception as e:
        return str(e)

# Example usage
username = 'sephora'
info = get_instagram_account_info(username)
print(info)
