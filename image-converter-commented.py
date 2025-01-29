import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog,
                           QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox,
                           QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PIL import Image
import subprocess

class ConversionWorker(QThread):
    """
    Worker thread for handling image conversion operations.
    Prevents UI freezing during long conversion processes.
    
    Signals:
        progress (int): Emits conversion progress percentage
        finished: Emits when conversion is complete
        error (str): Emits error messages during conversion
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, files, output_dir, dds_format):
        """
        Initialize the conversion worker.
        
        Args:
            files (list): List of file paths to convert
            output_dir (str): Directory for converted files
            dds_format (str): DDS compression format (DXT1/DXT3/DXT5)
        """
        super().__init__()
        self.files = files
        self.output_dir = output_dir
        self.dds_format = dds_format

    def convert_to_dds(self, input_path, output_path):
        """
        Convert a single image to DDS format using texconv.
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path for output DDS file
            
        Raises:
            Exception: If conversion fails
        """
        try:
            # Convert input to PNG first (temporary)
            img = Image.open(input_path)
            temp_png = os.path.join(self.output_dir, "temp.png")
            img.save(temp_png, "PNG")
            
            # Set compression format
            compression = "-f DXT5"  # default
            if self.dds_format == "DXT1":
                compression = "-f DXT1"
            elif self.dds_format == "DXT3":
                compression = "-f DXT3"
            elif self.dds_format == "DXT5":
                compression = "-f DXT5"
                
            # Build texconv command
            cmd = f"texconv -y {compression} -o \"{self.output_dir}\" \"{temp_png}\""
            
            # Execute conversion
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Conversion failed: {stderr.decode()}")
                
            # Cleanup: remove temporary PNG
            if os.path.exists(temp_png):
                os.remove(temp_png)
                
            # Rename output to match input filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            final_path = os.path.join(self.output_dir, f"{base_name}.dds")
            temp_dds = os.path.join(self.output_dir, "temp.dds")
            if os.path.exists(temp_dds):
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(temp_dds, final_path)
            
        except Exception as e:
            raise Exception(f"Error converting {input_path}: {str(e)}")

    def run(self):
        """
        Main worker thread function.
        Processes all files in the queue and emits progress updates.
        """
        total_files = len(self.files)
        for i, file_path in enumerate(self.files):
            try:
                # Setup output path
                filename = os.path.basename(file_path)
                name_without_ext = os.path.splitext(filename)[0]
                output_path = os.path.join(self.output_dir, f"{name_without_ext}.dds")
                
                # Convert file
                self.convert_to_dds(file_path, output_path)
                
                # Update progress
                progress = int((i + 1) / total_files * 100)
                self.progress.emit(progress)
                
            except Exception as e:
                self.error.emit(str(e))
                
        self.finished.emit()

class ImageConverterApp(QMainWindow):
    """
    Main application window for the Image to DDS converter.
    Provides a GUI for selecting and converting images to DDS format.
    """
    
    def __init__(self):
        """Initialize the main application window and UI components."""
        super().__init__()
        self.setWindowTitle("Image to DDS Converter")
        self.setMinimumSize(600, 400)
        self.setup_ui()
        
        # Verify texconv availability
        if not self.check_texconv():
            QMessageBox.critical(self, "Error", 
                "texconv not found. Please download it and place in the application directory.")
            sys.exit(1)

    def check_texconv(self):
        """
        Check if texconv is available in the system.
        
        Returns:
            bool: True if texconv is available, False otherwise
        """
        try:
            subprocess.run(["texconv", "-help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except:
            return False

    def setup_ui(self):
        """Setup all UI components and layouts."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Format selection dropdown
        format_layout = QHBoxLayout()
        format_label = QLabel("DDS Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["DXT1", "DXT3", "DXT5"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        main_layout.addLayout(format_layout)

        # File selection button
        self.file_btn = QPushButton("Select File")
        self.file_btn.clicked.connect(self.select_file)
        main_layout.addWidget(self.file_btn)

        # Folder selection button
        self.folder_btn = QPushButton("Select Folder")
        self.folder_btn.clicked.connect(self.select_folder)
        main_layout.addWidget(self.folder_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

        # Apply modern styling
        self.apply_styles()

    def apply_styles(self):
        """Apply CSS styles to UI components."""
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
                margin: 5px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                min-width: 150px;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)

    def select_file(self):
        """Handle single file selection and conversion."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.svg)"
        )
        if file_path:
            self.convert_files([file_path])

    def select_folder(self):
        """Handle folder selection and batch conversion."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder"
        )
        if folder_path:
            # Collect all image files in the folder
            image_files = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')):
                        image_files.append(os.path.join(root, file))
            
            if image_files:
                self.convert_files(image_files)
            else:
                QMessageBox.warning(self, "Error", "No image files found in the selected folder.")

    def convert_files(self, files):
        """
        Initialize and start the conversion process.
        
        Args:
            files (list): List of file paths to convert
        """
        # Get output directory
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory"
        )
        if not output_dir:
            return

        # Setup and start worker thread
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.worker = ConversionWorker(files, output_dir, self.format_combo.currentText())
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.error.connect(self.show_error)
        self.worker.start()

        # Disable buttons during conversion
        self.file_btn.setEnabled(False)
        self.folder_btn.setEnabled(False)

    def update_progress(self, value):
        """Update progress bar and status label."""
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Converting... {value}%")

    def conversion_finished(self):
        """Handle conversion completion."""
        self.progress_bar.setVisible(False)
        self.status_label.setText("Conversion completed successfully!")
        self.file_btn.setEnabled(True)
        self.folder_btn.setEnabled(True)
        QMessageBox.information(self, "Complete", "File conversion completed successfully.")

    def show_error(self, error_message):
        """Display error message to user."""
        QMessageBox.critical(self, "Error", error_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec())