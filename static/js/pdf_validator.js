/**
 * Client-side PDF validation for enhanced security
 */

class PDFValidator {
    /**
     * Validate if a file is a PDF
     * @param {File} file - The file to validate
     * @returns {Object} Validation result with isValid and message
     */
    static async validatePDFFile(file) {
        // Check if file exists
        if (!file) {
            return {
                isValid: false,
                message: 'No file provided'
            };
        }

        // Check file extension
        const fileName = file.name.toLowerCase();
        if (!fileName.endsWith('.pdf')) {
            return {
                isValid: false,
                message: `Invalid file type. Expected PDF, got: ${fileName.split('.').pop() || 'unknown'}`
            };
        }

        // Check MIME type
        const validMimeTypes = [
            'application/pdf',
            'application/x-pdf',
            'application/acrobat',
            'application/vnd.pdf',
            'text/pdf',
            'text/x-pdf'
        ];

        if (!validMimeTypes.includes(file.type)) {
            // Some systems don't set MIME type correctly, so this is a warning
            console.warn(`Suspicious MIME type: ${file.type || 'none'} for file: ${file.name}`);
        }

        // Check file size (100MB max)
        const maxSize = 100 * 1024 * 1024; // 100MB in bytes
        if (file.size > maxSize) {
            return {
                isValid: false,
                message: `File too large. Maximum size is ${maxSize / (1024 * 1024)}MB, your file is ${(file.size / (1024 * 1024)).toFixed(2)}MB`
            };
        }

        // Check minimum size (10 bytes - impossibly small for a real PDF)
        if (file.size < 10) {
            return {
                isValid: false,
                message: 'File is too small to be a valid PDF'
            };
        }

        // Check file signature (magic bytes) by reading first few bytes
        try {
            const buffer = await this.readFileHeader(file);
            if (!this.checkPDFSignature(buffer)) {
                return {
                    isValid: false,
                    message: 'File does not have a valid PDF signature. This file may be corrupted or not a real PDF.'
                };
            }
        } catch (error) {
            console.error('Error reading file:', error);
            // Don't block if we can't read the file header
        }

        return {
            isValid: true,
            message: 'Valid PDF file'
        };
    }

    /**
     * Read the first few bytes of a file
     * @param {File} file - The file to read
     * @returns {Promise<ArrayBuffer>} The file header
     */
    static readFileHeader(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            const blob = file.slice(0, 8); // Read first 8 bytes
            
            reader.onload = (e) => {
                resolve(e.target.result);
            };
            
            reader.onerror = reject;
            reader.readAsArrayBuffer(blob);
        });
    }

    /**
     * Check if the buffer contains PDF signature
     * @param {ArrayBuffer} buffer - The file header buffer
     * @returns {boolean} True if PDF signature found
     */
    static checkPDFSignature(buffer) {
        const bytes = new Uint8Array(buffer);
        
        // Check for %PDF- signature (0x25 0x50 0x44 0x46 0x2D)
        if (bytes[0] === 0x25 && // %
            bytes[1] === 0x50 && // P
            bytes[2] === 0x44 && // D
            bytes[3] === 0x46) { // F
            return true;
        }
        
        return false;
    }

    /**
     * Show validation error to user
     * @param {string} message - Error message to display
     */
    static showError(message) {
        // Create a more user-friendly error display
        const errorDiv = document.createElement('div');
        errorDiv.className = 'validation-error';
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f44336;
            color: white;
            padding: 15px 20px;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.3s ease;
        `;
        errorDiv.innerHTML = `
            <strong>Invalid File</strong><br>
            ${message}
        `;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            errorDiv.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                try {
                    errorDiv.remove();
                } catch (e) {
                    // Ignore if already removed
                }
            }, 300);
        }, 5000);
    }
}

// Add animation styles if not already present
if (!document.querySelector('#pdf-validator-styles')) {
    const style = document.createElement('style');
    style.id = 'pdf-validator-styles';
    style.innerHTML = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}