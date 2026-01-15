import cv2
import serial
from ultralytics import YOLO
from twilio.rest import Client
import time
import threading

# ============ TWILIO CONFIGURATION ============
TWILIO_ACCOUNT_SID = '*********'  
TWILIO_AUTH_TOKEN = '***********'    
TWILIO_PHONE_NUMBER = '+1234567890'           
ALERT_PHONE_NUMBER = '+91844######'            

# Initialize Twilio Client
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✓ Twilio connected successfully!")
except Exception as e:
    print(f"⚠ Twilio connection failed: {e}")
    twilio_client = None

# ============ ARDUINO CONNECTION ============
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize
    print("✓ Arduino connected on COM3")
except:
    print("⚠ Arduino not connected. Running in simulation mode.")
    arduino = None

# ============ YOLO MODEL ============
model = YOLO("yolov8n.pt")

danger_map = {
    "dog": "LOW",
    "cat": "LOW",
    "cow": "MEDIUM",
    "horse": "MEDIUM",
    "elephant": "HIGH",
    "bear": "HIGH",
    "lion": "HIGH",
    "tiger": "HIGH"
}

# ============ GPS & ALERT SETTINGS ============
last_alert_time = {}
ALERT_COOLDOWN = 60
current_gps_location = "Location pending..."

def read_arduino_data():
    """Background thread to read GPS data from Arduino"""
    global current_gps_location
    while True:
        if arduino and arduino.in_waiting > 0:
            try:
                line = arduino.readline().decode('utf-8').strip()
                
                if line.startswith("GPS:"):
                    gps_data = line.replace("GPS:", "")
                    
                    if gps_data == "WAITING":
                        current_gps_location = "GPS acquiring signal..."
                        print("🛰 GPS acquiring satellite signal...")
                    else:
                        # Parse lat,lng
                        lat, lng = gps_data.split(",")
                        current_gps_location = f"{lat},{lng}"
                        print(f"📍 GPS Updated: {current_gps_location}")
                        print(f"   Google Maps: https://www.google.com/maps?q={lat},{lng}")
                
                elif line:  # Print other Arduino messages
                    print(f"Arduino: {line}")
                    
            except Exception as e:
                print(f"Error reading Arduino: {e}")
        
        time.sleep(0.1)

# Start GPS reading thread
if arduino:
    gps_thread = threading.Thread(target=read_arduino_data, daemon=True)
    gps_thread.start()

def send_sms_alert(animal_name, danger_level, gps_location):
    """Send SMS alert with GPS location via Twilio"""
    if not twilio_client:
        print(f"⚠ Cannot send SMS - Twilio not connected")
        return False
    
    current_time = time.time()
    
    # Check cooldown period
    if animal_name in last_alert_time:
        time_diff = current_time - last_alert_time[animal_name]
        if time_diff < ALERT_COOLDOWN:
            print(f"⏳ Alert cooldown active for {animal_name} ({int(ALERT_COOLDOWN - time_diff)}s remaining)")
            return False
    
    # Build location string
    if gps_location != "Location pending..." and gps_location != "GPS acquiring signal...":
        lat, lng = gps_location.split(",")
        location_text = f"Location: https://www.google.com/maps?q={lat},{lng}"
    else:
        location_text = f"Location: {gps_location}"
    
    try:
        message = twilio_client.messages.create(
            body=f"🚨 ANIMAL ALERT!\n\n"
                 f"Danger Level: {danger_level}\n"
                 f"Animal: {animal_name.upper()}\n"
                 f"{location_text}\n\n"
                 f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            from_=TWILIO_PHONE_NUMBER,
            to=ALERT_PHONE_NUMBER
        )
        last_alert_time[animal_name] = current_time
        print(f"✓ SMS Alert sent! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"✗ SMS sending failed: {e}")
        return False

# ============ MAIN DETECTION LOOP ============
cap = cv2.VideoCapture(0)

print("\n🎥 Camera started. Press 'q' to quit.\n")
print(f"📍 Current GPS: {current_gps_location}\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.6)
    annotated_frame = results[0].plot()

    # Process detections
    highest_danger = "LOW"
    detected_animal = None
    
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cls = int(box.cls[0])
            label = model.names[cls]
            danger = danger_map.get(label, "LOW")

            # Track highest danger level
            if danger == "HIGH":
                highest_danger = "HIGH"
                detected_animal = label
            elif danger == "MEDIUM" and highest_danger != "HIGH":
                highest_danger = "MEDIUM"
                detected_animal = label

            # ===== VISUAL DISPLAY =====
            text_y = y1 - 75
            if text_y < 20:
                text_y = y1 + 50

            # Color coding
            if danger == "HIGH":
                color = (0, 0, 255)  # Red
            elif danger == "MEDIUM":
                color = (0, 165, 255)  # Orange
            else:
                color = (0, 255, 0)  # Green

            cv2.putText(annotated_frame, f"Animal: {label}",
                        (x1, text_y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, color, 2)
            cv2.putText(annotated_frame, f"Danger: {danger}",
                        (x1, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, color, 2)

    # ===== SEND SIGNAL TO ARDUINO =====
    if arduino:
        if highest_danger == "HIGH":
            arduino.write(b'H')
        elif highest_danger == "MEDIUM":
            arduino.write(b'M')
        else:
            arduino.write(b'L')

    # ===== SEND SMS FOR HIGH DANGER =====
    if highest_danger == "HIGH" and detected_animal:
        send_sms_alert(detected_animal, highest_danger, current_gps_location)

    # Display GPS on screen
    cv2.putText(annotated_frame, f"GPS: {current_gps_location}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.imshow("Animal Detection & Alert System", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
print("\n✓ System closed successfully!")