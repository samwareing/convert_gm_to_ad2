import py_midicsv as pm
import os

input_filename = "Beacon For Womankind.mid"

track_name = "Drumkit"

# MIDI note numbers
# General MIDI map to Addictive Drums 2 map
# For the Guitar Pro drumkit
# Note some information is lost after Guitar Pro export
mapping_gm_to_ad2 = {
    38: 38,
    37: 42,
    # 38: 41,  # Snare (rim shot)
    42: 49,
    # 46: 55,  # Hi-Hat (half)
    46: 57,
    44: 48,
    35: 36,
    36: 36,
    50: 71,
    48: 71,
    47: 69,
    45: 67,
    43: 65,
    # 51: 62,  # Ride (edge)
    51: 60,
    53: 61,
    55: 77,
    52: 79,
    49: 81,
    57: 89,
    56: 47,
    # 56: 47,  # Cowbell
    # 56: 47,  # Cowbell
}


def get_drumkit_track_numbers(csv_strings):
    drumkit_track_numbers = []
    for line in csv_strings:
        if track_name in line:
            print("Found Drumkit track: \"{line}\"")
            drumkit_track_numbers.append(line[0])
    return drumkit_track_numbers


def convert_drumkit_notes(drumkit_track_numbers, mapping, csv_strings):
    new_csv_strings = []
    for line in csv_strings:
        tokens = ("Note_on_c", "Note_off_c", "Poly_aftertouch_c")
        if line[0] in drumkit_track_numbers and any(token in line for token in tokens):
            line_split = line.split(",")
            track_number = line_split[0].strip()
            time = line_split[1].strip()
            token = line_split[2].strip()
            channel = line_split[3].strip()
            old_note = line_split[4].strip()
            vel_or_val = line_split[5].strip()
            new_note = mapping[int(old_note)]
            new_line = f"{track_number}, {time}, {token}, {channel}, {new_note}, {vel_or_val}\n"
        else:
            new_line = line
        new_csv_strings.append(new_line)
    return new_csv_strings


if __name__ == "__main__":
    csv_strings = pm.midi_to_csv(input_filename)

    drumkit_track_numbers = get_drumkit_track_numbers(csv_strings)
    if not drumkit_track_numbers:
        raise ValueError("No drumkit tracks found")

    converted = convert_drumkit_notes(drumkit_track_numbers, mapping_gm_to_ad2, csv_strings)

    midi_object = pm.csv_to_midi(converted)

    filename = os.path.splitext(input_filename)
    output_filename = f"{filename[0]}_converted{filename[1]}"

    with open(output_filename, "wb") as output_file:
        midi_writer = pm.FileWriter(output_file)
        midi_writer.write(midi_object)
