import csv
from tkinter.filedialog import asksaveasfile

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, NW, ttk
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont
from matplotlib import font_manager


def parse_csv_by_project(csv_path):
    df = pd.read_csv(csv_path)
    projects = []
    current_project = None
    for _, row in df.iterrows():
        if not pd.isna(row['Project ID']):
            if current_project:
                projects.append(current_project)
            current_project = {
                'Project ID': row['Project ID'],
                'Project Name': row['Project Name'],
                'Stock': row['Stock'],
                'Project Permalink': row['Project Permalink'],
                'Author': row['Author'],
                'Parts': []
            }
        if current_project:
            current_project['Parts'].append({
                'Part Number': row['Part Number'],
                'Part Name': row['Part Name'],
                'Quantity': row['Quantity'],
                'Part Permalink': row['Part Permalink']
            })
    if current_project:
        projects.append(current_project)
    return projects

def select_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        csv_file_entry.delete(0, tk.END)
        csv_file_entry.insert(0, file_path)

def select_image_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
    if file_path:
        image_file_entry.delete(0, tk.END)
        image_file_entry.insert(0, file_path)
        update_preview_with_example()

def load_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def process_image(image_path, parts_text, blur_level, darkening_level):
    image = load_image(image_path)
    if not image:
        return None
    adjusted_image = apply_blur_and_darkening(image, blur_level, darkening_level)
    final_image = overlay_text_with_dynamic_font(adjusted_image, parts_text)
    return final_image

def apply_blur_and_darkening(image, blur_level, darkening_level):
    max_blur_radius = 50  # Maximum blur radius to achieve full blur at 100%
    blur_radius = (blur_level / 100) * max_blur_radius
    blurred = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    darkened = blurred.point(lambda p: p * (1 - darkening_level / 100))
    return darkened

def overlay_text_with_dynamic_font(image, text):
    """
    Overlays dynamic text on an image, ensuring text is properly left-aligned,
    uses Arial font when available, and dynamically resizes to fit the image.
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    margin = 100  # Left margin for proper alignment
    max_text_width = width - 2 * margin  # Maximum text width based on margins

    font_size = 150  # Start with large font size
    font_path = None  # Path to chosen font

    # Use Arial font for consistency. Fallback to default fonts if Arial is unavailable
    try:
        font_path = font_manager.findfont(font_manager.FontProperties(family="Arial"))
    except Exception:
        print("Arial not found. Attempting fallback font.")

    if not font_path:
        # Fallback to DejaVu Sans or other fonts
        for font in font_manager.findSystemFonts():
            if "dejavu sans" in font.lower() and "bold" not in font.lower() and "italic" not in font.lower():
                font_path = font
                break

    if not font_path:
        print("Warning: Unable to load Arial or fallback font. Using default system font.")
        return image

    # Dynamically adjust font size
    while font_size > 10:  # Limit minimum font size to 10
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            break

        # Split text into lines and wrap them to fit
        text_lines = text.split("\n")  # Split input into separate lines
        wrapped_lines = []
        for line in text_lines:
            words = line.split()  # Split line into words
            current_line = ""
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                # Measure line width using textbbox
                bbox = draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0]
                if text_width > max_text_width:
                    wrapped_lines.append(current_line)
                    current_line = word  # Start a new line
                else:
                    current_line = test_line
            wrapped_lines.append(current_line)  # Add the final line

        # Join wrapped lines and calculate overall text height
        total_text_height = sum(
            [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
             for line in wrapped_lines]
        ) + (len(wrapped_lines) - 1) * 10  # Add spacing between lines

        # Ensure text fits in the image
        if total_text_height <= height - 2 * margin:
            break

        # Reduce font size and try again
        font_size -= 2

    # Start drawing at the left margin
    x = margin
    # Center vertically within the image
    y = (height - total_text_height) // 2

    # Draw each line of text with strict left alignment
    current_y = y
    for line in wrapped_lines:
        draw.text((x, current_y), line, fill="white", font=font, align="left")
        current_y += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 10

    return image

def display_parts(project_name, parts):
    """
    Display project parts in batches and ensure each batch is downloaded separately.

    Args:
        project_name (str): Name of the project.
        parts (list): List of parts.
    """
    print(f"Project: {project_name}")

    # Step 1: Group parts into batches of 5
    batch_size = 5  # Number of items per batch
    if not parts:
        print("No parts available to process.")
        return  # Safeguard for empty lists

    batches = [parts[i:i + batch_size] for i in range(0, len(parts), batch_size)]

    # Step 2: Display all defined batches
    print("\nBatches:")
    for batch_num, batch in enumerate(batches, start=1):
        print(f"Batch {batch_num}: {', '.join(batch)}")

    # Step 3: Download each batch separately
    print("\nDownloading Batches Separately:")
    for batch_num, batch in enumerate(batches, start=1):
        print(f"Downloading Batch {batch_num}: {', '.join(batch)}")
        # Simulate the actual download logic
        success = download_batch(batch_num, batch)  # Replace with real download logic if needed
        if success:
            print(f"✔ Batch {batch_num} downloaded successfully.")
        else:
            print(f"✘ Batch {batch_num} failed to download.")


def download_batch(batch_num, batch):
    """
    Simulates downloading a batch (replace with actual download logic if needed).

    Args:
        batch_num (int): The batch number being downloaded.
        batch (list): List of parts in the batch.

    Returns:
        bool: True if download is successful, False otherwise.
    """
    # Simulated download (always successful here)
    print(f"Processing download for Batch {batch_num}: {', '.join(batch)}")
    return True  # Replace with success/failure logic if needed

def limit_parts_text(projects):
    # Placeholder function to handle parts text limiting logic
    # Adjust as needed for your requirements
    parts = projects[0]['Parts'][:5]  # Limit to first 5 parts
    return "\n".join([f"• {p['Quantity']} x {p['Part Name']} ({p['Part Number']})" for p in parts])

def preview_image_with_example_text():
    image_file = image_file_entry.get()
    if not image_file:
        return
    try:
        example_text = """• Example Part 01\n• Example Part 02\n• Example Part 03\n• Example Part 04\n• Example Part 05"""

        image = load_image(image_file)
        if image:
            blurred_darkened = apply_blur_and_darkening(image, blur_slider.get(), darkening_slider.get())
            preview_with_text = overlay_text_with_dynamic_font(blurred_darkened, example_text)
            preview_with_text.thumbnail((320, 320))
            img_preview = ImageTk.PhotoImage(preview_with_text)
            preview_label.config(image=img_preview)
            preview_label.image = img_preview
    except Exception as e:
        print(f"Error creating preview: {e}")

def update_preview_with_example(*args):
    preview_image_with_example_text()

def download_action():
    csv_file = csv_file_entry.get()
    image_file = image_file_entry.get()
    prefix = prefix_entry.get()
    suffix = suffix_entry.get()
    project_input = project_ids_entry.get()
    all_projects = all_projects_var.get()
    blur_level = blur_slider.get()
    darkening_level = darkening_slider.get()
    if not csv_file or not image_file:
        messagebox.showerror("Error", "Both CSV file and image file are required!")
        return
    try:
        projects = parse_csv_by_project(csv_file)
        filtered_projects = projects if all_projects else [
            project for project in projects if str(project['Project ID']) in project_input.split(",")
        ]
        for project in filtered_projects:
            parts_text = limit_parts_text([project])
            processed_image = process_image(image_file, parts_text, blur_level, darkening_level)
            if processed_image:
                file_name = generate_file_name(project['Project ID'], prefix, suffix)
                save_image(processed_image, file_name)
        messagebox.showinfo("Download Complete", f"Downloaded {len(filtered_projects)} projects.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process: {str(e)}")

def generate_file_name(project_id, prefix="", suffix=""):
    file_name = f"{prefix}{project_id}{suffix}.jpg"
    return file_name

def save_image(image, file_name):
    save_path = filedialog.asksaveasfilename(
        initialfile=file_name,
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
    )
    if save_path:
        try:
            image.save(save_path)
            print(f"Image saved as: {save_path}")
        except Exception as e:
            print(f"Error saving image: {e}")

def cancel_action():
    response = messagebox.askyesno("Cancel", "Are you sure you want to cancel?")
    if response:
        root.destroy()

def download_required_csv():
    # Sample CSV content
    sample_csv_content = """Project ID,Part Name,Stock,Project Permalink,Author,Part Number,Part Name,Quantity,Part Permalink"""

    # Open a dialog to save the file with a default filename and .csv extension
    file = asksaveasfile(
        mode="w",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="SpexoApp-SampleCSV.csv",
    )

    if file:  # If the user selects a file
        file.write(sample_csv_content)  # Write the predefined content to the file
        file.close()  # Close the file


root = tk.Tk()
root.title("SpexoApp")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame, width=400, height=800)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
left_frame.pack_propagate(False)

placeholder_image = Image.new('RGB', (1080, 1080), (169, 169, 169))
placeholder_photo = ImageTk.PhotoImage(placeholder_image)
preview_label = tk.Label(left_frame, image=placeholder_photo)
preview_label.image = placeholder_photo
preview_label.pack(pady=8)

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(right_frame, text="Select CSV File").pack(pady=4)
csv_frame = tk.Frame(right_frame)
csv_frame.pack(pady=4)
csv_file_entry = tk.Entry(csv_frame, width=48)
csv_file_entry.pack(side=tk.LEFT, padx=4)
tk.Button(csv_frame, text="Browse", command=select_csv_file).pack(side=tk.LEFT, padx=4)

tk.Label(right_frame, text="Select Image File").pack(pady=4)
image_frame = tk.Frame(right_frame)
image_frame.pack(pady=4)
image_file_entry = tk.Entry(image_frame, width=48)
image_file_entry.pack(side=tk.LEFT, padx=4)
tk.Button(image_frame, text="Browse", command=select_image_file).pack(side=tk.LEFT, padx=4)

tk.Label(right_frame, text="Prefix (Optional)").pack(pady=4)
prefix_entry = tk.Entry(right_frame, width=56)
prefix_entry.pack(pady=4)

tk.Label(right_frame, text="Suffix (Optional)").pack(pady=4)
suffix_entry = tk.Entry(right_frame, width=56)
suffix_entry.pack(pady=4)
tk.Label(right_frame, text="Project IDs (Comma-separated)").pack(pady=4)
project_ids_entry = tk.Entry(right_frame, width=56)
project_ids_entry.pack(pady=4)

all_projects_var = tk.BooleanVar()
tk.Checkbutton(right_frame, text="Process All Projects", variable=all_projects_var).pack(pady=4)

tk.Label(right_frame, text="Blur Level").pack(pady=4)
blur_slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=160, command=update_preview_with_example)
blur_slider.set(50)  # Default to 50%
blur_slider.pack(pady=4)

tk.Label(right_frame, text="Darkening Level").pack(pady=4)
darkening_slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=160, command=update_preview_with_example)
darkening_slider.set(50)  # Default to 50%
darkening_slider.pack(pady=4)

tk.Button(right_frame, text="Download", command=download_action).pack(pady=8)
tk.Button(right_frame, text="Cancel", command=cancel_action).pack(pady=8)
download_button = ttk.Button(csv_frame, text="Download Sample CSV", command=download_required_csv)
download_button.pack(side="top", pady=(5, 0))  # Slight spacing between buttons




root.mainloop()

#TODO
# 3/31 - 4/01 Download Sample
# 4/02 - 4/03 Multiple Page
# 4/04 + All Projects Option

# DONE 3/26 Left Align
# DONE 3/28 Decrease font size
