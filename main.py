import bioread
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from analysis2 import analyze_file



def read_and_plot_acq_segments(file_path, segments):
    datafile = bioread.read_file(file_path)
    base_name = file_path.split('/')[-1].split('.')[0]

    # Initialize an Excel workbook
    workbook = Workbook()
    workbook.remove(workbook.active)  # Remove the default sheet

    for channel in datafile.channels:
        # Print out the units for each channel's signal
        print(f"Channel '{channel.name}' units: {channel.units}")

        for start, end in segments:
            start_index = np.searchsorted(channel.time_index, start)
            end_index = np.searchsorted(channel.time_index, end)
            time_data_segment = channel.time_index[start_index:end_index]
            signal_data_segment = channel.data[start_index:end_index]

            # Plotting
            plt.figure()
            plt.plot(time_data_segment, signal_data_segment)
            plt.title(f"{base_name} - {channel.name} from {start} to {end} seconds")
            plt.xlabel('Time (s)')
            plt.ylabel(f"Signal ({channel.units})")
            plt.savefig(f"{base_name}_{channel.name.replace(' ', '_')}_graph_{start}_{end}.png")
            plt.close()

            # Save data to Excel with a modification to include every 0.5s
            save_data_to_excel_mod(workbook, f"{channel.name}_{start}_{end}", time_data_segment, signal_data_segment)

    # Save the workbook
    workbook.save(f"{base_name}_data.xlsx")


def save_data_to_excel_mod(workbook, sheet_name, time_data, signal_data):
    sheet = workbook.create_sheet(title=sheet_name)
    sheet.append(["Time (s)", "Signal"])

    # Assuming time_data is uniformly spaced, find the closest index for each 0.5s increment
    current_time = 0.0
    while current_time < time_data[-1]:
        closest_index = (np.abs(time_data - current_time)).argmin()
        sheet.append([time_data[closest_index], signal_data[closest_index]])
        current_time += 0.1



# Define your segments and file paths
segments = [(0, 15), (15, 30), (30, 45), (45, 60)]
file_paths = ['files/Marcin.acq', 'files/Marta.acq', 'files/Pola.acq']

# Loop through each file path and perform frequency distribution analysis
for path in file_paths:
    analyze_file(path, segments, bins=20)  # Here, bins=20 is just an example; adjust as needed

