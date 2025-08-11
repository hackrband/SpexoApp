### Updated Full Requirements for the App:

1. **Platform**: Desktop app for macOS and Windows.
2. **Data Source**: User-provided CSV file with the following columns:
   - **Project ID**
   - **Project Name**
   - **Stock**
   - **Project Permalink**
   - **Author**
   - **Part Number**
   - **Part Name**
   - **Quantity**
   - **Part Permalink**
3. **Project Identification**:
   - A new project starts when the program encounters the next filled **Project ID** cell.
   - Rows without a **Project ID** are treated as part of the current project.
4. **Inputs**:
   - User-specified image (.png/.jpg).
   - CSV file containing the project and part data.
   - Optional prefix and suffix for output filenames.
5. **Project Selection**:
   - User can input comma-separated project IDs to process individually.
   - Option to select "All Projects" to process every project in the CSV file.
6. **Functionality**:
   - Parse the CSV to retrieve parts for each project.
   - Handle multiple parts:
     - Display all parts for a project as bullet points.
     - If more than 5 parts, split them into batches of 5 per image.
     - Combine the last batch with the previous one if it contains only 1 part.
   - Export images with filenames: `prefix + project ID + suffix`, appending `-01`, `-02`, etc., for batches.
7. **Image Specifications**:
   - Input image: Square or cropped to square by the app.
   - Max input size: 2 MB.
   - Output image: 1080x1080 px, 72 dpi.
8. **Layout**:
   - Window size: 1900x1080px.
   - Text fields with a 100px margin on all sides.
9. **Preview and Adjustments**:
   - Provide a live preview of the image with adjustable sliders for:
     - Gaussian blur (0–100).
     - Darkening (0–100).
10. **Output Workflow**:
    - Show the final image preview after adjustments.
    - Allow the user to save or cancel:
      - If saving, prompt for file location and save.
      - If canceling, confirm the action and return to the main screen.
