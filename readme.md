# XIVDrummer

## Overview

XIVDrummer is a Python utility designed for Final Fantasy XIV players and music enthusiasts. It specializes in splitting a MIDI drum track into three distinct tracks: bass drum, snare drum, and cymbal.

## Installation

1. Download or clone the repository containing the main.py, config.json, and other necessary files.
2. Ensure mido is installed. If not, install it using pip install mido.

# Usage

To run the script, use the following command in your terminal or command prompt:

```
python main.py <input_file> <output_file>

- <input_file>: The path to the MIDI file you wish to process.
- <output_file>: The path where the processed MIDI file will be saved.
```

Example:

```
python main.py path/to/your/input_file.mid path/to/your/output_file.mid
```

This command will process input_file.mid and save the split tracks to output_file.mid.

## Configuration

The script uses a config.json file to manage the mapping of MIDI events. Modify this file as needed to suit your specific requirements for MIDI track splitting.