import os
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
import OpenImageIO as oiio
import PyOpenColorIO as ocio

OCIO_CONFIG_PATH = "C:/ACES/aces_1.0.3/config.ocio" #OCIO PATH IS HARD CODDED

# MAIN CLASS
class EXRtoJPGConverter(QWidget):

    # MAIN UI STARTS HERE
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EXR to JPG Converter")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        self.label = QLabel("Select a sequence of EXRs to convert")
        self.label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("Select EXR Folder")
        self.convert_button = QPushButton("Convert to JPGs")
        self.convert_button.setEnabled(False)

        self.input_color_label = QLabel("Input Color Space:")
        self.input_color_dropdown = QComboBox()
        self.input_color_dropdown.addItems(["ACEScg", "RAW"])

        self.output_color_label = QLabel("Output Display Transform:")
        self.output_color_dropdown = QComboBox()
        self.output_color_dropdown.addItems(["sRGB", "Rec709"])

        self.output_folder_label = QLabel("No output folder selected")
        self.select_output_button = QPushButton("Select Output Folder")

        layout.addWidget(self.label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.input_color_label)
        layout.addWidget(self.input_color_dropdown)
        layout.addWidget(self.output_color_label)
        layout.addWidget(self.output_color_dropdown)
        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.select_output_button)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

        self.exr_folder = ""

        self.select_button.clicked.connect(self.select_exr_folder)
        self.convert_button.clicked.connect(self.convert_exrs_to_jpg)
        self.select_output_button.clicked.connect(self.select_output_folder)

    # MAIN UI ENDS HERE

    # INPUT FOLDER SELECTION
    def select_exr_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder Containing EXRs")
        if folder:
            self.exr_folder = folder
            self.label.setText(f"Selected Folder:\n{folder}")
            self.convert_button.setEnabled(True)

    # OUTPUT FOLDER SELECTION
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Output Folder:\n{folder}")

    # CONVERSION FUNCTION
    def convert_exrs_to_jpg(self):
        exr_files = sorted([
            f for f in os.listdir(self.exr_folder)
            if f.lower().endswith(".exr")
        ])

        if not exr_files:
            QMessageBox.warning(self, "No EXRs", "No EXR files found in selected folder.")
            return

        if not self.output_folder:
            QMessageBox.warning(self, "No Output Folder", "Please select an output folder before converting.")
            return

        output_folder = self.output_folder
        os.makedirs(output_folder, exist_ok=True)

        input_space = self.input_color_dropdown.currentText()
        output_space = self.output_color_dropdown.currentText()

        for exr_file in exr_files:
            input_path = os.path.join(self.exr_folder, exr_file)
            name_only = os.path.splitext(exr_file)[0]
            output_filename = f"{input_space}_to_{output_space}_{name_only}.jpg"
            output_path = os.path.join(output_folder, output_filename)

            self.convert_linear_exr_to_display_jpg(input_path, output_path, input_space, output_space) # MAIN LOGIC FUNCTION IS CALLED HERE

        QMessageBox.information(self, "Done", f"Converted {len(exr_files)} EXRs to JPGs.\nSaved in:\n{output_folder}")



    # MAIN LOGIC FOR CONVERSION
    def convert_linear_exr_to_display_jpg(self, input_path, output_path, input_space, output_space):

        # READ EXR IMAGE USING OIIO
        input_image = oiio.ImageInput.open(input_path) #OPEN IMG
        spec = input_image.spec() #GET METADATA
        pixels = input_image.read_image(format=oiio.FLOAT) #STORES PIXEL DATA AS 32BIT FLOAT(in LINEAR)
        input_image.close()

        # CONVERTING INTO NUMPY ARRAY FOR PROCESSING AND RESHAPING THE PIXEL VALUES INTO HEIGHT, WIDTH AND CHANNELS
        image_np = np.array(pixels).reshape((spec.height, spec.width, spec.nchannels))

        rgb = image_np[:, :, :3] # GET RGB CHANNELS
        rgb = np.clip(rgb, 0.0, 1.0) # CLIPPING

        # APPLY OCIO TRANS FOR ACES CG
        if input_space == "ACEScg":
            try:
                config = ocio.Config.CreateFromFile(OCIO_CONFIG_PATH) # LOAD CONFIG

                # MAPPING INPUT & OUTPUT COLOSPACE NAMES TO CORRESPODING OCIO NAMES
                ocio_input = "ACES - ACEScg"
                ocio_output = "Output - sRGB" if output_space == "sRGB" else "Output - Rec.709"

                # PROCESSOR
                processor = config.getProcessor(ocio_input, ocio_output)
                cpu_processor = processor.getDefaultCPUProcessor() 

                buffer = rgb.astype(np.float32).reshape(-1) #FLATTEN TO 1D BUFFER (ie) IN A SINGLE 1D ARRAY
                cpu_processor.applyRGB(buffer) # INPLACE TRANSFORM AVOIDING LOOPS
                rgb = buffer.reshape(spec.height, spec.width, 3) # CONVERTING BACK TO 3D IMAGE ARRAY

            except Exception as e:
                #EXCEPTION MSG
                print("OCIO transform failed:", e)
                QMessageBox.warning(self, "OCIO Error", f"OCIO transform failed: {e}")
                return
            

        else:
            # APPLY MANUAL GAMMA CORRECTION FOR RAW (FROM LINEAR TO S-LOG CURVE)
            if output_space == "sRGB":
                rgb = np.where(rgb <= 0.0031308, 12.92 * rgb, 1.055 * np.power(rgb, 1 / 2.4) - 0.055)
            elif output_space == "Rec709":
                rgb = np.where(rgb < 0.018, 4.5 * rgb, 1.099 * np.power(rgb, 0.45) - 0.099)

        # CONVERTION TO 8-BIT JPG
        srgb_8bit = (np.clip(rgb, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)

        # JPG WRITING TO DISK
        flat_pixels = srgb_8bit.flatten()

        output_spec = oiio.ImageSpec(spec.width, spec.height, 3, oiio.UINT8)
        out = oiio.ImageOutput.create(output_path) #EMPTY JPG IMAGE CREATION

        out.open(output_path, output_spec) # OPEN EMPTY JPG
        out.write_image(flat_pixels) # WRITE PIXEL DATA
        out.close() # CLOSE


if __name__ == "__main__":      #MAIN FUNCTION
    app = QApplication([])
    window = EXRtoJPGConverter()
    window.show()
    app.exec()
