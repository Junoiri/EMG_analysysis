import numpy as np
from scipy import stats
from scipy.signal import find_peaks

def calculate_statistics(data):
    """
    Calculates various statistical measures to summarize and describe the signal data quantitatively.
    """
    statistics = {
        'Mean': np.mean(data),  # Average value indicating central tendency.
        'Median': np.median(data),  # Middle value, dividing the signal into two equal parts, less affected by outliers.
        'Standard Deviation': np.std(data),  # Measure of signal's dispersion or variability.
        'Variance': np.var(data),  # Square of the standard deviation, another measure of signal variability.
        'Coefficient of Variation': np.std(data) / np.mean(data),  # Ratio of std. dev. to mean, expressing variability relative to mean.
        'Skewness': stats.skew(data),  # Measure of asymmetry of the signal distribution.
        'Kurtosis': stats.kurtosis(data),  # Measure of the "tailedness" of the signal distribution - peakness or flatness.
        'Range': np.ptp(data),  # Difference between the maximum and minimum values in the signal.
        'Interquartile Range (IQR)': stats.iqr(data),  # Spread of the middle 50% of values, a measure of statistical dispersion.
        'Root Mean Square (RMS)': np.sqrt(np.mean(np.square(data))),  # Square root of the arithmetic mean of the squares of the signal, used in power analysis.
    }
    return statistics

def correlation(signal1, signal2):
    """
    Determines the linear relationship between two signals, returning a correlation coefficient.
    """
    return np.corrcoef(signal1, signal2)[0, 1]

def feature_extraction(data):
    """
    Transforms raw signal data into numerical features for further processing and analysis.
    """
    features = {
        'Peaks': find_peaks(data)[0],  # Local maxima, useful for spike analysis in ECG or EEG.
        'Troughs': find_peaks(-data)[0],  # Local minima in the signal.
        # For onset and offset detection, replace the placeholder with your specific logic.
        'Onset': 'Placeholder for onset detection logic.',  # Start of an event, like muscle activation in EMG.
        'Offset': 'Placeholder for offset detection logic.',  # End of an event.
    }
    return features
