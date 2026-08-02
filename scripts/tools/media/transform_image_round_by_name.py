import os
from PIL import Image, ImageOps, ImageDraw

def process_icon(input_path, radius_ratio=0.2, make_circle=False):
    # Open the image and convert to RGBA
    img = Image.open(input_path).convert("RGBA")
    size = img.size
    
    # Create a mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    
    if make_circle:
        # Full circular crop
        draw.ellipse((0, 0) + size, fill=255)
    else:
        # Rounded corners (Apple/Android style)
        # radius is a percentage of the shortest side
        radius = int(min(size) * radius_ratio)
        draw.rounded_rectangle((0, 0) + size, radius=radius, fill=255)
    
    # Apply the mask
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    
    # Generate output filename
    base, _ = os.path.splitext(input_path)
    suffix = "_circle" if make_circle else "_rounded"
    output_path = f"{base}{suffix}.png"
    
    output.save(output_path, "PNG")
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    target = "01_icon.jpeg"
    if os.path.exists(target):
        # Create a standard rounded version
        process_icon(target, radius_ratio=0.18) # ~iOS style
        # Create a full circle version
        process_icon(target, make_circle=True)
    else:
        print(f"File {target} not found in current directory.")