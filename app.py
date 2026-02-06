from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import json
import os
import signal
import logging
import sqlite3
import sys

# Platform-specific imports
if sys.platform != 'win32':
    import pty
    import struct
    import fcntl
    import termios

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your-secret-key-change-this-in-production'
sock = Sock(app)

# Database configuration
DB_PATH = 'profiles.db'

def init_db():
    """Initialize database with ssh_profiles table."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ssh_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            host TEXT NOT NULL,
            user TEXT NOT NULL,
            port INTEGER DEFAULT 22,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP
        )''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Routes
@app.route('/')
def index():
    return render_template('index.html')


# SSH Profiles Management API
@app.route('/api/profiles/save', methods=['POST'])
def save_profile():
    """Save a new SSH profile."""
    try:
        data = request.json
        name = data.get('name', '').strip()
        host = data.get('host', '').strip()
        user = data.get('user', '').strip()
        port = data.get('port', 22)
        
        if not all([name, host, user]):
            return jsonify({'success': False, 'message': 'Missing required fields (name, host, user)'}), 400
        
        if not isinstance(port, int) or port < 1 or port > 65535:
            return jsonify({'success': False, 'message': 'Invalid port number'}), 400
        
        try:
            db = get_db()
            db.execute(
                "INSERT INTO ssh_profiles (name, host, user, port) VALUES (?, ?, ?, ?)",
                (name, host, user, port)
            )
            db.commit()
            db.close()
            logger.info(f"SSH profile saved: {name}")
            return jsonify({'success': True, 'message': f'Profile "{name}" saved'}), 200
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': f'Profile "{name}" already exists'}), 400
    
    except Exception as e:
        logger.error(f"Save profile error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/profiles', methods=['GET'])
def list_profiles():
    """Get all saved SSH profiles."""
    try:
        db = get_db()
        cur = db.execute("SELECT id, name, host, user, port, created_at, last_used FROM ssh_profiles ORDER BY created_at DESC")
        profiles = [dict(row) for row in cur.fetchall()]
        db.close()
        
        return jsonify({'success': True, 'profiles': profiles}), 200
    except Exception as e:
        logger.error(f"List profiles error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Delete a saved SSH profile."""
    try:
        db = get_db()
        cur = db.execute("SELECT name FROM ssh_profiles WHERE id=?", (profile_id,))
        profile = cur.fetchone()
        
        if not profile:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
        
        db.execute("DELETE FROM ssh_profiles WHERE id=?", (profile_id,))
        db.commit()
        db.close()
        
        logger.info(f"SSH profile deleted: {profile['name']}")
        return jsonify({'success': True, 'message': f'Profile "{profile["name"]}" deleted'}), 200
    except Exception as e:
        logger.error(f"Delete profile error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


# WebSocket for interactive terminal
@sock.route('/ws/terminal')
def terminal_ws(ws):
    """WebSocket handler for interactive terminal."""
    fd = None
    child_pid = None
    
    try:
        while True:
            data = ws.receive()
            if data is None:
                break
            
            msg = json.loads(data)
            
            if msg['type'] == 'connect':
                host = msg['host']
                user = msg['user']
                port = msg['port']
                
                # Fork a PTY for interactive SSH
                child_pid, fd = pty.fork()
                
                if child_pid == 0:
                    # Child process - exec ssh
                    os.execlp('ssh', 'ssh', 
                              '-o', 'StrictHostKeyChecking=no',
                              '-p', str(port),
                              f'{user}@{host}')
                else:
                    # Parent process
                    # Set non-blocking
                    import fcntl
                    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
                    
                    ws.send(json.dumps({'type': 'connected'}))
                    
                    # Start reading from PTY
                    import threading
                    
                    def read_output():
                        try:
                            while True:
                                try:
                                    output = os.read(fd, 1024)
                                    if output:
                                        ws.send(json.dumps({
                                            'type': 'output',
                                            'data': output.decode('utf-8', errors='replace')
                                        }))
                                except BlockingIOError:
                                    import time
                                    time.sleep(0.01)
                                except OSError:
                                    break
                        except Exception as e:
                            logger.error(f"Read error: {e}")
                    
                    read_thread = threading.Thread(target=read_output, daemon=True)
                    read_thread.start()
            
            elif msg['type'] == 'input' and fd:
                os.write(fd, msg['data'].encode('utf-8'))
            
            elif msg['type'] == 'resize' and fd:
                # Resize PTY
                winsize = struct.pack('HHHH', msg['rows'], msg['cols'], 0, 0)
                fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws.send(json.dumps({'type': 'error', 'data': str(e)}))
    
    finally:
        if fd:
            os.close(fd)
        if child_pid:
            try:
                os.kill(child_pid, signal.SIGTERM)
            except:
                pass


if __name__ == '__main__':
    # Initialize database
    init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)