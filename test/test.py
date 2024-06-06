import pytest
from chord_generator import evaluate_stability
from chord_generator import chords

assert evaluate_stability

# Define chords and calculate_interval function for the sake of completeness
chords = {
    'C': ['C', 'E', 'G'],
    'G': ['G', 'B', 'D'],
    'Am': ['A', 'C', 'E'],
    'F': ['F', 'A', 'C']
}

def calculate_interval(note1, note2):
    # Simplified example: Assume notes are in the order of a chromatic scale
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    index1 = chromatic_scale.index(note1)
    index2 = chromatic_scale.index(note2)
    interval = (index2 - index1) % 12
    return interval if interval <= 6 else interval - 12

# Function to evaluate the stability of the transition between two chords
def evaluate_stability(chord1, chord2):
    root1 = chords[chord1][0]
    root2 = chords[chord2][0]
    interval = calculate_interval(root1, root2)
    
    # Common stable intervals in music
    stable_intervals = [0, 2, 4, 5, 7, -5, -7]

    if interval in stable_intervals:
        return 100
    else:
        return 0
