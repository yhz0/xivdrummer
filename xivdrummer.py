# %%
# XIVDrummer
import sys
from mido import Message, MidiFile, MidiTrack, MetaMessage
import json
import argparse

def transform_midi(input_file, output_file, config_file, track_num, channel_filter):
    # Load the config file
    with open(config_file) as config_file:
        config = json.load(config_file)

    # Construct the replace dict
    replace_dict = {}
    for replace_entry in config["replace_list"]:
        k = replace_entry['note']
        v = (replace_entry['target_track'], replace_entry['target_note'])
        replace_dict[k] = v

    # Read the midi input file and locate the requested track
    mid_in = MidiFile(input_file)
    track_in = mid_in.tracks[track_num]

    print(f"Processing Track #{track_num}: {track_in.name}")

    # Create output file with 3 tracks: bassdrum, snare, cymbal
    mid_out = MidiFile(type=1)

    out_track_names = ["bassdrum", "snaredrum", "cymbal"]
    out_track_channel = {
        "bassdrum": 0,
        "snaredrum": 1,
        "cymbal": 2
    }
    out_tracks = {}

    for tn in out_track_names:
        # create track with track name
        track = MidiTrack()
        trackname_msg = MetaMessage("track_name", name = tn)
        track.append(trackname_msg)
        out_tracks[tn] = track
        mid_out.tracks.append(out_tracks[tn])

    # Maintain individual delta for each track, and initialized with zero
    out_track_delta = {tn: 0 for tn in out_track_names}

    # Set the resolution
    mid_out.ticks_per_beat = mid_in.ticks_per_beat

    # Loop through the midi messages in the input track
    for msg in track_in:
        # a message received, increment delta for all tracks
        for tn in out_track_names:
            out_track_delta[tn] += msg.time

        # meta messages: 'set_tempo', 'time_signature'
        # meta messages will be forwarded to all channels.
        if msg.type == 'set_tempo' or msg.type == 'time_signature' or msg.type == 'end_of_track':
            for tn in out_track_names:
                new_msg = msg.copy(time=out_track_delta[tn])
                out_tracks[tn].append(new_msg)
                # reset all deltas
                out_track_delta[tn] = 0

        # regular messages: 'note_on', 'note_off'
        # for regular messages, it will look up config.replace_list
        # and forward the message to the respective channel
        elif msg.type == 'note_on' or msg.type == 'note_off':
            
            # filter note by channel
            if channel_filter is not None and msg.channel != channel_filter:
                continue

            # if the note is caught then forward it to 
            # the added track, and reset the delta for the added track
            # otherwise just do nothing
            if msg.note in replace_dict.keys():
                target_track, target_note = replace_dict[msg.note]
                new_msg = msg.copy(channel=out_track_channel[target_track],
                        note=target_note,
                        time=out_track_delta[target_track])
                out_tracks[target_track].append(new_msg)
                out_track_delta[target_track] = 0

    # Save the output file
    mid_out.save(output_file)

def display_channels(input_file):
    mid_in = MidiFile(input_file)

    for i, track in enumerate(mid_in.tracks):
        print(f"Track {i}: {track.name}")

        channels = set()

        for msg in track:
            if msg.type == "note_on":
                channels.add(msg.channel)

        print("Available channels: ", channels)

def print_usage():
    # This function will print the usage of the script
    print("Usage: script.py <input_file> <output_file> [options]")
    print("Options:")
    print("  --track_num <number>         Track number (integer, default: 0)")
    print("  --channel_filter <number>    Channel filter (integer, optional)")
    print("  --config_file <path>         Path to config file (default: 'config.json')")
    sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transform MIDI file.")
    parser.add_argument('input_file', help='Input MIDI file')
    parser.add_argument('output_file', help='Output file')
    parser.add_argument('--track_num', type=int, default=0, help='Track number (default: 0)')
    parser.add_argument('--channel_filter', type=int, default=None, help='Channel filter (integer, optional)')
    parser.add_argument('--config_file', default='config.json', help="Path to config file (default: 'config.json')")

    args = parser.parse_args()

    # Use the parsed arguments
    transform_midi(args.input_file, args.output_file, args.config_file, args.track_num, args.channel_filter)