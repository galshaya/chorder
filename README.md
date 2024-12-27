# Chorder

A command-line tool for creating, formatting, and transposing chord charts. This tool helps musicians format their chord charts with proper chord alignment above lyrics and provides useful features like transposition and file handling.

## Features

- Format chord charts with chords properly aligned above lyrics
- Transpose entire songs to different keys
- Support for complex chord notations (e.g., Am7, G/B, F#dim)
- Handle both sharp (#) and flat (b) notations
- Convert between sharp and flat notations
- Read from files or interactive input
- Save formatted output to files

## Installation

```bash
pip install chorder
```

## Usage

### Basic Command Format
```bash
chorder [-i INPUT_FILE] [-o OUTPUT_FILE] [-t SEMITONES] [-f]
```

### Command Line Options
- `-i, --input`: Input file path (optional)
- `-o, --output`: Output file path (optional)
- `-t, --transpose`: Number of semitones to transpose (optional, can be negative)
- `-f, --use-flats`: Use flat notation instead of sharps (optional)

### Input Format
Write your chord chart with chords enclosed in pipe symbols (`|`) where they should appear above the lyrics:
```
|D|I don't want to |A|close my eyes|Em|
I don't want to fall asleep
'Caue I'd |G|miss you baby
```

### Examples

1. **Interactive Mode** (type lines, press Ctrl+D when done):
```bash
chorder
```

2. **Process a File**:
```bash
chorder -i song.txt
```

3. **Save Output to File**:
```bash
chorder -i song.txt -o formatted_song.txt
```

4. **Transpose Up by 2 Semitones**:
```bash
chorder -i song.txt -t 2
```

5. **Transpose Down by 3 Semitones and Save**:
```bash
chorder -i song.txt -t -3 -o transposed_song.txt
```

6. **Use Flat Notation**:
```bash
chorder -i song.txt -f
```

### Example Input and Output

Input:
```
|D|I don't want to |A|close my eyes|Em|
```

Output with default sharp notation:
```
D               A            Em
I don't want to close my eyes
```

Output with flat notation ( 1 semitone transposed) (-f):
```
Eb              Bb           Fm
I don't want to close my eyes
```

## Tips

1. Place chord markers (`|C|`) exactly where you want the chord to appear above the lyrics
2. For complex chords, just write them normally: `|Cmaj7|`, `|F#m7b5|`
3. When transposing, the tool automatically handles both sharp and flat notations
4. Use the `-f` flag if you prefer flat notation (e.g., Bb instead of A#)
5. Empty lines are preserved in the output for formatting
6. You can pipe input/output to/from other commands using standard UNIX pipes

## Development

To install for development:
```bash
git clone https://github.com/yourusername/chorder.git
cd chorder
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
