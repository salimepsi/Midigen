import random
import math
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

#Define the notes for the chords in Ab minor (Abm, Dbm, Ebm)
chords = {
    # Accords mineurs
    'Cmin': [48, 51, 55],   # C, Eb, G
    'C#min': [49, 52, 56],  # C#, E, G#
    'Dbmin': [49, 52, 56],  # Db, E, Ab
    'Dmin': [50, 53, 57],   # D, F, A
    'D#min': [51, 54, 58],  # D#, F#, A#
    'Ebmin': [51, 54, 58],  # Eb, Gb, Bb=
    'Emin': [52, 55, 59],   # E, G, B
    'Fmin': [53, 56, 60],   # F, Ab, C
    'F#min': [54, 57, 61],  # F#, A, C#
    'Gbmin': [54, 57, 61],  # Gb, A, Db
    'Gmin': [55, 58, 62],   # G, Bb, D
    'G#min': [56, 59, 63],  # G#, B, D#
    'Abmin': [56, 59, 63],  # Ab, B, Eb
    'Amin': [57, 60, 64],   # A, C, E
    'A#min': [58, 61, 65],  # A#, C#, F
    'Bbmin': [58, 61, 65],  # Bb, Db, F
    'Bmin': [59, 62, 66],   # B, D, F#

    # Accords majeurs
    'Cmaj': [48, 52, 55],   # C, E, G
    'C#maj': [49, 53, 56],  # C#, F, G#
    'Dbmaj': [49, 53, 56],  # Db, F, Ab
    'Dmaj': [50, 54, 57],   # D, F#, A
    'D#maj': [51, 55, 58],  # D#, G, A#
    'Ebmaj': [51, 55, 58],  # Eb, G, Bb
    'Emaj': [52, 56, 59],   # E, G#, B
    'Fmaj': [53, 57, 60],   # F, A, C
    'F#maj': [54, 58, 61],  # F#, A#, C#
    'Gbmaj': [54, 58, 61],  # Gb, Bb, Db
    'Gmaj': [55, 59, 62],   # G, B, D
    'G#maj': [56, 60, 63],  # G#, C, D#
    'Abmaj': [56, 60, 63],  # Ab, C, Eb
    'Amaj': [57, 61, 64],   # A, C#, E
    'A#maj': [58, 62, 65],  # A#, D, F
    'Bbmaj': [58, 62, 65],  # Bb, D, F
    'Bmaj': [59, 63, 66],   # B, D#, F#

    # Accords de septième
    'C7': [48, 52, 55, 58],     # C, E, G, Bb
    'C#7': [49, 53, 56, 59],    # C#, F, G#, B
    'Db7': [49, 53, 56, 59],    # Db, F, Ab, B
    'D7': [50, 54, 57, 60],     # D, F#, A, C
    'D#7': [51, 55, 58, 61],    # D#, G, A#, C#
    'Eb7': [51, 55, 58, 61],    # Eb, G, Bb, Db
    'E7': [52, 56, 59, 62],     # E, G#, B, D
    'F7': [53, 57, 60, 63],     # F, A, C, Eb
    'F#7': [54, 58, 61, 64],    # F#, A#, C#, E
    'Gb7': [54, 58, 61, 64],    # Gb, Bb, Db, E
    'G7': [55, 59, 62, 65],     # G, B, D, F
    'G#7': [56, 60, 63, 66],    # G#, C, D#, F#
    'Ab7': [56, 60, 63, 66],    # Ab, C, Eb, Gb
    'A7': [57, 61, 64, 67],     # A, C#, E, G
    'A#7': [58, 62, 65, 68],    # A#, D, F, G#
    'Bb7': [58, 62, 65, 68],    # Bb, D, F, Ab
    'B7': [59, 63, 66, 69],     # B, D#, F#, A

    # Accords mineurs de septième
    'Cm7': [48, 51, 55, 58],    # C, Eb, G, Bb
    'C#m7': [49, 52, 56, 59],   # C#, E, G#, B
    'Dbm7': [49, 52, 56, 59],   # Db, E, Ab, B
    'Dm7': [50, 53, 57, 60],    # D, F, A, C
    'D#m7': [51, 54, 58, 61],   # D#, F#, A#, C#
    'Ebm7': [51, 54, 58, 61],   # Eb, Gb, Bb, Db
    'Em7': [52, 55, 59, 62],    # E, G, B, D
    'Fm7': [53, 56, 60, 63],    # F, Ab, C, Eb
    'F#m7': [54, 57, 61, 64],   # F#, A, C#, E
    'Gbm7': [54, 57, 61, 64],   # Gb, A, Db, E
    'Gm7': [55, 58, 62, 65],    # G, Bb, D, F
    'G#m7': [56, 59, 63, 66],   # G#, B, D#, F#
    'Abm7': [56, 59, 63, 66],   # Ab, B, Eb, Gb
    'Am7': [57, 60, 64, 67],    # A, C, E, G
    'A#m7': [58, 61, 65, 68],   # A#, C#, F, G#
    'Bbm7': [58, 61, 65, 68],   # Bb, Db, F, Ab
    'Bm7': [59, 62, 66, 69],    # B, D, F#, A

    # Accords de neuvième
    'C9': [48, 52, 55, 58, 62],     # C, E, G, Bb, D
    'C#9': [49, 53, 56, 59, 63],    # C#, F, G#, B, D#
    'Db9': [49, 53, 56, 59, 63],    # Db, F, Ab, B, Eb
    'D9': [50, 54, 57, 60, 64],     # D, F#, A, C, E
    'D#9': [51, 55, 58, 61, 65],    # D#, G, A#, C#, F
    'Eb9': [51, 55, 58, 61, 65],    # Eb, G, Bb, Db, F
    'E9': [52, 56, 59, 62, 66],     # E, G#, B, D, F#
    'F9': [53, 57, 60, 63, 67],     # F, A, C, Eb, G
    'F#9': [54, 58, 61, 64, 68],    # F#, A#, C#, E, G#
    'Gb9': [54, 58, 61, 64, 68],    # Gb, Bb, Db, E, Ab
    'G9': [55, 59, 62, 65, 69],     # G, B, D, F, A
    'G#9': [56, 60, 63, 66, 70],    # G#, C, D#, F#, A#
    'Ab9': [56, 60, 63, 66, 70],    # Ab, C, Eb, Gb, Bb
    'A9': [57, 61, 64, 67, 71],     # A, C#, E, G, B
    'A#9': [58, 62, 65, 68, 72],    # A#, D, F, G#, C
    'Bb9': [58, 62, 65, 68, 72],    # Bb, D, F, Ab, C
    'B9': [59, 63, 66, 69, 73],     # B, D#, F#, A, C#

    # Accords mineurs de neuvième
    'Cm9': [48, 51, 55, 58, 62],    # C, Eb, G, Bb, D
    'C#m9': [49, 52, 56, 59, 63],   # C#, E, G#, B, D#
    'Dbm9': [49, 52, 56, 59, 63],   # Db, E, Ab, B, Eb
    'Dm9': [50, 53, 57, 60, 64],    # D, F, A, C, E
    'D#m9': [51, 54, 58, 61, 65],   # D#, F#, A#, C#, F
    'Ebm9': [51, 54, 58, 61, 65],   # Eb, Gb, Bb, Db, F
    'Em9': [52, 55, 59, 62, 66],    # E, G, B, D, F#
    'Fm9': [53, 56, 60, 63, 67],    # F, Ab, C, Eb, G
    'F#m9': [54, 57, 61, 64, 68],   # F#, A, C#, E, G#
    'Gbm9': [54, 57, 61, 64, 68],   # Gb, A, Db, E, Ab
    'Gm9': [55, 58, 62, 65, 69],    # G, Bb, D, F, A
    'G#m9': [56, 59, 63, 66, 70],   # G#, B, D#, F#, A#
    'Abm9': [56, 59, 63, 66, 70],   # Ab, B, Eb, Gb, Bb
    'Am9': [57, 60, 64, 67, 71],    # A, C, E, G, B
    'A#m9': [58, 61, 65, 68, 72],   # A#, C#, F, G#, C
    'Bbm9': [58, 61, 65, 68, 72],   # Bb, Db, F, Ab, C
    'Bm9': [59, 62, 66, 69, 73],    # B, D, F#, A, C#

    'Cmaj7': [48, 52, 55, 59],   # C, E, G, B
    'C#maj7': [49, 53, 56, 60],  # C#, F, G#, C
    'Dbmaj7': [49, 53, 56, 60],  # Db, F, Ab, C
    'Dmaj7': [50, 54, 57, 61],   # D, F#, A, C#
    'D#maj7': [51, 55, 58, 62],  # D#, G, A#, D
    'Ebmaj7': [51, 55, 58, 62],  # Eb, G, Bb, D
    'Emaj7': [52, 56, 59, 63],   # E, G#, B, D#
    'Fmaj7': [53, 57, 60, 64],   # F, A, C, E
    'F#maj7': [54, 58, 61, 65],  # F#, A#, C#, E#
    'Gbmaj7': [54, 58, 61, 65],  # Gb, Bb, Db, F
    'Gmaj7': [55, 59, 62, 66],   # G, B, D, F#
    'G#maj7': [56, 60, 63, 67],  # G#, C, D#, G
    'Abmaj7': [56, 60, 63, 67],  # Ab, C, Eb, G
    'Amaj7': [57, 61, 64, 68],   # A, C#, E, G#
    'A#maj7': [58, 62, 65, 69],  # A#, D, F, A
    'Bbmaj7': [58, 62, 65, 69],  # Bb, D, F, A
    'Bmaj7': [59, 63, 66, 70],   # B, D#, F#, A#
    'Cbmaj7': [59, 63, 66, 70],
    'Fbmaj7': [64, 68, 59, 63],

    #Diminué 
    'Cdim': [48, 51, 54],       # C, Eb, Gb
    'C#dim': [49, 52, 55],      # C#, E, G
    'Ddim': [50, 53, 56],       # D, F, Ab
    'D#dim': [51, 54, 57],      # D#, F#, A
    'Edim': [52, 55, 58],       # E, G, Bb
    'Fdim': [53, 56, 59],       # F, Ab, B
    'F#dim': [54, 57, 60],      # F#, A, C
    'Gdim': [55, 58, 61],       # G, Bb, Db
    'G#dim': [56, 59, 62],      # G#, B, D
    'Adim': [57, 60, 63],       # A, C, Eb
    'A#dim': [58, 61, 64],      # A#, C#, E
    'Bdim': [59, 62, 65],       # B, D, F
    'Cbdim': [59, 62, 65],      # Cb, D, F

    #Dim 7
    'Cdim7': [48, 51, 54, 57],    # C, Eb, Gb, Bbb (A)
    'C#dim7': [49, 52, 55, 58],   # C#, E, G, Bb
    'Ddim7': [50, 53, 56, 59],    # D, F, Ab, Cb (B)
    'D#dim7': [51, 54, 57, 60],   # D#, F#, A, C
    'Edim7': [52, 55, 58, 61],    # E, G, Bb, Db
    'Fdim7': [53, 56, 59, 62],    # F, Ab, B, D
    'F#dim7': [54, 57, 60, 63],   # F#, A, C, Eb
    'Gdim7': [55, 58, 61, 64],    # G, Bb, Db, E
    'G#dim7': [56, 59, 62, 65],   # G#, B, D, F
    'Adim7': [57, 60, 63, 66],    # A, C, Eb, Gb
    'A#dim7': [58, 61, 64, 67],   # A#, C#, E, G
    'Bdim7': [59, 62, 65, 68],    # B, D, F, Ab
    'Cbdim7': [59, 62, 65, 68],   # Cb, D, F, Ab

}

def humanize_chord(chord, base_velocity=64, time_variation=10, velocity_variation=15, duration_variation=10, quarter_note_ticks=480):
    """
    Humanize the chord by slightly varying the timing, velocity, and duration of each note.
    
    :param chord: List of MIDI note numbers.
    :param base_velocity: Base velocity of the notes.
    :param time_variation: Maximum variation in timing (ticks).
    :param velocity_variation: Maximum variation in velocity.
    :param duration_variation: Maximum variation in note duration (ticks).
    :param quarter_note_ticks: Base duration of a quarter note in ticks.
    :return: List of (note, time, velocity, duration) tuples.
    """
    base_duration = quarter_note_ticks
    humanized_chord = []
    for note in chord:
        time_offset = random.randint(-time_variation, time_variation)
        velocity_offset = random.randint(-velocity_variation, velocity_variation)
        velocity = max(1, min(127, base_velocity + velocity_offset))  # Ensure velocity is within MIDI range
        duration = base_duration + random.randint(-duration_variation, duration_variation // 2)  # Ensure duration is close to base_duration
        duration = math.ceil(duration)  # Ensure the duration is rounded up to the nearest integer
        humanized_chord.append((note, time_offset, velocity, duration))
    return humanized_chord

def create_chord_progression_midi(chord_names, midi_file_path, bpm):
    """
    Create a MIDI file with a humanized chord progression.
    
    :param chord_names: List of chord names (e.g., ['Abm', 'Dbm', 'Ebm']).
    :param midi_file_path: Path to save the MIDI file.
    :param bpm: Beats per minute (tempo) of the MIDI file.
    :param quarter_note_ticks: Duration of a quarter note in ticks (default is 480 ticks).
    """
    # Convert BPM to microseconds per beat
    tempo = bpm2tempo(bpm)
    quarter_note_ticks=60000/bpm
    # Create a new MIDI file and add a track
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    # Set the tempo (microseconds per beat)
    track.append(MetaMessage('set_tempo', tempo=tempo))


    # Add the humanized chords to the track based on the provided chord names
    for chord_name in chord_names:
        if chord_name not in chords:
            print(f"Error: Invalid chord name '{chord_name}'. Valid chords are: {list(chords.keys())}")
            return

        chord = chords[chord_name]
        humanized_chord = humanize_chord(chord, quarter_note_ticks=quarter_note_ticks)
        max_duration = max(note[3] for note in humanized_chord)
        note_on_times = [max(0, note[1]) for note in humanized_chord]

        # Note-on messages
        for i, (note, time_offset, velocity, duration) in enumerate(humanized_chord):
            track.append(Message('note_on', note=note, velocity=velocity, time=note_on_times[i]))

        # Note-off messages
        for i, (note, time_offset, velocity, duration) in enumerate(humanized_chord):
            # Calculate the note_off time to ensure all notes in the chord end approximately together
            if i == 0:
                track.append(Message('note_off', note=note, velocity=velocity, time=note_on_times[i] + duration))
            else:
                track.append(Message('note_off', note=note, velocity=velocity, time=random.randint(0,12)))

    # Save the MIDI file
    midi.save(midi_file_path)
    print(f'MIDI file saved as {midi_file_path}')

# Function to pick a random chord
def pick_random_chord():
    return random.choice(list(chords.keys()))

# Function to calculate the interval between two MIDI note values
def calculate_interval(note1, note2):
    return note2 - note1

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

# Function to generate a chord progression starting from a given chord
def generate_chord_progression(start_chord='Cmaj', length=4):
    progression = [start_chord]
    current_chord = start_chord
    for _ in range(length - 1):
        next_chord = pick_random_chord()
        while evaluate_stability(current_chord, next_chord) == 0:
            next_chord = pick_random_chord()
        progression.append(next_chord)
        current_chord = next_chord
    return progression

# Example usage
chord_progression =['Abm7', 'Dbm7', 'Ebm7', 'Cbmaj7', 'Bdim7', 'Fbmaj7', 'Gb7', 'Abm7']
create_chord_progression_midi(chord_progression, 'chord_progression.mid', bpm=153)

