# CADence

ESC 2024 CCS Guideline-Based Probability Calculator for Coronary Artery Disease

## Overview

CADence is a clinical decision support tool that helps clinicians assess the probability of coronary artery disease based on the latest ESC guidelines. It integrates patient characteristics, risk factors, and test results to provide evidence-based recommendations.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cadence.git
cd cadence
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Structure

The application is organized into several modules:
- `src/components/`: UI components
- `src/constants/`: Constant values and configurations
- `src/state/`: State management
- `src/utils/`: Utility functions and calculations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Dr. U Bhalraam MBChB, BMSc, MRCP