# Reaction Time Experiment - Setup Instructions

## Overview
This is a professional research application for measuring reaction times across different stimulus modalities (visual, auditory, and combined). The experiment follows standard psychological research protocols with precise timing, data collection, and participant management.

## System Requirements
- Windows 10/11 (for audio functionality)
- Python 3.7 or higher
- Minimum 4GB RAM
- Sound card/speakers for auditory stimuli

## Installation

### Method 1: Run from Source Code
1. Install Python 3.7+ from https://python.org
2. Download the experiment files:
   - `reaction_time_experiment.py`
   - `requirements.txt`
3. Open Command Prompt/PowerShell in the experiment folder
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the experiment:
   ```bash
   python reaction_time_experiment.py
   ```

### Method 2: Create Executable (Recommended for Research)
1. Install Python and dependencies as above
2. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
3. Create executable:
   ```bash
   pyinstaller --onefile --windowed --name "ReactionTimeExperiment" reaction_time_experiment.py
   ```
4. The executable will be created in the `dist` folder
5. Distribute the `.exe` file to participants

## Experiment Protocol

### Participant Flow
1. **Consent & Demographics**: Complete informed consent and demographic questionnaire
2. **Instructions**: Read detailed task instructions
3. **Practice Trials**: 6 practice trials (2 per modality) to familiarize with task
4. **Main Experiment**: 30 trials (10 per modality) with counterbalanced block order
5. **Results**: View summary statistics and download data

### Trial Structure
- Fixation cross (+) appears
- Random foreperiod (1-3 seconds)
- Stimulus presentation:
  - Visual: Green circle flash (200ms)
  - Auditory: 1000Hz tone (200ms)
  - Combined: Both visual and auditory simultaneously
- Participant responds with spacebar
- Feedback provided (reaction time or error message)
- 1.5 second inter-trial interval

### Data Collection
- **Reaction Time**: Measured in milliseconds from stimulus onset to response
- **Error Detection**: 
  - Anticipations: RT < 100ms
  - Misses: No response within 2000ms
- **Participant Data**: Demographics, consent, timestamps
- **Export Formats**: CSV and JSON

## Counterbalancing
The experiment uses a Latin square design to counterbalance block order across participants:
- Participant 1: Visual → Auditory → Combined
- Participant 2: Auditory → Combined → Visual  
- Participant 3: Combined → Visual → Auditory

## Data Analysis
The exported data includes:
- Individual trial data with reaction times and error flags
- Summary statistics by modality
- Participant demographics
- Experiment metadata

## Troubleshooting

### Audio Issues
- Ensure Windows audio is working
- Check volume levels
- Try running as administrator if audio fails

### Timing Issues
- Close other applications to ensure precise timing
- Use a dedicated research computer if possible
- Avoid running on virtual machines

### Data Export Issues
- Ensure write permissions in the save location
- Check available disk space
- Try saving to desktop if other locations fail

## Research Ethics
- Participants must provide informed consent
- Data is collected anonymously with participant IDs
- Participants can withdraw at any time
- Data should be stored securely according to institutional guidelines

## Technical Support
For technical issues or questions about the experiment protocol, contact the research team.

## Version History
- v1.0: Initial release with full experiment protocol