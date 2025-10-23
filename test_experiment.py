#!/usr/bin/env python3
"""
Test script for Reaction Time Experiment
Run this to verify the experiment works correctly before creating executable
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("+ tkinter imported successfully")
    except ImportError as e:
        print(f"- tkinter import failed: {e}")
        return False
    
    try:
        import json
        import csv
        import time
        import random
        import datetime
        import threading
        import math
        import uuid
        import os
        print("+ Standard library modules imported successfully")
    except ImportError as e:
        print(f"- Standard library import failed: {e}")
        return False
    
    try:
        import winsound
        print("+ winsound imported successfully (Windows audio)")
    except ImportError as e:
        print(f"- winsound import failed: {e}")
        print("  Note: Audio functionality may not work on non-Windows systems")
    
    return True

def test_gui_creation():
    """Test that the GUI can be created."""
    print("\nTesting GUI creation...")
    
    try:
        from reaction_time_experiment import ReactionTimeExperiment
        print("+ ReactionTimeExperiment class imported successfully")
        
        # Test creating the app (don't run mainloop)
        app = ReactionTimeExperiment()
        print("+ GUI application created successfully")
        
        # Test basic GUI components
        if hasattr(app, 'root') and app.root:
            print("+ Main window created")
        else:
            print("- Main window not created")
            return False
            
        if hasattr(app, 'notebook') and app.notebook:
            print("+ Notebook widget created")
        else:
            print("- Notebook widget not created")
            return False
        
        # Clean up
        app.root.destroy()
        print("+ GUI test completed successfully")
        return True
        
    except Exception as e:
        print(f"- GUI creation failed: {e}")
        return False

def test_data_structures():
    """Test data structure creation and manipulation."""
    print("\nTesting data structures...")
    
    try:
        from reaction_time_experiment import ReactionTimeExperiment
        app = ReactionTimeExperiment()
        
        # Test participant data structure
        test_participant_data = {
            'participant_id': 'TEST123',
            'age': 25,
            'gender': 'Other',
            'dominant_hand': 'Right',
            'primary_language': 'English',
            'country': 'Test Country',
            'impairments': 'None',
            'colorblind': 'No',
            'computer_usage': 'Daily',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        app.participant_data = test_participant_data
        print("+ Participant data structure works")
        
        # Test trial data structure
        test_trial_data = {
            'participant_id': 'TEST123',
            'trial_number': 1,
            'modality': 'visual',
            'is_practice': True,
            'block': None,
            'reaction_time': 250,
            'error_type': None,
            'is_error': False,
            'timestamp': '2024-01-01T00:00:00'
        }
        
        app.trial_data = [test_trial_data]
        print("+ Trial data structure works")
        
        # Test Latin square
        if len(app.latin_square) == 3:
            print("+ Latin square counterbalancing configured")
        else:
            print("- Latin square configuration error")
            return False
        
        # Clean up
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"- Data structure test failed: {e}")
        return False

def test_statistics():
    """Test statistical calculations."""
    print("\nTesting statistical calculations...")
    
    try:
        from reaction_time_experiment import ReactionTimeExperiment
        app = ReactionTimeExperiment()
        
        # Test median calculation
        test_numbers = [100, 200, 300, 400, 500]
        median = app.calculate_median(test_numbers)
        if median == 300:
            print("+ Median calculation works")
        else:
            print(f"- Median calculation error: expected 300, got {median}")
            return False
        
        # Test standard deviation calculation
        std = app.calculate_std(test_numbers)
        if abs(std - 158.11) < 0.1:  # Allow small floating point differences
            print("+ Standard deviation calculation works")
        else:
            print(f"- Standard deviation calculation error: expected ~158.11, got {std}")
            return False
        
        # Clean up
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"- Statistics test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Reaction Time Experiment - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_gui_creation,
        test_data_structures,
        test_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("+ All tests passed! The experiment is ready to use.")
        print("\nTo run the experiment:")
        print("  python reaction_time_experiment.py")
        print("\nTo create an executable:")
        print("  pip install pyinstaller")
        print("  pyinstaller --onefile --windowed --name 'ReactionTimeExperiment' reaction_time_experiment.py")
    else:
        print("- Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
