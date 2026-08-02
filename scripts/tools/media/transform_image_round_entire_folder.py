import os
from PIL import Image, ImageOps, ImageDraw

def process_icon(input_path, radius_ratio=0.2, make_circle=False):
    try:
        img = Image.open(input_path).convert("RGBA")
        size = img.size
        
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        
        if make_circle:
            draw.ellipse((0, 0) + size, fill=255)
        else:
            radius = int(min(size) * radius_ratio)
            draw.rounded_rectangle((0, 0) + size, radius=radius, fill=255)
        
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        
        base, _ = os.path.splitext(input_path)
        suffix = "_circle" if make_circle else "_rounded"
        output_path = f"{base}{suffix}.png"
        
        output.save(output_path, "PNG")
        print(f"✅ Processed: {output_path}")
    except Exception as e:
        print(f"❌ Could not process {input_path}: {e}")

if __name__ == "__main__":
    # Get all files in current directory
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    files = [f for f in os.listdir('.') if f.lower().endswith(valid_extensions)]
    
    if not files:
        print("No image files found in the current directory.")
    else:
        for image_file in files:
            # Skip files we already processed in previous runs
            if "_rounded" in image_file or "_circle" in image_file:
                continue
                
            print(f"Targeting: {image_file}")
            # Create a standard rounded version (~iOS style)
            process_icon(image_file, radius_ratio=0.18)
            # Create a full circle version
            process_icon(image_file, make_circle=True)