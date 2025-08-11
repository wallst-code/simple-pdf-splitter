# Simple PDF Splitter

A robust, desktop PDF splitting tool with an intuitive graphical interface. Split large PDFs into smaller files quickly and securely - designed for local processing without cloud dependencies.

**Privacy-Focused**: This app processes your files locally on your computer, making it more secure than web-based alternatives that transmit files over the internet. No cloud uploads or external servers required.

## ⚖️ License & Legal Disclaimer

### License
This software is distributed under the **MIT License**. See [LICENSE](LICENSE) file for full terms.

### NO WARRANTY DISCLAIMER
**THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.**

**IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

### Important Legal Notices
- **USE AT YOUR OWN RISK**: The author(s) assume no responsibility for any data loss, corruption, system issues, or other consequences arising from the use of this software
- **NO LEGAL ADVICE**: This software is a tool only and does not constitute legal advice
- **DATA RESPONSIBILITY**: You are solely responsible for the handling and protection of your data
- **COMPLIANCE**: Users are responsible for ensuring their use complies with applicable laws and regulations
- **NO GUARANTEE**: No guarantee of fitness for any particular purpose is provided
- **MAINTENANCE**: This project is provided as-is. Active maintenance is not guaranteed

---

## 🚀 Quick Start - Windows Desktop Application

### 🪟 Windows Users
**Download installer** → **Run setup** → **Start splitting PDFs!**

*Professional Windows installation with desktop shortcut.*

---

## 📥 Download & Installation

### System Requirements
- **Windows**: Windows 10 or later (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 200MB free space

### Installation Options

⚠️ **Don't use the green "Code" button** - go to **[Releases](https://github.com/wallst-code/simple-pdf-splitter/releases)**

#### Option 1: Installer (Recommended)
1. **Download** `SimplePDFSplitter_Setup_v1.0.0.exe`
2. **Double-click** to run the installer
3. **If Windows shows a security warning:**
   - Click "More info"
   - Click "Run anyway" (this is normal for new software)
4. **Follow the installation wizard**
   - Accept license agreement
   - Choose install location (or use default)
   - Desktop shortcut will be created
5. **Launch from desktop shortcut or Start Menu**

#### Option 2: Portable ZIP
1. **Download** `SimplePDFSplitter-Windows-v1.0.0.zip`
2. **Extract** the ZIP file to any folder
3. **Navigate** to the extracted folder
4. **Run** `SimplePDFSplitter.exe`
5. *Optional:* Create your own shortcut

---

## ✨ Features

- **🔒 Privacy-Focused** - Local processing without internet transmission
- **📄 Smart Page Splitting** - Split by page ranges with automatic validation
- **🏷️ Custom Naming** - Name each split with client, case, and document codes
- **📊 Batch Processing** - Split multiple sections in one operation
- **🎯 Legal Professional Focus** - Designed for law firms and legal departments
- **💻 Native Desktop Application** - Professional Windows application
- **🚀 Fast Performance** - Optimized PDF processing engine
- **📁 Organized Output** - Files saved with clear naming convention

## 📖 How to Use

### Step 1: Load Your PDF
- Click **"Select PDF File"** button
- Or drag and drop your PDF into the window
- The application displays the filename and total page count

### Step 2: Configure Client Information
- Enter **Client Name** (e.g., "Smith, John")
- Enter **Case Number** (e.g., "2024-CV-001234")

### Step 3: Define Split Sections
- Click **"+ Add Split"** to add a new section
- For each section, specify:
  - **Start Page** and **End Page** (auto-calculated)
  - **Document Code** (e.g., "EXH001", "DEPO")
  - **Description** (optional additional text)
- Green checkmarks appear when entries are valid
- Remove sections with the **×** button if needed

### Step 4: Process the PDF
- Click **"Run Split"** to process
- Progress shown in status area
- Files are saved to your Downloads folder
- Success dialog shows all created files
- Click **"Open Folder"** to view the files

*Note: Each file gets a unique ID added to prevent naming collisions and other nerdy technical problems. Think of it as your file's social security number, but less controversial.*

## 🎯 Use Cases

### Legal Document Management
- **Discovery Documents**: Split large discovery productions into individual exhibits
- **Court Filings**: Separate combined filings into individual documents
- **Depositions**: Extract specific page ranges from transcripts
- **Contracts**: Split multi-document contract packages
- **Medical Records**: Organize records by date or provider
- **Real Estate**: Separate closing documents

### Example Workflow
```
Original: Discovery_Production.pdf (500 pages)
↓
Split into:
- Smith_2024CV001234_EXH001_Contract.pdf (pages 1-25)
- Smith_2024CV001234_EXH002_Emails.pdf (pages 26-150)
- Smith_2024CV001234_EXH003_Financial.pdf (pages 151-300)
- Smith_2024CV001234_EXH004_Correspondence.pdf (pages 301-500)
```

## 🛡️ Security & Privacy

### Privacy-Focused Design
- ✅ **Local Processing** - Works without internet connection
- ✅ **No Cloud Dependencies** - Files remain on your computer
- ✅ **No Analytics** - Usage is not tracked
- ✅ **Minimal Data Footprint** - Temporary files cleaned after use
- ✅ **Desktop Application** - No web servers involved
- ✅ **Open Source** - Code available for inspection

### Enhanced Privacy
- Processing occurs locally, reducing exposure compared to cloud services
- No requirement to upload files to third-party servers
- More private than web-based alternatives that transmit data
- Designed to minimize data exposure risks

## 🏗️ Building from Source (For Developers)

### Prerequisites
- Python 3.9+
- PyQt6
- PyMuPDF

### Development Setup
```bash
# Clone the repository
git clone https://github.com/wallst-code/simple-pdf-splitter.git
cd simple-pdf-splitter

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main_gui.py
```

### Build Executable
```bash
# Windows
build_gui.bat

# The executable will be in dist/SimplePDFSplitter/
```

### Create Installer
```bash
# Requires Inno Setup Compiler
# Run Inno Setup with installer_setup.iss
```

## 📁 Project Structure

```
simple_pdf_splitter/
├── main_gui.py                    # Application entry point
├── src/
│   ├── gui/                       # PyQt6 GUI components
│   │   ├── main_window_clean.py   # Main application window
│   │   ├── widgets/               # Custom widgets
│   │   └── dialogs/               # Dialog windows
│   ├── services/                  # Business logic
│   │   ├── pdf_service.py         # PDF operations
│   │   └── pdf_processor.py       # Processing engine
│   └── config/                    # Configuration
│       └── settings.py            # Application settings
├── static/                        # Static resources
│   └── images/                    # Icons and banners
└── requirements.txt               # Python dependencies
```

## 🎨 User Interface

The application features a clean, professional interface:
- **Header**: Application branding and version
- **File Selection**: Large drop zone for PDF files
- **Configuration Panel**: Client and case information
- **Split Configuration**: Dynamic list of split sections
- **Action Buttons**: Clear Run Split and Add Split buttons
- **Status Area**: Real-time processing feedback

## 🔧 Troubleshooting

### Common Issues

**Windows Security Warning**
- This is normal for downloaded executables
- Click "More info" then "Run anyway"

**PDF Won't Load**
- Ensure the PDF is not password protected
- Check that the file is not corrupted
- Try copying the PDF to a different location

**Application Won't Start**
- Ensure Windows 10 or later
- Check that you have sufficient disk space
- Try running as Administrator

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Maximum 200 lines per class
- Maximum 20 lines per method
- Clear, descriptive variable names
- Comment complex logic

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No liability
- ❌ No warranty

**The software is provided "as is", without warranty of any kind.**

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI
- PDF processing powered by [PyMuPDF](https://pymupdf.readthedocs.io/)
- Icon design by [Icons8](https://icons8.com)
- Designed for legal professionals by legal professionals

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/wallst-code/simple-pdf-splitter/issues)
- Check existing issues for solutions
- Provide detailed error descriptions

## 🚀 Future Enhancements

Planned features for future releases:
- [ ] Mac and Linux support
- [ ] PDF merging capabilities
- [ ] Bookmark preservation
- [ ] OCR support for scanned documents
- [ ] Custom output folder selection
- [ ] Page rotation and reordering
- [ ] Batch file processing

---

**Simple PDF Splitter** - Professional PDF splitting for legal professionals
*Version 1.0.0*

Made with ❤️ for the legal community