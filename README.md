# 🕉️ Hotel Ujjain Concierge

A spiritual hotel concierge application for Ujjain, featuring **Nandi**, a warm and respectful virtual concierge designed to serve pilgrims visiting the sacred city.

## Features

### Guest Mode
- **Chat with Nandi**: Your virtual concierge who provides:
  - Temple timings and information (Mahakal, Kal Bhairav, Harsiddhi, Mangalnath, etc.)
  - Local guidance (distances, auto fares, shopping)
  - Spiritual information (mantras, customs)
  - Hotel amenities (WiFi, breakfast, checkout)
- **Service Requests**: Submit requests for towels, water, cleaning, and other services

### Manager Mode
- View all pending service requests
- Mark requests as completed
- Secure password protection

## Technology Stack

- **Framework**: Streamlit
- **Database**: SQLite3
- **Styling**: Custom CSS with Dharmic theme (Saffron & Cream colors)
- **Fonts**: Google Fonts (Cinzel, Lato)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd azimuthal-pinwheel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Configuration

The app is configured to always display in Light Mode with the Saffron theme, regardless of device settings. See `.streamlit/config.toml` for theme configuration.

## Manager Access

To access Manager Mode:
1. Click the toggle button in the top-left corner
2. Select "Manager Mode" from the sidebar
3. Enter password: `MahakalAdmin`

## Design Philosophy

The app features a "Dharmic" aesthetic:
- **Colors**: Cream background (#FFFBF0), Saffron accents (#FF9933), Maroon headings (#800000)
- **Typography**: Elegant serif headers (Cinzel) with clean body text (Lato)
- **Spiritual Elements**: Om symbol (🕉️), Namaste emoji (🙏)

---

**Jai Mahakal! 🕉️**
