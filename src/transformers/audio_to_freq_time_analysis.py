import librosa
import numpy as np
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
hyperparameters_path = os.path.join(
    dir_path, "../config/hyperparameters_separation.json"
)
fourierparameters_path = os.path.join(dir_path, "../config/fourierparameters.json")

with open(hyperparameters_path) as hyperparameters_file:
    hyperparameters = json.load(hyperparameters_file)

with open(fourierparameters_path) as fourierparameters_file:
    fourierparameters = json.load(fourierparameters_file)


def audio_to_freq_time_analysis(file_path, flag=False):
    try:
        # Use librosa to load audio file
        signal, sample_rate = librosa.load(
            file_path, sr=fourierparameters["sample_rate"], mono=True
        )

        # Determine the indices for the middle n seconds
        start_idx = int(
            (
                len(signal) / fourierparameters["sample_rate"]
                - fourierparameters["track_seconds_considered"]
            )
            / 2
            * fourierparameters["sample_rate"]
        )
        end_idx = (
            start_idx
            + fourierparameters["track_seconds_considered"]
            * fourierparameters["sample_rate"]
        )

        signal = signal[start_idx:end_idx]

        # STFT -> spectrogram
        hop_length = fourierparameters["hop_length"]
        n_fft = fourierparameters["n_fft"]
        n_mels = fourierparameters["n_mels"]

        # Perform stft
        stft = librosa.stft(signal, n_fft=n_fft, hop_length=hop_length)

        # Calculate abs values on complex numbers to get magnitude
        mag_spectrogram, phase = librosa.magphase(stft)

        # Create filters
        mel_scale = librosa.filters.mel(sr=sample_rate, n_fft=n_fft, n_mels=n_mels)

        # Constructing Mel Spectrogram by matrix multiplying STFT with Mel filters
        mel_spectrogram = np.dot(mel_scale, mag_spectrogram)

        if flag:
            mel_spectrogram[
                mel_spectrogram < fourierparameters["audio_amplitude_threshold"]
            ] = 0

        return mel_spectrogram, phase

    except Exception as e:
        raise Exception("Exception occurred: {}".format(e))
