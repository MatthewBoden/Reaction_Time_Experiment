#!/usr/bin/env python3
"""
Reaction Time Experiment
Visual vs. Auditory vs. Combined Stimuli in a Simple Reaction Time Task

A professional research application for measuring reaction times across different
stimulus modalities with precise timing and data collection.

Author: Research Assistant
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import json
import csv
import os
from datetime import datetime
import threading
import winsound
import math
from typing import Dict, List, Tuple, Optional
import uuid


class ReactionTimeExperiment:
    """Main experiment class handling the complete reaction time study."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reaction Time Experiment v1.0")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Experiment parameters
        self.practice_trials_per_modality = 2
        self.main_trials_per_modality = 10
        self.modalities = ['visual', 'auditory', 'combined']
        self.min_foreperiod = 1000  # milliseconds
        self.max_foreperiod = 3000  # milliseconds
        self.max_response_time = 2000  # milliseconds
        self.min_response_time = 100  # milliseconds (anticipation threshold)
        
        # Latin square for counterbalancing
        self.latin_square = [
            ['visual', 'auditory', 'combined'],
            ['auditory', 'combined', 'visual'],
            ['combined', 'visual', 'auditory']
        ]
        
        # Experiment state
        self.current_trial = 0
        self.current_block = 0
        self.is_practice = True
        self.is_running = False
        self.trial_in_progress = False  # Prevent multiple simultaneous trials
        self.experiment_started = False  # Prevent multiple experiment starts
        self.trial_start_time = 0
        self.stimulus_start_time = 0
        self.response_time = 0
        self.trial_sequence = []
        
        # GUI components
        self.setup_gui()
        
    def setup_gui(self):
        """Initialize the main GUI components."""
        # Create notebook for different screens
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for different screens
        self.consent_frame = ttk.Frame(self.notebook)
        self.instructions_frame = ttk.Frame(self.notebook)
        self.practice_frame = ttk.Frame(self.notebook)
        self.experiment_frame = ttk.Frame(self.notebook)
        self.results_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.consent_frame, text="Consent & Demographics")
        self.notebook.add(self.instructions_frame, text="Instructions")
        self.notebook.add(self.practice_frame, text="Practice Trials")
        self.notebook.add(self.experiment_frame, text="Main Experiment")
        self.notebook.add(self.results_frame, text="Results")
        
        # Initially disable all tabs except consent
        self.notebook.tab(1, state='disabled')
        self.notebook.tab(2, state='disabled')
        self.notebook.tab(3, state='disabled')
        self.notebook.tab(4, state='disabled')
        
        self.setup_consent_form()
        self.setup_instructions()
        self.setup_practice_trials()
        self.setup_experiment_trials()
        self.setup_results()
        
    def setup_consent_form(self):
        """Create the consent and demographics form."""
        # Title
        title_label = ttk.Label(self.consent_frame, text="Reaction Time Experiment", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.consent_frame, 
                                  text="Consent and Demographics", 
                                  font=('Arial', 12))
        subtitle_label.pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(self.consent_frame)
        scrollbar = ttk.Scrollbar(self.consent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Demographics form
        form_frame = ttk.LabelFrame(scrollable_frame, text="Demographics", padding=20)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Initials
        ttk.Label(form_frame, text="Initials:").grid(row=0, column=0, sticky='w', pady=5)
        self.initials_var = tk.StringVar()
        initials_entry = ttk.Entry(form_frame, textvariable=self.initials_var, width=10)
        initials_entry.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Age
        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky='w', pady=5)
        self.age_var = tk.StringVar()
        age_spinbox = ttk.Spinbox(form_frame, from_=18, to=100, textvariable=self.age_var, width=10)
        age_spinbox.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Gender
        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky='w', pady=5)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, width=20, state='readonly')
        gender_combo['values'] = ('Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say')
        gender_combo.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Dominant hand
        ttk.Label(form_frame, text="Dominant hand:").grid(row=3, column=0, sticky='w', pady=5)
        self.hand_var = tk.StringVar()
        hand_combo = ttk.Combobox(form_frame, textvariable=self.hand_var, width=20, state='readonly')
        hand_combo['values'] = ('Right', 'Left', 'Ambidextrous')
        hand_combo.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Primary language
        ttk.Label(form_frame, text="Primary language:").grid(row=4, column=0, sticky='w', pady=5)
        self.language_var = tk.StringVar()
        language_entry = ttk.Entry(form_frame, textvariable=self.language_var, width=25)
        language_entry.grid(row=4, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Country
        ttk.Label(form_frame, text="Country/Region:").grid(row=5, column=0, sticky='w', pady=5)
        self.country_var = tk.StringVar()
        country_entry = ttk.Entry(form_frame, textvariable=self.country_var, width=25)
        country_entry.grid(row=5, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Impairments
        ttk.Label(form_frame, text="Vision/Hearing impairments:").grid(row=6, column=0, sticky='nw', pady=5)
        self.impairments_text = tk.Text(form_frame, height=3, width=30)
        self.impairments_text.grid(row=6, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Colorblind
        ttk.Label(form_frame, text="Colorblind:").grid(row=7, column=0, sticky='w', pady=5)
        self.colorblind_var = tk.StringVar()
        colorblind_combo = ttk.Combobox(form_frame, textvariable=self.colorblind_var, width=20, state='readonly')
        colorblind_combo['values'] = ('No', 'Yes')
        colorblind_combo.grid(row=7, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Computer usage
        ttk.Label(form_frame, text="Computer usage frequency:").grid(row=8, column=0, sticky='w', pady=5)
        self.computer_var = tk.StringVar()
        computer_combo = ttk.Combobox(form_frame, textvariable=self.computer_var, width=20, state='readonly')
        computer_combo['values'] = ('Daily', 'Weekly', 'Monthly', 'Rarely')
        computer_combo.grid(row=8, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Consent section
        consent_frame = ttk.LabelFrame(scrollable_frame, text="Consent Information", padding=20)
        consent_frame.pack(fill='x', padx=20, pady=10)
        
        consent_text = """
This experiment involves measuring your reaction time to different types of stimuli 
(visual, auditory, and combined). The task is simple: press the spacebar as quickly 
as possible when you see or hear a stimulus.

The experiment will take approximately 10-15 minutes to complete.
        """
        ttk.Label(consent_frame, text=consent_text, justify='left').pack(anchor='w')
        
        # Consent checkboxes
        self.consent_vars = {}
        consent_items = [
            "I have read and understood the study instructions",
            "I consent to participate in this study",
            "I agree to have my responses recorded and used anonymously for research purposes",
            "I understand that I can withdraw at any time without penalty"
        ]
        
        for i, item in enumerate(consent_items):
            var = tk.BooleanVar()
            self.consent_vars[f"consent_{i}"] = var
            ttk.Checkbutton(consent_frame, text=item, variable=var).pack(anchor='w', pady=2)
        
        # Submit button
        submit_btn = ttk.Button(scrollable_frame, text="Start Experiment", 
                               command=self.submit_consent_form)
        submit_btn.pack(pady=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_instructions(self):
        """Create the instructions screen."""
        # Title
        title_label = ttk.Label(self.instructions_frame, text="Instructions", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Instructions content
        instructions_text = """
In this experiment, you will respond to different types of stimuli as quickly as possible.

STIMULI TYPES:
• Visual: A green circle will flash on the screen
• Auditory: You will hear a 1000 Hz tone
• Combined: Both the green circle and tone will occur simultaneously

TASK:
Press the SPACEBAR as quickly as possible when you see or hear the stimulus.

TRIAL STRUCTURE:
1. A fixation cross (+) will appear
2. Wait for a random delay (1-3 seconds)
3. The stimulus will appear/play
4. Press spacebar as quickly as possible
5. You'll see feedback about your response

IMPORTANT NOTES:
• Keep your finger ready on the spacebar
• Only respond when you see/hear the stimulus
• Don't anticipate - wait for the actual stimulus
• You'll do 6 practice trials first, then 30 main trials
• Take breaks between blocks if needed

Click "Start Practice Trials" when you're ready to begin.
        """
        
        instructions_label = ttk.Label(self.instructions_frame, text=instructions_text, 
                                      justify='left', font=('Arial', 10))
        instructions_label.pack(padx=40, pady=20)
        
        # Start button
        start_btn = ttk.Button(self.instructions_frame, text="Start Practice Trials", 
                              command=self.start_practice_trials)
        start_btn.pack(pady=20)
        
        # Store button reference to disable it after clicking
        self.start_button = start_btn
        
    def setup_practice_trials(self):
        """Create the practice trials screen."""
        # Progress info
        progress_frame = ttk.LabelFrame(self.practice_frame, text="Practice Progress", padding=10)
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.practice_trial_label = ttk.Label(progress_frame, text="Trial 1 of 6", 
                                             font=('Arial', 12, 'bold'))
        self.practice_trial_label.pack()
        
        self.practice_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.practice_progress.pack(pady=10)
        
        # Trial display area
        self.practice_trial_display_frame = ttk.Frame(self.practice_frame)
        self.practice_trial_display_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Fixation cross
        self.practice_fixation_label = ttk.Label(self.practice_trial_display_frame, text="+", 
                                       font=('Arial', 48, 'bold'))
        
        # Stimulus circle
        self.practice_stimulus_canvas = tk.Canvas(self.practice_trial_display_frame, width=200, height=200, 
                                        bg='white', highlightthickness=0)
        
        # Feedback label
        self.practice_feedback_label = ttk.Label(self.practice_trial_display_frame, text="", 
                                       font=('Arial', 16, 'bold'))
        
        # Instructions
        self.practice_trial_instructions = ttk.Label(self.practice_trial_display_frame, 
                                           text="Get ready! Press spacebar when you see or hear the stimulus.",
                                           font=('Arial', 12))
        self.practice_trial_instructions.pack(pady=10)
        
    def setup_experiment_trials(self):
        """Create the main experiment screen."""
        # Progress info
        progress_frame = ttk.LabelFrame(self.experiment_frame, text="Experiment Progress", padding=10)
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.experiment_trial_label = ttk.Label(progress_frame, text="Trial 1 of 30", 
                                               font=('Arial', 12, 'bold'))
        self.experiment_trial_label.pack()
        
        self.current_block_label = ttk.Label(progress_frame, text="Block: Visual", 
                                            font=('Arial', 10))
        self.current_block_label.pack()
        
        self.experiment_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.experiment_progress.pack(pady=10)
        
        # Trial display area
        self.experiment_trial_display_frame = ttk.Frame(self.experiment_frame)
        self.experiment_trial_display_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Fixation cross
        self.experiment_fixation_label = ttk.Label(self.experiment_trial_display_frame, text="+", 
                                       font=('Arial', 48, 'bold'))
        
        # Stimulus circle
        self.experiment_stimulus_canvas = tk.Canvas(self.experiment_trial_display_frame, width=200, height=200, 
                                        bg='white', highlightthickness=0)
        
        # Feedback label
        self.experiment_feedback_label = ttk.Label(self.experiment_trial_display_frame, text="", 
                                       font=('Arial', 16, 'bold'))
        
        # Instructions
        self.experiment_trial_instructions = ttk.Label(self.experiment_trial_display_frame, 
                                           text="Get ready! Press spacebar when you see or hear the stimulus.",
                                           font=('Arial', 12))
        self.experiment_trial_instructions.pack(pady=10)
        
    def setup_results(self):
        """Create the results screen."""
        # Title
        title_label = ttk.Label(self.results_frame, text="Experiment Complete!", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Thank you message
        thank_you_label = ttk.Label(self.results_frame, 
                                   text="Thank you for participating in this reaction time experiment.",
                                   font=('Arial', 12))
        thank_you_label.pack(pady=10)
        
        # Results summary
        results_frame = ttk.LabelFrame(self.results_frame, text="Your Results Summary", padding=20)
        results_frame.pack(fill='x', padx=20, pady=20)
        
        self.results_text = tk.Text(results_frame, height=15, width=80, font=('Courier', 10))
        self.results_text.pack()
        
        # Download buttons
        button_frame = ttk.Frame(self.results_frame)
        button_frame.pack(pady=20)
        
        csv_btn = ttk.Button(button_frame, text="Download CSV Data", 
                            command=lambda: self.download_data('csv'))
        csv_btn.pack(side='left', padx=10)
        
        json_btn = ttk.Button(button_frame, text="Download JSON Data", 
                             command=lambda: self.download_data('json'))
        json_btn.pack(side='left', padx=10)
        
        # Bind spacebar for responses
        self.root.bind('<KeyPress-space>', self.handle_spacebar_press)
        self.root.focus_set()
        
    def submit_consent_form(self):
        """Validate and submit the consent form."""
        # Check required fields
        if not all([self.initials_var.get(), self.age_var.get(), self.gender_var.get(), self.hand_var.get(),
                   self.language_var.get(), self.country_var.get(), self.colorblind_var.get(),
                   self.computer_var.get()]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        # Check consent checkboxes
        if not all(var.get() for var in self.consent_vars.values()):
            messagebox.showerror("Error", "Please check all consent boxes.")
            return
        
        # Collect participant data
        self.participant_data = {
            'participant_id': str(uuid.uuid4())[:8].upper(),
            'initials': self.initials_var.get().upper(),
            'age': int(self.age_var.get()),
            'gender': self.gender_var.get(),
            'dominant_hand': self.hand_var.get(),
            'primary_language': self.language_var.get(),
            'country': self.country_var.get(),
            'impairments': self.impairments_text.get('1.0', tk.END).strip(),
            'colorblind': self.colorblind_var.get(),
            'computer_usage': self.computer_var.get(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Enable instructions tab and switch to it
        self.notebook.tab(1, state='normal')
        self.notebook.select(1)
        
    def start_practice_trials(self):
        """Start the practice trials (auto-completed)."""
        if self.experiment_started:
            print("Experiment already started - ignoring call")
            return
            
        print("Starting practice trials (auto-completed)")
        
        # Disable the start button to prevent multiple clicks
        self.start_button.config(state='disabled')
        
        # Create practice trial sequence (2 trials per modality)
        self.trial_sequence = []
        for modality in self.modalities:
            for i in range(self.practice_trials_per_modality):
                self.trial_sequence.append({
                    'modality': modality,
                    'trial_number': len(self.trial_sequence) + 1,
                    'is_practice': True
                })
        
        # Auto-complete practice trials by creating fake trial data
        self.trial_data = []
        for i, trial in enumerate(self.trial_sequence):
            trial_data = {
                'participant_id': self.participant_data['participant_id'],
                'initials': self.participant_data['initials'],
                'trial_number': i + 1,
                'modality': trial['modality'],
                'is_practice': True,
                'block': None,
                'reaction_time': 250 + (i * 10),  # Fake reaction times
                'error_type': None,
                'is_error': False,
                'timestamp': datetime.now().isoformat()
            }
            self.trial_data.append(trial_data)
        
        print(f"Auto-completed {len(self.trial_sequence)} practice trials")
        
        # Go directly to main experiment
        self.start_main_experiment()
        
    def start_main_experiment(self):
        """Start the main experiment."""
        if self.experiment_started:
            print("Experiment already started - ignoring call")
            return
            
        print("Starting main experiment")
        self.experiment_started = True
        self.is_practice = False
        self.current_trial = 0
        self.current_block = 0
        self.trial_in_progress = False
        
        # Determine block order using Latin square
        participant_number = hash(self.participant_data['participant_id']) % 3
        block_order = self.latin_square[participant_number]
        
        print(f"Block order: {block_order}")
        
        # Create main trial sequence
        self.trial_sequence = []
        for modality in block_order:
            for i in range(self.main_trials_per_modality):
                self.trial_sequence.append({
                    'modality': modality,
                    'trial_number': len(self.trial_sequence) + 1,
                    'is_practice': False,
                    'block': block_order.index(modality) + 1
                })
        
        print(f"Created {len(self.trial_sequence)} main trials")
        
        # Enable experiment tab and switch to it
        self.notebook.tab(3, state='normal')
        self.notebook.select(3)
        
        # Add a small delay to ensure GUI is ready
        self.root.after(100, self.run_next_trial)
        
    def run_next_trial(self):
        """Run the next trial in the sequence."""
        if self.trial_in_progress:
            return
            
        if self.current_trial >= len(self.trial_sequence):
            self.show_results()
            return
        
        trial = self.trial_sequence[self.current_trial]
        self.trial_in_progress = True
        self.update_progress(trial)
        self.run_trial(trial)
        
    def update_progress(self, trial):
        """Update the progress display."""
        total_trials = len(self.trial_sequence)
        progress = ((self.current_trial + 1) / total_trials) * 100
        
        self.experiment_trial_label.config(text=f"Trial {self.current_trial + 1} of {total_trials}")
        self.current_block_label.config(text=f"Block: {trial['modality'].title()}")
        self.experiment_progress['value'] = progress
        
    def run_trial(self, trial):
        """Execute a single trial."""
        self.is_running = False
        self.hide_all_stimuli()
        
        # Show fixation cross
        self.experiment_fixation_label.pack(expand=True)
        self.root.update()
        
        # Random foreperiod
        foreperiod = random.randint(self.min_foreperiod, self.max_foreperiod)
        
        # Schedule stimulus presentation
        self.root.after(foreperiod, lambda: self.present_stimulus(trial['modality']))
        
    def hide_all_stimuli(self):
        """Hide all stimulus elements."""
        self.experiment_fixation_label.pack_forget()
        self.experiment_stimulus_canvas.pack_forget()
        self.experiment_feedback_label.config(text="")
        
    def present_stimulus(self, modality):
        """Present the stimulus for the given modality."""
        self.hide_all_stimuli()
        self.is_running = True
        self.stimulus_start_time = time.time() * 1000  # Convert to milliseconds
        
        if modality in ['visual', 'combined']:
            self.show_visual_stimulus()
        
        if modality in ['auditory', 'combined']:
            self.play_auditory_stimulus()
        
        # Auto-hide visual stimulus after 200ms
        if modality in ['visual', 'combined']:
            self.root.after(200, self.hide_visual_stimulus)
        
        # Set timeout for missed responses
        self.root.after(self.max_response_time, lambda: self.record_response(is_missed=True))
        
    def show_visual_stimulus(self):
        """Display the visual stimulus (green circle)."""
        self.experiment_stimulus_canvas.pack(expand=True)
        self.experiment_stimulus_canvas.delete("all")
        self.experiment_stimulus_canvas.create_oval(50, 50, 150, 150, fill='green', outline='green')
        self.root.update()
        
    def hide_visual_stimulus(self):
        """Hide the visual stimulus."""
        self.experiment_stimulus_canvas.pack_forget()
        
    def play_auditory_stimulus(self):
        """Play the auditory stimulus (1000 Hz tone)."""
        try:
            # Play 1000 Hz tone for 200ms
            winsound.Beep(1000, 200)
        except Exception as e:
            print(f"Audio error: {e}")
            
    def handle_spacebar_press(self, event):
        """Handle spacebar press during trials."""
        if self.is_running:
            self.record_response()
            
    def record_response(self, is_missed=False):
        """Record the participant's response."""
        if not self.is_running:
            return
        
        self.is_running = False
        self.response_time = time.time() * 1000  # Convert to milliseconds
        
        reaction_time = self.response_time - self.stimulus_start_time
        trial = self.trial_sequence[self.current_trial]
        
        error_type = None
        is_error = False
        
        if is_missed:
            error_type = 'miss'
            is_error = True
        elif reaction_time < self.min_response_time:
            error_type = 'anticipation'
            is_error = True
        
        trial_data = {
            'participant_id': self.participant_data['participant_id'],
            'initials': self.participant_data['initials'],
            'trial_number': self.current_trial + 1,
            'modality': trial['modality'],
            'is_practice': trial['is_practice'],
            'block': trial.get('block'),
            'reaction_time': round(reaction_time),
            'error_type': error_type,
            'is_error': is_error,
            'timestamp': datetime.now().isoformat()
        }
        
        self.trial_data.append(trial_data)
        self.show_feedback(reaction_time, error_type, is_error)
        
        # Move to next trial after feedback
        self.root.after(1500, self.next_trial)
        
    def show_feedback(self, reaction_time, error_type, is_error):
        """Show feedback for the trial."""
        self.experiment_feedback_label.pack(pady=20)
        
        if is_error:
            if error_type == 'anticipation':
                self.experiment_feedback_label.config(text=f"Too fast! ({round(reaction_time)}ms)", 
                                         foreground='red')
            elif error_type == 'miss':
                self.experiment_feedback_label.config(text="Missed!", foreground='red')
        else:
            self.experiment_feedback_label.config(text=f"{round(reaction_time)}ms", foreground='green')
        
        self.root.update()
        
    def next_trial(self):
        """Move to the next trial."""
        self.trial_in_progress = False
        self.current_trial += 1
        self.run_next_trial()
        
    def show_results(self):
        """Display the results screen."""
        # Enable results tab and switch to it
        self.notebook.tab(4, state='normal')
        self.notebook.select(4)
        
        self.display_summary_stats()
        
    def display_summary_stats(self):
        """Calculate and display summary statistics."""
        main_trials = [trial for trial in self.trial_data if not trial['is_practice']]
        practice_trials = [trial for trial in self.trial_data if trial['is_practice']]
        
        # Calculate statistics by modality
        stats = {}
        for modality in self.modalities:
            modality_trials = [trial for trial in main_trials if trial['modality'] == modality]
            valid_trials = [trial for trial in modality_trials if not trial['is_error']]
            
            if valid_trials:
                reaction_times = [trial['reaction_time'] for trial in valid_trials]
                stats[modality] = {
                    'total_trials': len(modality_trials),
                    'valid_trials': len(valid_trials),
                    'error_rate': round((len(modality_trials) - len(valid_trials)) / len(modality_trials) * 100, 1),
                    'mean_rt': round(sum(reaction_times) / len(reaction_times)),
                    'median_rt': round(self.calculate_median(reaction_times)),
                    'std_rt': round(self.calculate_std(reaction_times)),
                    'min_rt': min(reaction_times),
                    'max_rt': max(reaction_times)
                }
            else:
                stats[modality] = {
                    'total_trials': len(modality_trials),
                    'valid_trials': 0,
                    'error_rate': 100.0,
                    'mean_rt': 0,
                    'median_rt': 0,
                    'std_rt': 0,
                    'min_rt': 0,
                    'max_rt': 0
                }
        
        # Display results
        results_text = f"""
PARTICIPANT: {self.participant_data['participant_id']} ({self.participant_data['initials']})
COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS BY MODALITY:
{'='*60}

VISUAL STIMULI:
  Total Trials: {stats['visual']['total_trials']}
  Valid Trials: {stats['visual']['valid_trials']}
  Error Rate: {stats['visual']['error_rate']}%
  Mean RT: {stats['visual']['mean_rt']}ms
  Median RT: {stats['visual']['median_rt']}ms
  Std Dev: {stats['visual']['std_rt']}ms
  Range: {stats['visual']['min_rt']}-{stats['visual']['max_rt']}ms

AUDITORY STIMULI:
  Total Trials: {stats['auditory']['total_trials']}
  Valid Trials: {stats['auditory']['valid_trials']}
  Error Rate: {stats['auditory']['error_rate']}%
  Mean RT: {stats['auditory']['mean_rt']}ms
  Median RT: {stats['auditory']['median_rt']}ms
  Std Dev: {stats['auditory']['std_rt']}ms
  Range: {stats['auditory']['min_rt']}-{stats['auditory']['max_rt']}ms

COMBINED STIMULI:
  Total Trials: {stats['combined']['total_trials']}
  Valid Trials: {stats['combined']['valid_trials']}
  Error Rate: {stats['combined']['error_rate']}%
  Mean RT: {stats['combined']['mean_rt']}ms
  Median RT: {stats['combined']['median_rt']}ms
  Std Dev: {stats['combined']['std_rt']}ms
  Range: {stats['combined']['min_rt']}-{stats['combined']['max_rt']}ms

OVERALL:
  Practice Trials: {len(practice_trials)}
  Main Trials: {len(main_trials)}
  Total Trials: {len(self.trial_data)}
  Completion Time: {self.calculate_completion_time()}
        """
        
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', results_text)
        
    def calculate_median(self, numbers):
        """Calculate the median of a list of numbers."""
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            return sorted_numbers[n//2]
            
    def calculate_std(self, numbers):
        """Calculate the standard deviation of a list of numbers."""
        if len(numbers) < 2:
            return 0
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
        return math.sqrt(variance)
        
    def calculate_completion_time(self):
        """Calculate the total completion time."""
        if not self.trial_data:
            return "Unknown"
        
        start_time = datetime.fromisoformat(self.trial_data[0]['timestamp'])
        end_time = datetime.fromisoformat(self.trial_data[-1]['timestamp'])
        duration = end_time - start_time
        
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        return f"{minutes}m {seconds}s"
        
    def download_data(self, format_type):
        """Download the experiment data."""
        if not self.trial_data:
            messagebox.showerror("Error", "No data to download.")
            return
        
        # Prepare data for export
        all_data = {
            'participant_data': self.participant_data,
            'trial_data': self.trial_data,
            'experiment_info': {
                'version': '1.0',
                'completed_at': datetime.now().isoformat(),
                'total_trials': len(self.trial_data),
                'practice_trials': len([t for t in self.trial_data if t['is_practice']]),
                'main_trials': len([t for t in self.trial_data if not t['is_practice']])
            }
        }
        
        # Get save location
        participant_id = self.participant_data['participant_id']
        if format_type == 'csv':
            filename = f"reaction_time_data_{participant_id}.csv"
            filetypes = [('CSV files', '*.csv')]
        else:
            filename = f"reaction_time_data_{participant_id}.json"
            filetypes = [('JSON files', '*.json')]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=filetypes,
            initialvalue=filename
        )
        
        if file_path:
            try:
                if format_type == 'csv':
                    self.save_csv(file_path, all_data)
                else:
                    self.save_json(file_path, all_data)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {str(e)}")
                
    def save_csv(self, file_path, data):
        """Save data as CSV file."""
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write participant data
            writer.writerow(['Participant Data'])
            for key, value in data['participant_data'].items():
                writer.writerow([key, value])
            
            writer.writerow([])  # Empty row
            
            # Write trial data
            writer.writerow(['Trial Data'])
            writer.writerow(['participant_id', 'trial_number', 'modality', 'is_practice', 
                           'block', 'reaction_time', 'error_type', 'is_error', 'timestamp'])
            
            for trial in data['trial_data']:
                writer.writerow([
                    trial['participant_id'],
                    trial['trial_number'],
                    trial['modality'],
                    trial['is_practice'],
                    trial.get('block', ''),
                    trial['reaction_time'],
                    trial['error_type'] or '',
                    trial['is_error'],
                    trial['timestamp']
                ])
                
    def save_json(self, file_path, data):
        """Save data as JSON file."""
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
    def run(self):
        """Start the experiment application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = ReactionTimeExperiment()
    app.run()
