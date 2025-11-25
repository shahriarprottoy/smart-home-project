The Smart Home Controller is an interactive desktop-based application built with Flet, designed to simulate the monitoring and management of common smart-home devices. The app provides an intuitive, dashboard-style interface where users can control devices, view real-time states, explore device-specific information, and track activity logs.
Purpose
The project demonstrates how a smart home system can be represented in a user-friendly GUI with device interactions, logging, and statistics. It can serve as:
A prototype for a real home automation interface
A demo dashboard for IoT-related coursework
A foundation for integrating real hardware or APIs later

Key Features
1. Device Control Interface
The dashboard displays four devices, each with live status updates and actions:
Living Room Light — simple ON/OFF toggle
Front Door Lock — LOCK/UNLOCK control
Thermostat — adjustable temperature slider
Ceiling Fan — fan speed slider (0–3)
Each interaction updates the UI immediately and generates an entry in the action log.

2. Device Metadata & Details View

Each device has structured metadata:
Unique ID
Friendly name
Device type
Current state
Users can click Details to view:
Device metadata
A filtered history of actions related to that device
A button to return to the main overview

3. Action Logging System
Every user action is automatically recorded with:
Timestamp
Device name
Action description
User identity (“User”)

The app displays:
A recent activity panel on the Overview page
A detailed 20-entry log table on the Statistics page

4. Statistics Page
While the current version includes a simulated power consumption chart, it is structured so real data could easily be integrated later.
The page also contains a synchronized action log summary.

5. Responsive UI Layout
The interface includes:
A clean header with a logo
Easy navigation tabs (Overview / Statistics)
Color-coded device cards
Auto-updating content sections
Fixed-width centered layout for consistent appearance
Technologies Used
Python 3
Flet framework (Flutter-based UI for Python)
Datetime for real-time timestamping
Local image embedding for branding

How It Works
Device states are stored in mutable dictionaries.
UI elements (buttons, sliders, labels) are bound to handler functions.

Whenever the user interacts with a device:
State changes occur,
UI updates visually,
A log entry is created,
Log views refresh automatically.
Navigation switches content inside a shared container (body_placeholder) without recreating the entire layout.

Project Goals
Demonstrate Flet’s capabilities for building desktop app interfaces
Provide a realistic smart-home dashboard prototype
Serve as a foundation for future IoT integrations
Showcase state management, UI routing, and reactive updates
