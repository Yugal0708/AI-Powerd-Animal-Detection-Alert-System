# 🛡️ AI-Powered Animal Detection & Alert System  
**Preventing Human-Wildlife Conflicts Through Deep Learning & IoT**

<p align="center">
  <img src="https://via.placeholder.com/800x400/1a3c34/ffffff?text=AI+Animal+Detection+System" alt="Project Banner" width="800"/>
  <br>
  <em>Real-time dangerous wildlife detection with instant SMS alerts & GPS tracking</em>
</p>

## 🎯 Project Overview

An end-to-end **AI + IoT surveillance system** that detects dangerous wild animals (lion, tiger, leopard, elephant, bear, etc.) in real-time using computer vision and sends instant SMS alerts with GPS coordinates to prevent human-wildlife conflicts — a major issue causing **400+ annual fatalities** in India.

- **Project Type**: IoT + Computer Vision + Cloud Integration  
- **Duration**: 4 Months  
- **Role**: Lead Developer / Full-Stack AI Engineer  
- **Status**: Deployment-Ready Prototype

## 💡 Problem Statement

Human-wildlife conflicts in rural India lead to significant loss of life, livestock, crops, and retaliatory killings of endangered species. Traditional monitoring methods are expensive, manual, and ineffective at night or in remote areas.

**Goal**: Build an **affordable, autonomous, 24/7 early-warning system** for communities living near forests.

## 🔧 Technical Implementation

### AI & Machine Learning
- **Dual-Model Architecture**:
  - **YOLOv8** (Ultralytics) for real-time object detection
  - **EfficientNet-B0** (ImageNet-pretrained) for fine-grained species classification
- **Accuracy**: 95%+ in distinguishing domestic animals (cat/dog) from dangerous wildlife
- **Performance**: 30+ FPS inference with <2-second end-to-end response time
- **Smart Caching**: Custom detection cache to reduce false negatives and stabilize tracking

### Hardware & Embedded Systems
- **Arduino Uno** integration for:
  - LED indicators
  - Audio alarms
  - NEO-6M GPS module management
- **Multi-threaded GPS reading** for real-time location without blocking detection loop

### Cloud & Communication
- **Twilio SMS API** for instant alerts with Google Maps links
- **Cooldown & Priority System**: Prevents spam, escalates alerts when humans are near dangerous animals
- **Rate Limiting**: 60-second cooldown per animal type

### Computer Vision Pipeline
- **OpenCV**: Real-time video capture, annotation & display
- **PyTorch / Ultralytics**: Model inference (GPU support ready)
- **Custom Preprocessing**: Optimized resizing, normalization & augmentation

## 📊 Key Achievements

- 95%+ Detection Accuracy (very low false positives)
- <2-second Detection → Alert latency
- ~₹5,000 per unit cost — affordable for rural deployment
- 24/7 autonomous operation
- Person detection for enhanced human safety
- Scalable to multiple locations

## 🛠️ Technology Stack

| Category              | Technologies                              |
|-----------------------|-------------------------------------------|
| Languages             | Python 3.x                                |
| AI/ML                 | YOLOv8, EfficientNet-B0, PyTorch, TorchVision, Ultralytics |
| Computer Vision       | OpenCV                                    |
| Hardware              | Arduino Uno, NEO-6M GPS, USB Webcam       |
| IoT & Communication   | PySerial, Multi-threading, Twilio API     |
| Cloud                 | Twilio SMS                                |
| Development Tools     | Git, VS Code, Arduino IDE                 |

## 🌍 Real-World Impact

- **Social**: Protects rural lives, reduces retaliatory killings of wildlife
- **Environmental**: Supports conservation of endangered species
- **Economic**: Prevents crop/livestock losses worth lakhs annually
- **Scalability**: Ready for deployment in 1000+ forest-adjacent villages

## 🚀 Future Enhancements (Phase 2 Roadmap)

- Centralized cloud dashboard for multi-site monitoring
- Mobile app with live feed & alerts
- Night vision / IR camera support
- Local wildlife dataset fine-tuning
- Drone-based aerial surveillance
- Automated non-lethal deterrents (ultrasonic, lights)
- Wildlife movement pattern prediction & analytics

## 🏆 Recognition & Awards

- 📜 Presented at a regional science exhibition and recognized for design and presentation

## 📸 Project Highlights

- Real-time species-specific detection  
- GPS-enabled precise location alerts  
- Multi-channel notification (LED + Buzzer + SMS)  
- Human presence tracking for safety escalation  
- Very low-cost rural-friendly design  

## 🔗 Resources

- **GitHub Repository**: 
- **Technical Documentation**: 
- **Project Poster**: 

## 📞 Contact & Collaboration

Open to collaborations, deployments, research partnerships, and funding discussions.

- **LinkedIn**: https://www.linkedin.com/in/yugal-bilawane-1b029b32b/
- **Email**: yugalbilawane0514@gmail.com
- **GitHub**: 

> "Leveraging AI to protect lives and preserve wildlife — one detection at a time."

