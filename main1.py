import numpy as np
import bioread
from analysis3 import calculate_statistics, feature_extraction

segments = [(0, 15), (15, 30), (30, 45), (45, 60)]
file_paths = ['files/Marcin.acq', 'files/Marta.acq', 'files/Pola.acq']


def process_segment_data(data, segment_name):
    print(f"\n--- {segment_name} ---")
    stats = calculate_statistics(data)
    for key, value in stats.items():
        # Update the number of decimal places here
        print(f"{key.replace('_', ' ').title()}: {value:.4f}")  # Change .2f to .4f for four decimal places

    features = feature_extraction(data)
    print(f"Number of Peaks: {len(features['Peaks'])}")
    if features['Onset'] is not None and features['Offset'] is not None:
        # Assuming Onset and Offset are indices and don't need decimal places
        print(f"Onset at index: {features['Onset']}, Offset at index: {features['Offset']}")



for file_path in file_paths:
    datafile = bioread.read_file(file_path)
    base_name = file_path.split('/')[-1].split('.')[0]
    print(f"\nProcessing {base_name}...")

    for channel in datafile.channels:
        for start, end in segments:
            print(f"\nChannel: {channel.name}")
            start_index = np.searchsorted(channel.time_index, start)
            end_index = np.searchsorted(channel.time_index, end)
            signal_data_segment = channel.data[start_index:end_index]
            segment_name = f"{base_name} - {channel.name} Segment {start}-{end}s"
            process_segment_data(signal_data_segment, segment_name)
