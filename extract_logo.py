from PIL import Image

img = Image.open(r"C:\Users\baris.savran\.gemini\antigravity-ide\brain\1014c0af-7350-4865-9238-120872e52064\.user_uploaded\media_1790326286247.jpg").convert("RGBA")

# Remove background (paper texture)
# The paper is around (236, 237, 231)
datas = img.getdata()
new_data = []
for item in datas:
    r, g, b, a = item
    # If it's mostly white/gray/cream, make it transparent
    # The gold leaf is around (180, 150, 80), so checking for R,G,B all > 180 is safe.
    if r > 180 and g > 180 and b > 180:
        new_data.append((255, 255, 255, 0))
    else:
        # To avoid white halos, we can blend or just keep it.
        # Simple thresholding for now
        new_data.append(item)

img.putdata(new_data)

# Crop the bounding box
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

# The user might want the logo to be nicely scaled.
# We'll just save it as is.
img.save("logo.png")
print("New logo extracted and saved as logo.png with transparent background")
