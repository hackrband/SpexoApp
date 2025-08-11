### Full Preparations and Steps to Build the App from Scratch in Python

Here’s a complete overview of everything you need to set up and implement the app:

---

#### **Step 1: Environment Setup**

1. **Install Python**:
   - Ensure Python (3.7 or later) is installed on your machine. Download it from [python.org](https://www.python.org/).
   - Install `pip` (Python’s package installer) if not already included.

2. **Install Required Libraries**:
   - Use `pip` to install the following dependencies:
     ```bash
     pip install pandas Pillow tk
     ```

3. **Set Up a Working Directory**:
   - Create a folder to store your project files (e.g., `OvertextApp`).

4. **Prepare the CSV File**:
   - Ensure the CSV file adheres to your updated column format:
     - **Project ID, Project Name, Stock, Project Permalink, Author, Part Number, Part Name, Quantity, Part Permalink**.
   - Save this file in your working directory for testing.

---

#### **Step 2: Design the App Flow**

1. **Input Requirements**:
   - A CSV file containing project data.
   - A user-specified image file.
   - Optional prefix and suffix for filenames.

2. **Outputs**:
   - One or more images per project, exported with appropriate file names.

3. **Workflow**:
   - Step 1: User selects the CSV file and image file.
   - Step 2: User selects specific projects or "All Projects."
   - Step 3: Preview the image with options for cropping, blur, and darkening adjustments.
   - Step 4: Save or cancel.

---

#### **Step 3: Build the GUI**

1. **Use Tkinter for GUI**:
   - Design a window to:
     - Accept file inputs (CSV and image).
     - Input prefix and suffix.
     - Select projects or "All Projects."
   - Add sliders for blur and darkening adjustments.
   - Include a preview pane for the adjusted image.
   - Add buttons for save and cancel functionality.

---

#### **Step 4: Implement CSV Parsing**

1. **Read the CSV File**:
   - Use `pandas` to read and process the data.
2. **Identify Projects**:
   - Detect new projects by reading the next filled **Project ID** cell.
3. **Group Rows**:
   - Group rows belonging to the same project for batch processing.

---

#### **Step 5: Image Manipulation**

1. **Load the Image**:
   - Use `Pillow` to open the image file.
2. **Interactive Cropping**:
   - Use Tkinter’s `Canvas` for drag-and-zoom functionality.
3. **Apply Adjustments**:
   - Gaussian blur and darkening with adjustable sliders.
4. **Overlay Text**:
   - Add part details as bullet points on the image.

---

#### **Step 6: Export Functionality**

1. **File Naming**:
   - Generate file names based on the format `prefix + project ID + suffix`, appending `-01`, `-02`, etc., for batches.
2. **Save Files**:
   - Allow the user to select the save location using a file dialog.

---

#### **Step 7: Testing**

1. **Test CSV Parsing**:
   - Test the logic for identifying new projects and grouping rows by Project ID.
2. **Test GUI**:
   - Verify all input fields, sliders, and buttons function correctly.
3. **Test Image Processing**:
   - Ensure cropping, blur, darkening, and text overlay work as expected.
4. **Test File Export**:
   - Confirm files are named and saved correctly.

---

#### **Step 8: Deployment**

1. **Package the App**:
   - Use `PyInstaller` to bundle your app into an executable for macOS and Windows.
     ```bash
     pip install pyinstaller
     pyinstaller --onefile your_script.py
     ```
2. **Distribute**:
   - Share the executable or provide the script with instructions for dependencies.

---

### Summary of Tools and Libraries:

1. **Python Libraries**:
   - `pandas` (CSV parsing and grouping).
   - `Pillow` (image manipulation).
   - `tkinter` (GUI).
2. **Development Tools**:
   - IDE: PyCharm, VS Code, or any text editor.
   - Command Line: For running the script and installing dependencies.
3. **File Requirements**:
   - A sample CSV file for testing.
   - An image file for testing the cropping and overlay functionality.