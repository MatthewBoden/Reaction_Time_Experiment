# Create Executable Instructions

## Quick Start
To create a standalone executable for the Reaction Time Experiment:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "ReactionTimeExperiment" reaction_time_experiment.py
```

## Detailed Instructions

### 1. Prepare Environment
```bash
# Install Python 3.7+ if not already installed
# Download from https://python.org

# Install required packages
pip install pyinstaller
```

### 2. Create Executable
```bash
# Basic executable (recommended for research)
pyinstaller --onefile --windowed --name "ReactionTimeExperiment" reaction_time_experiment.py

# Alternative with icon (if you have an icon file)
pyinstaller --onefile --windowed --icon=icon.ico --name "ReactionTimeExperiment" reaction_time_experiment.py

# Debug version (shows console output)
pyinstaller --onefile --name "ReactionTimeExperiment" reaction_time_experiment.py
```

### 3. PyInstaller Options Explained
- `--onefile`: Creates a single executable file
- `--windowed`: Hides console window (recommended for GUI apps)
- `--name`: Sets the output filename
- `--icon`: Adds custom icon (optional)

### 4. Output Location
The executable will be created in:
```
dist/ReactionTimeExperiment.exe
```

### 5. Distribution
- Copy the `.exe` file to target computers
- No Python installation required on target machines
- Ensure Windows audio is working for auditory stimuli

### 6. Testing
Before distributing:
1. Test on a clean Windows machine
2. Verify audio functionality
3. Test data export features
4. Check timing precision

### 7. Advanced Options
```bash
# Include additional files
pyinstaller --onefile --windowed --add-data "config.ini;." reaction_time_experiment.py

# Exclude unnecessary modules (smaller file size)
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy reaction_time_experiment.py

# Create installer (requires additional tools)
pyinstaller --onefile --windowed --name "ReactionTimeExperiment" reaction_time_experiment.py
# Then use NSIS or Inno Setup to create installer
```

### 8. Troubleshooting
- **Large file size**: Use `--exclude-module` to remove unused packages
- **Audio not working**: Ensure `winsound` module is included
- **Slow startup**: Normal for PyInstaller executables
- **Antivirus warnings**: Common with PyInstaller; may need to whitelist

### 9. File Size Optimization
```bash
# Minimal executable (excludes optional modules)
pyinstaller --onefile --windowed --exclude-module numpy --exclude-module pandas --exclude-module matplotlib --name "ReactionTimeExperiment" reaction_time_experiment.py
```

### 10. Professional Distribution
For research environments:
1. Create executable as above
2. Test thoroughly on target systems
3. Create installation package with NSIS/Inno Setup
4. Include user manual and troubleshooting guide
5. Set up data collection server if needed
