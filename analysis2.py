import os
import numpy as np
import matplotlib.pyplot as plt
import bioread
from scipy.interpolate import make_interp_spline


def plot_frequency_distribution(hist, bin_edges, directory, title="Frequency Distribution", x_unit="Unit",
                                y_unit="Frequency"):
    # Calculate bin centers
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # Create a spline representation of the data
    spline = make_interp_spline(bin_centers, hist, k=3)  # k=3 for cubic spline
    smooth_bin_centers = np.linspace(bin_centers.min(), bin_centers.max(), 300)  # Increase number for smoother line
    smooth_hist = spline(smooth_bin_centers)

    plt.figure()
    plt.plot(smooth_bin_centers, smooth_hist, linestyle='-', color='b')  # Use smoothed data for plotting
    plt.fill_between(smooth_bin_centers, smooth_hist, color='skyblue', alpha=0.4)  # Fill below the smoothed line
    plt.xlabel(f'Signal Value ({x_unit})')
    plt.ylabel(f'{y_unit}')
    plt.title(title)

    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(os.path.join(directory, title.replace(" ", "_") + ".png"))
    plt.close()


def analyze_file(file_path, segments, bins=10, x_unit="Unit", y_unit="Frequency"):
    datafile = bioread.read_file(file_path)
    base_name = file_path.split('/')[-1].split('.')[0]

    for channel in datafile.channels:
        print(f"Analyzing {channel.name} in {base_name}")
        for start, end in segments:
            start_index = np.searchsorted(channel.time_index, start)
            end_index = np.searchsorted(channel.time_index, end)
            signal_data_segment = channel.data[start_index:end_index]

            hist, bin_edges = np.histogram(signal_data_segment, bins=bins)

            plot_title = f"{base_name} - {channel.name} Frequency Distribution {start}-{end}s"
            plot_frequency_distribution(hist, bin_edges, "fda2", title=plot_title, x_unit=x_unit, y_unit=y_unit)
