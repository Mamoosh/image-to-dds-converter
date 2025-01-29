# Image to DDS Converter

I had trouble converting image files to DDS with DXT1, DXT3, DXT5 versions and couldn't batch convert them. This code allows you to easily convert single files or multiple files in a folder to DDS format with different compression options.

## Features 🚀

- User-friendly GUI built with PyQt6
- Support for PNG, JPG, JPEG, and SVG image formats
- Multiple DDS compression options (DXT1, DXT3, DXT5)
- Single file or batch folder conversion
- Progress bar for conversion tracking
- Multithreaded image processing
- Modern and clean interface

## Prerequisites 📋

Before using the application, make sure you have:

1. Python 3.8 or higher
2. Required libraries:
```bash
pip install PyQt6
pip install Pillow
```

3. Download and install texconv:
   - Go to [DirectXTex releases page](https://github.com/microsoft/DirectXTex/releases/)
   - Download texconv.exe
   - Place it in your application directory

## Installation 🔧

1. Clone the repository:
```bash
git clone https://github.com/Mamoosh/image-to-dds-converter.git
cd image-to-dds-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage Guide 📖

1. Launch the application
2. Select DDS compression type (DXT1, DXT3, or DXT5)
3. For single file conversion:
   - Click "Select File"
   - Choose your image file
   - Select output directory
4. For batch conversion:
   - Click "Select Folder"
   - Choose folder containing images
   - Select output directory
5. Monitor progress through the progress bar

## Project Structure 📁

```
image-to-dds-converter/
│
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
├── texconv.exe         # DDS conversion tool
└── README.md           # Documentation
```

## Features in Detail ⚙️

- **Multiple Format Support**: Convert PNG, JPG, JPEG, and SVG images
- **Compression Options**: Choose between DXT1, DXT3, and DXT5 compression
- **Batch Processing**: Convert multiple files at once
- **Progress Tracking**: Real-time conversion progress display
- **Error Handling**: Comprehensive error messages
- **Multithreading**: Background processing to keep UI responsive

## Contributing 🤝

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Error Handling 🔍

The application includes robust error handling for:
- Missing texconv executable
- Invalid input files
- Conversion failures
- File permission issues
- Disk space problems

## Technical Details 🔧

- Built with PyQt6 for the GUI
- Uses Microsoft's texconv for DDS conversion
- Supports multithreaded processing
- Handles various image formats through PIL
- Efficient memory management for large files
