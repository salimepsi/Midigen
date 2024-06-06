from mido import MidiFile, MidiTrack, MetaMessage, Message

# Créer un fichier MIDI
midi = MidiFile()

# Créer une nouvelle piste MIDI
track = MidiTrack()
midi.tracks.append(track)

# Ajouter des messages à la piste
track.append(MetaMessage('set_tempo', tempo=500000, time=0))
track.append(Message('note_on', channel=0, note=56, velocity=74, time=0))
track.append(Message('note_on', channel=0, note=59, velocity=77, time=0))


#track.append(Message('note_on', channel=0, note=63, velocity=69, time=0))

#track.append(Message('note_off', channel=0, note=59, velocity=77, time=479))
#track.append(Message('note_off', channel=0, note=63, velocity=69, time=482))

# Sauvegarder le fichier MIDI
midi.save('output_track.mid')

print('Le fichier MIDI a été sauvegardé sous le nom "output_track.mid".')
