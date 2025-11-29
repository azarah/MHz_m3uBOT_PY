"""
Flask web server for the web player interface.
This runs alongside the Discord bot to serve the web player.
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import threading
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # Enable CORS for API endpoints

# Global reference to bot cache (will be set by bot.py)
bot_cache = {}

def set_bot_cache(cache):
    """Set the bot's cache reference so web server can access it"""
    global bot_cache
    bot_cache = cache

@app.route('/')
def index():
    """Serve the main web player page"""
    return render_template('player.html')

@app.route('/api/playlist/<int:user_id>')
def get_playlist(user_id):
    """Get playlist for a specific user ID"""
    tracks = bot_cache.get(user_id, [])
    return jsonify({
        'success': True,
        'user_id': user_id,
        'tracks': tracks,
        'count': len(tracks)
    })

@app.route('/api/playlist')
def get_playlist_by_token():
    """Get playlist using a token (for security)"""
    token = request.args.get('token')
    if not token:
        return jsonify({'success': False, 'error': 'Token required'}), 400
    
    # Simple token validation (you can enhance this)
    # For now, token format: user_id-timestamp
    try:
        user_id = int(token.split('-')[0])
        tracks = bot_cache.get(user_id, [])
        return jsonify({
            'success': True,
            'user_id': user_id,
            'tracks': tracks,
            'count': len(tracks)
        })
    except (ValueError, IndexError):
        return jsonify({'success': False, 'error': 'Invalid token'}), 400

@app.route('/api/users')
def list_users():
    """List all users with cached playlists"""
    users = [{'user_id': uid, 'track_count': len(tracks)} 
             for uid, tracks in bot_cache.items()]
    return jsonify({
        'success': True,
        'users': users,
        'count': len(users)
    })

def run_web_server(host='127.0.0.1', port=5000):
    """Run the Flask web server in a separate thread"""
    app.run(host=host, port=port, debug=False, use_reloader=False)

