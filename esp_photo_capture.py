import serial
import time
import cv2
import serial.tools.list_ports

# ----------------------------
# USER SETTINGS
# ----------------------------
ESP_BAUD = 115200
SAVE_PHOTO_PATH = "intruder_photo.jpg"
ESP_PORT = "COM3"     # <-- Change this if needed
# ----------------------------

# -------------------------------------------
# AUTO CHECK IF PORT EXISTS
# -------------------------------------------
def validate_port(port_name):
    available = [p.device for p in serial.tools.list_ports.comports()]
    if port_name not in available:
        print("\n❌ ERROR: Port", port_name, "not found!")
        print("Available ports:", available)
        exit()
    return True

validate_port(ESP_PORT)

# -------------------------------------------
# CONNECT TO ESP32
# -------------------------------------------
print("Connecting to ESP32 on", ESP_PORT, "...")
try:
    ser = serial.Serial(ESP_PORT, ESP_BAUD, timeout=1)
except Exception as e:
    print("\n❌ Failed to open port:", e)
    print("➡ Close Arduino Serial Monitor and try again.")
    exit()

time.sleep(2)
print("Connected!\nListening for Access Denied messages...\n")

# -------------------------------------------
# CAMERA CAPTURE FUNCTION
# -------------------------------------------
def take_photo():
    print("📸 Taking photo...")

    cam = cv2.VideoCapture(0)
    time.sleep(0.5)
    ret, frame = cam.read()
    cam.release()

    if ret:
        cv2.imwrite(SAVE_PHOTO_PATH, frame)
        print("✅ Photo saved as:", SAVE_PHOTO_PATH)
    else:
        print("❌ Camera capture failed!")

# -------------------------------------------
# MAIN LISTEN LOOP
# -------------------------------------------
while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print("ESP:", line)

            # Trigger when ESP32 sends ACCESS_DENIED
            if "ACCESS_DENIED" in line:
                take_photo()

    except KeyboardInterrupt:
        print("\nExiting program.")
        break

    except Exception as e:
        print("Error:", e)
