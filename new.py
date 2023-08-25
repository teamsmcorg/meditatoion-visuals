import pygame
from gtts import gTTS
import os
import time
from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)

class GuidedImageryApp:
    def __init__(self):
        self.tts_file = None
        self.instructions = [
            # Your instructions here
            "Find a quiet, comfy place to relax. Close your eyes and take slow breaths. Imagine you're by a peaceful river with the sun and breeze. Breathe in good feelings, breathe out stress. Imagine your tummy moving like the river as you breathe.Think of birds singing happily. Breathe like their singing: in when they sing, out when they stop. Imagine stress going away like leaves in the river.Listen to the birds and river until you're ready to stop. When you're done, open your eyes slowly and take this peaceful feeling with you. Do this whenever you want to feel calm.",
            "Imagine a peaceful scene in a forest.",
            "Visualize yourself walking along a serene stream.",
            "Feel the warmth of the sun on your skin.",
            "Listen to the birds chirping in the distance.",
        ]
        self.current_instruction = 0
        self.dynamic_instructions = []
        self.session_active = False

        # Initialize pygame.mixer and other variables here
        self.audio_file = "mixkit-birds-chirping-near-the-river-2473.wav"
        pygame.mixer.init()

        self.tts_file = "/temp.mp3"

    # Rest of your GuidedImageryApp class methods here
    def start_session(self):
        self.session_active = True
        self.play_audio()
        self.update_visualization()

    def stop_session(self):
        self.session_active = False
        pygame.mixer.music.stop()

    def pause_session(self):
        pygame.mixer.music.pause()

    def resume_session(self):
        pygame.mixer.music.unpause()
    
    def stop_session(self):
        self.session_active = False
        pygame.mixer.music.stop()
        pygame.mixer.stop() 

    def add_dynamic_instruction(self, instruction):
        self.dynamic_instructions.append(instruction)

    def add_instruction(self, instruction):
        if instruction:
            self.add_dynamic_instruction(instruction)

    def play_audio(self):
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play(-1)  # Loop the audio

    def update_visualization(self):
        if self.session_active and (self.current_instruction < len(self.instructions) + len(self.dynamic_instructions)):
            if self.current_instruction < len(self.instructions):
                instruction = self.instructions[self.current_instruction]
            else:
                instruction = self.dynamic_instructions[self.current_instruction - len(self.instructions)]

            self.speak_instruction(instruction)
            self.current_instruction += 1
            time.sleep(5)  # Pause for 5 seconds before moving to the next instruction
            self.update_visualization()
        else:
            self.stop_session()

    def speak_instruction(self, instruction):
        tts = gTTS(text=instruction, lang="en")
        dt=datetime.now().strftime("%M%S")
        fs=dt+".mp3"
        tts.save(fs)

        tts_sound = pygame.mixer.Sound(fs)
        tts_sound.play()

        while pygame.mixer.get_busy():
            time.sleep(0.1)

        tts_sound.stop()
        os.remove(fs)
        fs = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_session', methods=['POST'])
def start_session():
    app = GuidedImageryApp()
    app.start_session()
    return 'Session started'

@app.route('/pause_session', methods=['POST'])
def pause_session():
    app = GuidedImageryApp()
    app.pause_session()
    return 'Session paused'

@app.route('/resume_session', methods=['POST'])
def resume_session():
    app = GuidedImageryApp()
    app.resume_session()
    return 'Session resumed'

@app.route('/stop_session', methods=['POST'])
def stop_session():
    app = GuidedImageryApp()
    app.stop_session()
    return 'Session stopped'

@app.route('/play_music', methods=['POST'])
def play_music():
    pygame.mixer.music.play(-1)  # Loop the music
    return 'Music playing'

@app.route('/stop_music', methods=['POST'])
def stop_music():
    pygame.mixer.music.stop()
    return 'Music stopped'


if __name__ == "__main__":
    app.run(debug=True)
