from dataclasses import dataclass
from typing import List
import re
from pathlib import Path

# Define chord mappings for transposition
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SHARP_TO_FLAT = {
    'C#': 'Db', 
    'D#': 'Eb', 
    'F#': 'Gb', 
    'G#': 'Ab', 
    'A#': 'Bb'
}
FLAT_TO_SHARP = {v: k for k, v in SHARP_TO_FLAT.items()}

@dataclass
class ChordPosition:
    chord: str
    position: int

@dataclass
class ParsedLine:
    chords: List[ChordPosition]
    lyrics: str

def parse_chord_markers(line: str) -> List[ChordPosition]:
    """
    Takes a line like "|F|Yesterday, |Em7|all" and extracts all chord positions
    Returns a list of ChordPosition objects
    """
    chords = []
    offset = 0  # Track how many characters we've removed
    
    for match in re.finditer(r'\|([^|]+)\|', line):
        chord = match.group(1)
        # Original position minus the offset from previous chord markers
        adjusted_position = match.start() - offset
        chords.append(ChordPosition(chord, adjusted_position))
        # Add length of |chord| to offset
        offset += len(match.group(0))  # length of |chord|
    
    return chords

def clean_lyrics(line: str) -> str:
    """
    Removes all chord markers from the line, preserving other spacing
    Example: "|F|Yesterday, |Em7|all" -> "Yesterday, all"
    """
    return re.sub(r'\|[^|]+\|', '', line)

def process_line(line: str) -> ParsedLine:
    """
    Main function to process a single line of input
    Returns a ParsedLine object containing chord positions and clean lyrics
    """
    chords = parse_chord_markers(line)
    lyrics = clean_lyrics(line)
    return ParsedLine(chords, lyrics)

def convert_to_flat_notation(chord: str) -> str:
    """Convert a chord from sharp to flat notation if applicable"""
    if not chord:
        return chord
        
    # Find the root note and the rest of the chord
    match = re.match(r'([A-G][#]?)(.*)', chord)
    if not match:
        return chord
        
    root, suffix = match.groups()
    
    # Convert if the root is in our sharp to flat mapping
    if root in SHARP_TO_FLAT:
        return SHARP_TO_FLAT[root] + suffix
    
    return chord

def format_line(parsed_line: ParsedLine, use_flats: bool = False) -> str:
    """
    Formats a ParsedLine into a two-line string with chords above lyrics
    Example:
    F     Em7    A7
    Yesterday, all my troubles
    """
    # If no chords or empty line, just return lyrics
    if not parsed_line.chords or not parsed_line.lyrics:
        return parsed_line.lyrics

    # Create a chord line of spaces equal to lyrics length
    chord_line = list(" " * len(parsed_line.lyrics))
    
    # Place each chord at its position
    for chord_pos in parsed_line.chords:
        chord = convert_to_flat_notation(chord_pos.chord) if use_flats else chord_pos.chord
        if chord_pos.position < len(chord_line):
            chord_line[chord_pos.position:chord_pos.position + len(chord)] = chord
    
    # Return combined output, with trailing spaces removed from chord line
    return f"{''.join(chord_line).rstrip()}\n{parsed_line.lyrics}"

def transpose_chord(chord: str, semitones: int) -> str:
    """
    Transpose a chord by a given number of semitones
    Example: transpose_chord("Am", 2) -> "Bm"
    """
    # Handle empty chords
    if not chord:
        return chord
        
    # Convert flats to sharps
    for flat, sharp in FLAT_TO_SHARP.items():
        if chord.startswith(flat):
            chord = chord.replace(flat, sharp, 1)
            break
    
    # Find the root note and the rest of the chord
    match = re.match(r'([A-G][#]?)(.*)', chord)
    if not match:
        return chord  # Return unchanged if not a valid chord
        
    root, suffix = match.groups()
    
    # Find the new root note
    current_index = NOTES.index(root)
    new_index = (current_index + semitones) % 12
    new_root = NOTES[new_index]
    
    return new_root + suffix

def transpose_line(parsed_line: ParsedLine, semitones: int) -> ParsedLine:
    """Transpose all chords in a line by the given number of semitones"""
    new_chords = [
        ChordPosition(transpose_chord(cp.chord, semitones), cp.position)
        for cp in parsed_line.chords
    ]
    return ParsedLine(new_chords, parsed_line.lyrics)

def process_file(file_path: Path) -> List[ParsedLine]:
    """Process a file and return a list of ParsedLine objects"""
    with open(file_path, 'r') as f:
        return [process_line(line.strip()) for line in f] 