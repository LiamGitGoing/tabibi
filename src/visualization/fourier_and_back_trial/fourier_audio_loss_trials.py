import librosa
import numpy as np
import soundfile as sf

from src.data_manipulation.transformers.normalization.mix_bass_data_normalizer import (
    Normalizer,
)
from src.transformers.freq_time_analysis_to_audio import freq_time_analysis_to_audio

INPUT_FILE_PATH = "./audio/MusicDelta_80sRock/MusicDelta_80sRock_MIX.wav"


def fourier_audio_loss(file_path):
    try:
        # use librosa to load audio file
        signal, sample_rate = librosa.load(file_path, sr=22050, mono=True)

        # STFT -> spectrogram
        hop_length = 512  # in num. of samples
        n_fft = 2048  # window in num. of samples
        # perform stft
        stft = librosa.stft(signal, n_fft=n_fft, hop_length=hop_length)
        # calculate abs values on complex numbers to get magnitude
        spectrogram = np.abs(stft)

        t_dict = {"x": list()}

        t_dict["x"].append(spectrogram)
        norm_x = Normalizer(t_dict["x"])
        t_dict["x"], t_dict["min_max_amplitudes"] = (
            norm_x.normalize(),
            norm_x.get_min_max(),
        )

        freq_time_analysis_to_audio(
            t_dict["x"],
            "audio/",
            ["MusicDelta_80sRock_MIX.wav"],
            t_dict["min_max_amplitudes"],
        )

    except Exception as e:
        raise Exception("Exception occurred: {}".format(e))


fourier_audio_loss(INPUT_FILE_PATH)