from flask import Flask, jsonify, request
from colorama import Fore, init
from flask_cors import CORS
import instaloader
import json
import uuid
import os

app = Flask(__name__)  # flask
init(autoreset=True) # colorama
CORS(app) # flask

DATABASE_FILE = '../database/instagram.txt'
global_sessions = {}


##########################################
###              SESSIONS              ###
##########################################

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "Server is running"}), 200

def create_session(uuid):
    print(f"{Fore.GREEN}CREATED SESSION - {uuid}")
    global_sessions[uuid] = {
        'data': {},
    }
    print(f"{Fore.BLUE} Global Sessions: {len(global_sessions)}")
    
def delete_session(uuid):
    if uuid in global_sessions:
        del global_sessions[uuid]
        print(f"{Fore.RED}DELETED SESSION - {uuid}")
        print(f"{Fore.BLUE} Global Sessions: {len(global_sessions)}")
        return True
    else:
        return False

@app.route('/api/create_session', methods=['POST'])
def create_session_endpoint():
    session_id = str(uuid.uuid4())
    create_session(session_id)
    return jsonify({'sessionId': session_id}), 200

@app.route('/api/delete_session', methods=['POST'])
def delete_session_endpoint():
    data = request.get_json()
    session_id = data.get('sessionId')
    if session_id and delete_session(session_id):
        return jsonify({'message': 'Session deleted successfully'}), 200
    else:
        return jsonify({'error': 'Invalid session ID'}), 403
    
###########################################
###              INSTAGRAM              ###
###########################################

def read_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_database(database):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(database, file, indent=4)

def get_instagram_account_info(username):
    loader = instaloader.Instaloader()

    try:
        loader.login("rysun.api", "Ten37yellow!")
        profile = instaloader.Profile.from_username(loader.context, username)

        posts = profile.get_posts()
        post_details = []

        for post in posts:
            post_details.append({
                'shortcode': post.shortcode,
                'likes': post.likes,
                'comments': post.comments,
                'url': post.url,
                'image_url': post.url,
                'caption': post.caption,
            })
        try:
            highest_engagement_post = max(post_details, key=lambda x: x['likes'] + x['comments'])
            lowest_engagement_post = min(post_details, key=lambda x: x['likes'] + x['comments'])
            
            res = write_instagram_iframe(highest_engagement_post, lowest_engagement_post)
            highest_engagement_post["href"] = res[0]
            lowest_engagement_post["href"] = res[1]
        except:
            highest_engagement_post = None
            lowest_engagement_post = None

        account_info = {
            'username': profile.username,
            'full_name': profile.full_name,
            'biography': profile.biography,
            'followers': profile.followers,
            'followees': profile.followees,
            'posts': profile.mediacount,
            'profile_pic_url': profile.profile_pic_url,
            'highest_engagement_post': highest_engagement_post,
            'lowest_engagement_post': lowest_engagement_post
        }
        return account_info

    except instaloader.exceptions.ProfileNotExistsException:
        return f"Profile with username {username} does not exist."
    except Exception as e:
        return str(e)


def write_instagram_iframe(highest, lowest):
    try:
        h = "https://www.instagram.com/p/xxx/?img_index=1"
        l = "https://www.instagram.com/p/yyy/?img_index=1"
        h = h.replace("xxx", highest)
        l = l.replace("yyy", lowest)
        print(h,l)
        return [h, l]
    except Exception as e:
        print(e)
        return ["", ]
    
@app.route('/get_instagram_info', methods=['POST'])
def get_instagram_info():
    data = request.json
    username = data.get('username')[1:]

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    database = read_database()
    
    if username in database:
        write_instagram_iframe(database[username]['highest_engagement_post']['shortcode'], database[username]['lowest_engagement_post']['shortcode'])
        
        return jsonify(database[username]), 200
    
    info = get_instagram_account_info(username)
    
    if isinstance(info, str):
        return jsonify({"error": info}), 404
    
    database[username] = info
    save_database(database)

    return jsonify(info), 200


######################################
###              MAIN              ###
######################################

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
