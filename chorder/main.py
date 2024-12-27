import argparse
import sys
from pathlib import Path
from .formatter import process_file, process_line, format_line, transpose_line

def print_welcome():
    """Print welcome message and basic instructions"""
    print("""
╔════════════════════════════════════════════╗
║            Welcome to Chorder!             ║
║        Your Musical Chart Assistant        ║
╚════════════════════════════════════════════╝

Quick Guide:
1. Enter chords using pipe symbols: |C|Lyrics |Am|go |F|here
2. Press Enter after each line
3. Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done
4. Use command line options for advanced features:
   -i: input file
   -o: output file
   -t: transpose (number of semitones)
   -f: use flat notation (e.g., Bb instead of A#)

Example: Happy |C|birthday to |G|you
""")

def interactive_mode():
    """Handle interactive input with user-friendly prompts"""
    print("\nEnter your lyrics with chords (Press Ctrl+D when finished):")
    print("─" * 50)
    parsed_lines = []
    try:
        while True:
            line = input("> ")
            parsed_lines.append(process_line(line))
    except EOFError:
        print("\nProcessing your chord chart...")
    return parsed_lines

def save_to_file(file_path: Path, parsed_lines, use_flats: bool = False):
    """Save formatted lines to a file"""
    with open(file_path, 'w') as f:
        for parsed_line in parsed_lines:
            formatted = format_line(parsed_line, use_flats)
            f.write(formatted + "\n")

def main():
    parser = argparse.ArgumentParser(description='Chord Chart Formatter and Transposer')
    parser.add_argument('-i', '--input', type=Path, help='Input file path')
    parser.add_argument('-o', '--output', type=Path, help='Output file path')
    parser.add_argument('-t', '--transpose', type=int, help='Number of semitones to transpose (can be negative)')
    parser.add_argument('-f', '--use-flats', action='store_true', help='Use flat notation (e.g., Bb instead of A#)')
    
    args = parser.parse_args()
    
    # Show welcome message if no input file specified
    if not args.input:
        print_welcome()
    
    # If no input file, use interactive mode
    if args.input:
        try:
            parsed_lines = process_file(args.input)
            print(f"\nProcessing file: {args.input}")
        except FileNotFoundError:
            print(f"Error: Input file '{args.input}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        parsed_lines = interactive_mode()
    
    # Transpose if requested
    if args.transpose:
        print(f"\nTransposing by {args.transpose} semitones...")
        parsed_lines = [transpose_line(line, args.transpose) for line in parsed_lines]
    
    # Output handling
    if args.output:
        try:
            save_to_file(args.output, parsed_lines, args.use_flats)
            print(f"\nSaved formatted chord chart to: {args.output}")
        except Exception as e:
            print(f"Error saving file: {e}")
            sys.exit(1)
    else:
        print("\nFormatted Chord Chart:")
        print("─" * 50)
        for parsed_line in parsed_lines:
            print(format_line(parsed_line, args.use_flats))
            print()  # Extra newline for readability
        print("─" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0) 