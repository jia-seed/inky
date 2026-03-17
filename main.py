import gc
import time
import jpegdec
import uos
import machine
from picographics import PicoGraphics, DISPLAY_INKY_FRAME as DISPLAY

# How often to auto-switch images (in seconds)
CYCLE_SECONDS = 30  # 30 seconds

# Set up the display
graphics = PicoGraphics(DISPLAY)
j = jpegdec.JPEG(graphics)

# Buttons: A=next, B=previous
button_a = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)

# Get list of JPEG images sorted
IMAGE_DIR = "/images"
images = sorted([f for f in uos.listdir(IMAGE_DIR) if f.endswith(".jpg")])
print(f"Found {len(images)} images: {images}")

if len(images) == 0:
    raise RuntimeError("No .jpg files found in /images/")

idx = 0

def show_image(index):
    filename = IMAGE_DIR + "/" + images[index]
    print(f"Displaying: {filename} ({index + 1}/{len(images)})")
    gc.collect()
    j.open_file(filename)
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
    graphics.update()

# Show first image
show_image(idx)

last_change = time.ticks_ms()

while True:
    # Button A = next image
    if button_a.value() == 0:
        idx = (idx + 1) % len(images)
        show_image(idx)
        last_change = time.ticks_ms()
        time.sleep(0.5)  # debounce

    # Button B = previous image
    if button_b.value() == 0:
        idx = (idx - 1) % len(images)
        show_image(idx)
        last_change = time.ticks_ms()
        time.sleep(0.5)  # debounce

    # Auto-cycle
    if time.ticks_diff(time.ticks_ms(), last_change) > CYCLE_SECONDS * 1000:
        idx = (idx + 1) % len(images)
        show_image(idx)
        last_change = time.ticks_ms()

    time.sleep(0.1)

