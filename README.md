# WgStatus Project

WgStatus is a Python project that provides real-time updates on the status of WireGuard connections through a web interface. The application is built using Flask and utilizes HTML, CSS, and JavaScript for a responsive user experience.

## Project Structure

```
WgStatus
├── src
│   ├── app.py                # Entry point of the application
│   ├── templates
│   │   └── index.html        # HTML template for the web interface
│   ├── static
│   │   ├── css
│   │   │   └── styles.css     # CSS styles for the application
│   │   └── js
│   │       └── scripts.js      # JavaScript for real-time updates
│   ├── utils
│   │   ├── __init__.py        # Package initialization
│   │   ├── csv_utils.py       # Utilities for handling CSV files
│   │   └── wg_utils.py        # Utilities for WireGuard commands
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/CarrotHuerta/WgStatus
   cd WgStatus
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

The application will start a web server, and you can access the interface by navigating to `http://yourserverip:5000` in your web browser.
