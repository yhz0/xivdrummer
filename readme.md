# XIVDrummer

## Overview

XIVDrummer is a Python utility designed for Final Fantasy XIV players and music enthusiasts. It specializes in splitting a MIDI drum track into three distinct tracks: bass drum, snare drum, and cymbal.

## Installation

1. Download or clone the repository containing the xivdrummer.py, config.json, and other necessary files.
2. Ensure mido is installed. If not, install it using `pip install mido`.

You may also use the provided google colab notebook.

# Usage

To run the script, use the following command in your terminal or command prompt:

```
python main.py <input_file> <output_file> [options]
```

- `<input_file>`: The path to the MIDI file you wish to process.
- `<output_file>`: The path where the processed MIDI file will be saved.

Optional arguments:

- `--track_num <number>`: Specify the track number to process. Default is 0.
- `--channel_filter <number>`: Apply a channel filter with the specified number. Leave this option out if no channel filtering is needed.
- `--config_file <path>`: Path to the configuration file. Default is 'config.json'.

Example:

```
python main.py path/to/your/input_file.mid path/to/your/output_file.mid --track_num 0 --channel_filter 9 --config_file path/to/your/config.json
```

This command will process `input_file.mid`, considering only track number 0 and channel filter 9, and save the result to `output_file.mid`, using settings from `config.json`.

## Configuration

The script uses a config.json file to manage the mapping of MIDI events. Modify this file as needed to suit your specific requirements for MIDI track splitting.