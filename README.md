# PARAM SSH Manager

A modern, web-based SSH terminal manager designed for HPC clusters and remote server management. Built with Flask and xterm.js, it provides an intuitive interface for managing SSH connections, SLURM jobs, Conda environments, and file operations.

## ✨ Features

### 🔐 SSH Connection Management
- **Interactive Terminal**: Full-featured terminal emulator with xterm.js
- **Profile Management**: Save and manage multiple SSH connection profiles
- **Quick Connect**: One-click connection with saved profiles
- **Real-time Status**: Visual connection status indicators

### 📁 File Manager
- **Remote File Browser**: Navigate remote filesystem with ease
- **File Operations**: View, edit, and delete files directly from the browser
- **Directory Search**: Find files quickly across directories
- **Disk Quota Check**: Monitor your disk usage on remote systems
- **Home Directory Quick Access**: Jump to home directory instantly

### 🖥️ SLURM Job Management
- **Job Dashboard**: Real-time view of your SLURM jobs
- **Job Control**: Submit, monitor, and cancel jobs from the web interface
- **Queue Information**: Check job status, priority, and resource allocation
- **Node Status**: View cluster node availability and resources
- **GPU Information**: Monitor GPU usage and availability

### 🐍 Conda Environment Manager
- **Environment Creation**: Create new Conda environments remotely
- **Package Installation**: Install packages in your environments
- **Environment Cleanup**: Remove unused environments to save space

### 💻 System Information
- **Real-time Metrics**: View hostname, OS, kernel, architecture
- **Resource Monitoring**: Check CPU cores and memory availability
- **Instant Updates**: Refresh system information on demand

## 🎨 Screenshots

### File Browser
*Navigate and manage remote files*
![File Manager](static/FILE_Manager.png)

### SLURM Jobs Dashboard
*Monitor and manage your HPC jobs*
![SLURM Page](static/SLURM_Dashboard.png)

### Conda Environment Manager
*Manage conda environments*
![Conda Manager](static/CONDA_Env.png)

### System Info
*Interactive terminal with connection management*
![System Info](static/SYS_Info.png)

## 📋 Prerequisites

- Python 3.8 or higher
- SSH access to remote servers
- Modern web browser with WebSocket support

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ayush1512/paramConsole
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the web interface**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📦 Dependencies

- **Flask 3.0.0**: Web framework
- **flask-sock 0.7.0**: WebSocket support for real-time terminal
- **Werkzeug 3.1.4**: WSGI utility library

## 🔧 Configuration

### Database
The application uses SQLite to store SSH profiles. The database file (`profiles.db`) is automatically created on first run.

### Network
By default, the application runs on:
- **Host**: `0.0.0.0` (accessible from network)
- **Port**: `5000`

To change these settings, modify the last line in `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📖 Usage

### Connecting to a Server

1. Enter your SSH credentials in the sidebar:
   - **Host**: Remote server address
   - **Username**: Your SSH username
   - **Port**: SSH port (default: 22)

2. Click **Connect** to establish the connection

3. Optionally, save the connection as a profile for future use

### Managing Profiles

- **Save Profile**: Click "Save" after entering connection details
- **Connect with Profile**: Click "Connect" on any saved profile
- **Delete Profile**: Remove profiles you no longer need

### File Management

1. Switch to the **File Manager** tab
2. Enter a directory path or click **Browse Home**
3. Use the file browser to:
   - View file details (size, permissions, modified date)
   - View file contents
   - Delete files
   - Search for files in directories
   - Check disk quota

### SLURM Jobs

1. Connect to your HPC cluster
2. Switch to the **SLURM Jobs** tab
3. View your running and queued jobs
4. Use the interface to:
   - Submit new jobs
   - Check job status and details
   - Cancel jobs
   - View node and GPU information

### Conda Environments

1. Switch to the **Conda Environments** tab
2. Create new environments with custom names
3. Install packages into environments
4. Remove environments when no longer needed

## 🎯 Project Structure

```
Final/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── profiles.db           # SQLite database (auto-generated)
├── static/
│   ├── nsm.png          # Application logo
│   └── nsm.webp         # Application logo (WebP format)
├── templates/
│   └── index.html       # Main web interface
└── README.md            # This file
```

## 🛡️ Security Notes

- SSH connections use your system's SSH client with key-based authentication
- Passwords are never stored by the application
- All SSH connections are established through secure PTY (pseudo-terminal)
- StrictHostKeyChecking is disabled for convenience (can be modified in code)

## 🐛 Troubleshooting

### Connection Issues
- Ensure SSH is properly configured on your system
- Verify you can connect via command-line SSH first
- Check if the remote server accepts SSH connections

### WebSocket Errors
- Make sure your browser supports WebSockets
- Check if any firewall is blocking WebSocket connections
- Ensure Flask-Sock is properly installed

### Terminal Not Responding
- Refresh the page and reconnect
- Check browser console for error messages
- Verify the WebSocket connection is established

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source. Please check the repository for license details.

## 👨‍💻 Author

Developed for PARAM supercomputing infrastructure management.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Terminal powered by [xterm.js](https://xtermjs.org/)
- UI inspired by modern terminal applications

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Open a new issue with detailed information

---

**Note**: This application is designed for trusted environments. Always follow your organization's security policies when deploying web-based SSH clients.
