# DynamicRAISS-VehicleSafety
A dynamic perception-driven framework that proactively protects Vulnerable Road Users (VRUs)-especially pedestrians integrating real-time object detection, intent estimation, risk scoring, and control simulation into a unified safety system in EVs &amp; autonomous vehicles. Product under company--Leameng Solutions Technologies (LeSo).
The following is the Technical Product report (Unpublished draft) of the project. [Technical Report](https://github.com/kaustuv-d/DynamicRAISS-VehicleSafety/blob/main/DRAISS_VRU_draft02.pdf) 

# DRAISS-VRU: Dynamic Risk-Aware Intent Sensing & Simulation for Vulnerable Road Users
**Affiliations:**  
- Indian Institute of Technology Indore  
- Leameng Solution Technologies (LeSo)  

---

## 📘 Overview

**DRAISS-VRU** is a dynamic perception-driven framework that proactively protects Vulnerable Road Users (VRUs)—especially pedestrians—by integrating:

- **Real-time object detection**
- **Intent estimation**
- **Risk scoring**
- **Override control simulation**
- **Acoustic warning system**

This project simulates a unified safety system specifically designed for **Electric Vehicles (EVs)** and **Autonomous Vehicles (AVs)** using MATLAB Simulink.

> 📄 This repository hosts the **technical project files**, including:
- MATLAB `.slx` simulation model
- Python code for risk estimation
- AVAS logic design
- Technical Report (Unpublished Draft)

---

## 🎯 Key Features

### 1. **Perception Layer (YOLOv8-based)**
- Real-time pedestrian detection from camera feed using YOLOv8.
- Supports bounding box extraction and zone classification.
- Configurable for integration with LiDAR and RADAR (future upgrade).

### 2. **Intent Estimation**
- Zone-based logic (crosswalk, curbside, approach angle).
- Movement tracking to determine if a pedestrian intends to cross.

### 3. **Risk Scoring Engine**
- Python-based model using **XGBoost** classifier.
- Calculates risk levels based on velocity, intent, and proximity.
- Integrated into Simulink via MATLAB Function Block using `py.*`.

### 4. **Simulink-Based Simulation**
- Simscape vehicle modeling for kinematic behavior.
- Real-time simulation of vehicle override based on risk.
- Full vehicle path behavior simulation using input from the risk model.

### 5. **AVAS (Acoustic Vehicle Alerting System)**
- Dynamic AVAS tone modulation (volume + frequency) based on:
  - Risk level
  - Pedestrian distance
  - Intent probability
- Based on **AIS 138** standards for quiet EV pedestrian alerts.

---
## 🧠 System Architecture
![Alt](Logic Flow Chart.png)
