import pytest
from chord_generator import evaluate_stability
from chord_generator import chords

def test_calculate_interval(get_chords_Cmin, get_chords_Emaj):
    interval = calculate_interval(get_chords_Cmin[0], get_chords_Emaj[0])
    assert interval == 4
    assert test_calculate_interval (-8,-9) == 1

def test_evaluate_stability():
    assert evaluate_stability('Cmin',(Emaj))
