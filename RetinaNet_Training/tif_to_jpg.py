from PIL import Image
import os

def convert_tif_to_jpg(input_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output folder '{output_folder}' is ready.")
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        print(f"Checking file: {filename}")
        if filename.lower().endswith(".tif") or filename.lower().endswith(".tiff"):
            print(f"Processing file: {filename}")
            # Construct full file path
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.rsplit('.', 1)[0] + '.jpg')
            
            try:
                # Open the .tif image
                with Image.open(input_path) as img:
                    print(f"Opened {input_path}")
                    # Convert to RGB mode if necessary
                    if img.mode in ("RGBA", "P"):
                        print(f"Converting {input_path} to RGB mode")
                        img = img.convert("RGB")
                    # Save the image in .jpg format
                    img.save(output_path, "JPEG")
                print(f"Converted {input_path} to {output_path}")
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")

# Example usage:
input_folder = '/home/arismita/ML/yolov5_training/landcover/test/images'  # Update this path
output_folder = '/home/arismita/ML/RetinaNet/landcover/testing code/JPEGImages'  # Update this path
convert_tif_to_jpg(input_folder, output_folder)
