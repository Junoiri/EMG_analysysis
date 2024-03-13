import os
import numpy as np
import matplotlib.pyplot as plt
import bioread


def calculate_frequency_distribution(data, bins=10):
    """
    Calculate the frequency distribution of the given data.

    Parameters:
    - data: The signal data as a numpy array.
    - bins: The number of bins to use for the distribution.

    Returns:
    - hist: The counts in each bin.
    - bin_edges: The edges of the bins.
    """
    hist, bin_edges = np.histogram(data, bins=bins)
    return hist, bin_edges


def plot_frequency_distribution(hist, bin_edges, directory, title="Frequency Distribution"):
    """
    Plot the frequency distribution given the histogram and bin edges, and save to a specified directory.

    Parameters:
    - hist: The counts in each bin (output of np.histogram).
    - bin_edges: The edges of the bins (output of np.histogram).
    - directory: The directory where the plot will be saved.
    - title: Title of the plot.
    """
    plt.figure()
    plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor="black")
    plt.xlabel('Signal Value')
    plt.ylabel('Frequency')
    plt.title(title)

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the figure
    plt.savefig(os.path.join(directory, title.replace(" ", "_") + ".png"))
    plt.close()


def analyze_file(file_path, segments, bins=10):
    """
    Perform frequency distribution analysis for the given file and segments, and save the graphs to a directory.

    Parameters:
    - file_path: Path to the .acq file.
    - segments: A list of tuples, each representing a start and end time.
    - bins: The number of bins to use for the frequency distribution.
    """
    datafile = bioread.read_file(file_path)
    base_name = file_path.split('/')[-1].split('.')[0]

    for channel in datafile.channels:
        print(f"Analyzing {channel.name} in {base_name}")
        for start, end in segments:
            start_index = np.searchsorted(channel.time_index, start)
            end_index = np.searchsorted(channel.time_index, end)
            signal_data_segment = channel.data[start_index:end_index]

            # Calculate frequency distribution
            hist, bin_edges = calculate_frequency_distribution(signal_data_segment, bins)

            # Plot and save the distribution graph
            plot_title = f"{base_name} - {channel.name} Frequency Distribution {start}-{end}s"
            plot_frequency_distribution(hist, bin_edges, "fda", title=plot_title)
