Smart Waste Management System - Chennai

Overview

An IoT-based waste management solution for Chennai, using sensors to monitor bins, optimize collection routes, classify waste, and engage citizens, creating a sustainable infrastructure.

Features
•	Real-time Bin Monitoring: Detect fill levels and odors, with status updates.
•	Admin Dashboard: Optimize routes, monitor bin status, and manage vehicles.
•	Waste Classification: AI-powered waste type identification and disposal guidelines.
•	Location Services: Locate bins via pincode and display availability.

Technical Architecture

Hardware
•	ESP32 Microcontroller
•	HC-SR04 Ultrasonic Sensor
•	MQ137 Gas Sensor
•	LED Indicators

Software Stack
•	Frontend: HTML5, Tailwind CSS, JavaScript
•	Backend: Express.js
•	Mapping: Leaflet.js
•	Real-time Updates: WebSocket

Requirements

Hardware
•	ESP32 Development Board, Ultrasonic Sensor, Gas Sensor, LEDs, Wires, Power Supply

Software
•	Node.js, npm, Arduino IDE

Dependencies
{
  "express": "^4.17.1",
  "socket.io": "^4.0.0",
  "leaflet": "^1.7.1",
  "tailwindcss": "^2.0.0"
}

Installation & Setup

1.	Clone Repo:
2.	git clone https://github.com/[username]/smart-waste-management
3.	cd smart-waste-management
4.	Install Dependencies:
5.	npm install
6.	Configure Hardware:
o	Update WiFi and server URL in sensor.cpp
o	Flash the ESP32 using Arduino IDE
7.	Start Server:
8.	npm start
9.	Access:
o	Admin: http://localhost:3000/adminportal.html
o	Classification: http://localhost:3000/classification.html
o	Location: http://localhost:3000/locate.html


Usage
•	Admin Portal: Monitor and optimize collection routes.
•	Citizen Interface: Find bins, upload waste images, and get guidelines.
•	Sensor Setup: Connect and power up the system.

