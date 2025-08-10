# Simple PDF Splitter

A robust, local PDF splitting tool with an intuitive web interface. Split large PDFs into smaller files quickly and securely - all processing happens locally on your computer with **zero data transmission**. No cloud uploads, no data retention, no tracking.

**Privacy**: This app processes your files locally with no data storage after you exit the program - like a digital paper shredder that only keeps what you want.

## ⚖️ License & Disclaimer

**MIT License** - Free to use, modify, and distribute.

**IMPORTANT DISCLAIMER**: This software is provided "AS IS" without warranty of any kind, express or implied. Use at your own risk. The author assumes no responsibility for any data loss, system issues, or other consequences arising from the use of this software.

**Note**: This project is provided as-is. While the code is available for review and modification, active maintenance is not guaranteed.

---

## 🚀 Quick Start

**Download** → **Extract** → **Run** → **Open Browser to `localhost:5000`**

*Having installation issues? Jump to the [Installation Troubleshooting](#-installation-troubleshooting) section below.*

---

## 📥 Installation

### System Requirements
- **Windows**: Windows 10 or later (64-bit)
- **macOS**: macOS 10.14 (Mojave) or later
- **RAM**: 4GB minimum, 8GB recommended for large PDFs
- **Disk Space**: 100MB free space

### Download Instructions

1. **Download the latest version** (when available)
2. **Choose the appropriate version**:
   - `Simple-PDF-Splitter-Windows.zip` for Windows
   - `Simple-PDF-Splitter-macOS.zip` for macOS
3. **Extract the downloaded file** to a folder of your choice
4. **Follow the platform-specific instructions below**

---

## 🖥️ Platform-Specific Setup

### Windows Installation

1. **Extract the ZIP file** to `C:\Simple-PDF-Splitter` (or your preferred location)
2. **Navigate to the extracted folder**
3. **Double-click `Simple-PDF-Splitter.exe`**

#### ⚠️ Expected Security Warning
Windows will show this warning on first run:

```
Windows protected your PC
Microsoft Defender SmartScreen prevented an unrecognized app from starting.
```

**This is normal for unsigned software. To proceed:**
1. Click **"More info"**
2. Click **"Run anyway"**
3. The application will start and remember your choice for future runs

### macOS Installation

1. **Extract the ZIP file** to `/Applications/Simple-PDF-Splitter` (or your preferred location)
2. **Navigate to the extracted folder**
3. **Double-click the application bundle**

#### ⚠️ Expected Security Warnings
macOS will show these warnings on first run:

**Warning 1 - Gatekeeper:**
```
"Simple PDF Splitter" cannot be opened because it is from an unidentified developer.
```

**To resolve:**
1. Go to **System Preferences** → **Security & Privacy**
2. Click **"Open Anyway"** next to the blocked application message
3. Confirm by clicking **"Open"** in the dialog

**Warning 2 - Quarantine Dialog:**
```
"Simple PDF Splitter" is an app downloaded from the internet. Are you sure you want to open it?
```
- Click **"Open"** to continue

---

## 🌐 Using the Application

1. **Start the application** using the steps above
2. **Open your web browser** and go to: `http://localhost:5000`
3. **Upload your PDF** and configure split settings
4. **Download your split files** directly to your computer

### Browser Compatibility
- ✅ Chrome (recommended)
- ✅ Firefox  
- ✅ Safari
- ✅ Edge

---

## Features

### Professional GUI Interface
- Intuitive drag-and-drop interface with custom branding
- Real-time validation and feedback
- Progress tracking with visual indicators

### Batch Processing
- Split multiple page ranges from the same document in one operation
- Configure unlimited splits with custom names
- Process all splits simultaneously

### Client & Case Management
- Built-in fields for client names and case numbers
- Professional file naming conventions
- Automatic organization of output files

### Advanced Statistics
- Real-time document coverage analysis
- Gap detection to identify missed pages
- Visual representation of split coverage

### Professional File Naming
- Automatic naming with client info, case numbers, and document codes
- Format: `{client_name}_{case_number}_{doc_code}_{optional_name}_{pages}.pdf`
- Example: `John_Smith_CV2024-001_DISC001_Medical_Records_001-025.pdf`

### Configurable Output
- Customizable output folder with settings persistence
- Automatic folder creation
- Recent folder history

---

## 🛠️ Common Issues

### Application Won't Start
- **Windows**: If you see security warnings, click "More info" then "Run anyway"
- **macOS**: Go to System Preferences → Security & Privacy → click "Open Anyway"
- **Both**: Make sure you extracted the ZIP file completely before running

### Windows Error Codes
If you see error codes like "0xc000007b" or similar:
- These are Windows system errors
- Search for the specific error code on Microsoft's support site
- Often related to missing Windows components
- Your IT department may need to help

### Browser Can't Connect
- Wait 10-15 seconds after starting the application
- Make sure the application is still running (check if the window is open)
- Try refreshing the browser page
- Try a different browser (Chrome or Firefox recommended)

### PDF Processing Issues
- **Large files**: May take longer to process - be patient
- **Downloads not starting**: Check your browser's download settings
- **Error messages**: Take a screenshot for reference

### General Tips
- Restart the application if something seems stuck
- Make sure your PDF files aren't corrupted or password-protected
- Close other applications if running low on memory

---

## 🔒 Security & Privacy

### Why These Security Warnings Appear
This software is **unsigned** because code signing certificates cost hundreds of dollars annually. The warnings are your operating system being cautious about any unsigned executable.

### Complete Privacy & Data Security
- ✅ **100% local processing** - no internet connection required or used
- ✅ **Zero data transmission** - nothing is sent anywhere, ever
- ✅ **No data retention** - files are processed in memory and immediately released
- ✅ **No persistent storage** - all data is cleared when the application exits
- ✅ **No user data capture** - no logs, no analytics, no tracking of any kind
- ✅ **No servers involved** - purely localhost application
- ✅ **Files never leave your computer** - complete air-gap security
- ✅ **Source code available** for independent security verification

**In simple terms**: This app works exactly like a desktop calculator - it helps you do something useful, then forgets everything. Your PDFs and any information about them exist only on your computer and nowhere else.

### Verification
**File Integrity**: Each release includes SHA256 checksums. Verify your download:

**Windows (PowerShell):**
```powershell
Get-FileHash Simple-PDF-Splitter-Windows.zip -Algorithm SHA256
```

**macOS/Linux (Terminal):**
```bash
shasum -a 256 Simple-PDF-Splitter-macOS.zip
```

Compare the output with the checksum provided in the release notes.

---

## Development

### Running from Source
For developers who want to run from source code:

1. **Get the source code**
   ```bash
   # Clone from your repository when available
   # Or extract from source distribution
   cd simple-pdf-splitter
   ```

2. **Install Python 3.12+**
   - Download from [python.org](https://www.python.org/downloads/)

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open browser** to `http://localhost:5000`

### Project Architecture

This application follows professional software development patterns:

```
simple_pdf_splitter/
├── app.py                         # Flask application entry point
├── src/
│   ├── config/                    # Configuration management
│   │   ├── settings.py            # Application constants
│   │   ├── messages.py            # User-facing strings
│   │   └── paths.py               # Path management
│   ├── models/                    # Data models
│   │   └── split_request.py       # Request/response models
│   ├── services/                  # Core services
│   │   ├── pdf_service.py         # PDF manipulation
│   │   ├── file_validator.py      # File validation
│   │   └── session_service.py     # Session management
│   ├── presenters/                # MVP presenters
│   │   ├── web_presenter.py       # Main presenter
│   │   ├── upload_presenter.py    # Upload logic
│   │   └── process_presenter.py   # Processing logic
│   └── views/                     # User interface
│       ├── web_routes.py          # Flask routes
│       ├── htmx_routes.py         # HTMX endpoints
│       └── htmx_configure.py      # Configuration UI
├── templates/                     # HTML templates
├── static/                        # CSS, JS, images
└── tests/                         # Test suite
```

### Architecture Highlights

- **MVP Pattern** - Model-View-Presenter for clean separation of concerns
- **Configuration Management** - Centralized settings and constants
- **Type Safety** - Full type hints throughout codebase
- **Error Handling** - Comprehensive validation and user feedback
- **Threading** - Non-blocking UI with background PDF processing
- **Professional Documentation** - Complete docstrings and code comments

---

## 📋 System Information for Support

If you need help, please include this information:

**Windows:**
```
OS Version: [Windows 10/11 + build number]
Application Version: [from About dialog]
Error Message: [exact text]
Browser: [Chrome/Firefox/Edge + version]
```

**macOS:**
```
OS Version: [macOS version]
Application Version: [from About dialog]  
Error Message: [exact text]
Browser: [Chrome/Firefox/Safari + version]
```

---

## 🆘 Getting Help

1. **Check this README** - covers 90% of common issues
2. **Visit the About page** in the application for support information
3. **For developers**: Check the source code and documentation

### Support
- Create detailed bug reports with system information
- Include screenshots when relevant for visual issues
- Provide step-by-step reproduction steps for bugs

---

## 🔄 Updates

**Automatic updates**: Not available (security by design)
**Manual updates**: 
1. Download the latest release
2. Replace the old application folder
3. Your settings and preferences are preserved

**Stay informed**: 
- ⭐ **Star this repository** to get notified of new releases
- 👀 **Watch** for important security updates

---

## 🤝 Contributing

Found a bug? Have a feature request? 

- 🐛 **Bug Reports**: Document the issue with clear reproduction steps
- 💡 **Feature Requests**: Describe your use case and proposed solution
- 🔧 **Code Contributions**: Fork the repository when available

---

*Made with ❤️ for document workflow efficiency. No cloud required.*