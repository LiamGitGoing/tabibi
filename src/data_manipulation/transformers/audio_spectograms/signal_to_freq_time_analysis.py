import os
import time
import numpy as np
from src.__helpers__.__utils__ import (
    convert_t_dict_key_to_numpy_arrays,
    convert_to_recarray,
    get_one_file_with_extension,
    savez_numpy_data,
)
from src.data_manipulation.transformers.normalization.train_mix_bass_data_normalizer import (
    Normalizer,
)
from src.transformers.audio_to_freq_time_analysis import audio_to_freq_time_analysis


def transform_mix_and_bass_to_spectrogram(
    base_path, files_to_transform, save_file_path
):
    t_dict = {"x": list(), "y": list(), "mix_name": list()}
    dim_for_padding = []

    """
     # Uncomment if a pause is needed to prevent computer hardware from becoming overwhelmed
    data_point_multitude = 1
    """

    data_point_amount = 0

    # Iterates over all folders in base_path and checks if the folder is included in the files_to_transform list.
    # If yes, transforms the mix wav file and the bass wav file into spectograms.
    for foldername in os.listdir(f"{base_path}"):
        if foldername in files_to_transform:
            for mix_file_name in os.listdir(f"{base_path}/{foldername}/"):
                if mix_file_name.endswith(".wav"):
                    print(f"@@@@@@ data_point: {mix_file_name} @@@@@@ ")

                    data_point_amount += 1

                    mix_folder_path = f"{base_path}/{foldername}"
                    mix_file_path = f"{mix_folder_path}/{mix_file_name}"

                    print(mix_file_name)

                    bass_folder_path = f"{mix_folder_path}/Bass"
                    bass_file_name = get_one_file_with_extension(
                        directory_path=bass_folder_path, extension="wav"
                    )
                    print(bass_file_name)
                    print()

                    """
                    # Uncomment if a pause is needed to prevent computer hardware from becoming overwhelmed
                    if data_point_amount == (data_point_multitude * 30):
                        print("Waiting for 30 seconds")
                        data_point_multitude += 1
                        time.sleep(30)
                    """

                    if bass_file_name is None:
                        continue
                    bass_file_path = f"{bass_folder_path}/{bass_file_name}"

                    mix_spectrogram = audio_to_freq_time_analysis(
                        file_path=mix_file_path
                    )
                    bass_spectrogram = audio_to_freq_time_analysis(
                        file_path=bass_file_path
                    )

                    t_dict["x"].append(mix_spectrogram)
                    t_dict["y"].append(bass_spectrogram)
                    t_dict["mix_name"].append(mix_file_name)

                    dim_for_padding.append(mix_spectrogram.shape[1])

                    # delete variables after use to free up memory
                    del mix_spectrogram
                    del bass_spectrogram
                    del mix_file_name

                if data_point_amount == 2:
                    break
            if data_point_amount == 2:
                break
        if data_point_amount == 2:
            break

    # Pad the lists so that they all have the same dimensions
    max_dimension = max(dim_for_padding)
    t_dict["x"] = [
        np.pad(arr, ((0, 0), (0, max_dimension - arr.shape[1]))) for arr in t_dict["x"]
    ]
    t_dict["y"] = [
        np.pad(arr, ((0, 0), (0, max_dimension - arr.shape[1]))) for arr in t_dict["y"]
    ]

    # Save output into file
    t_dict = convert_t_dict_key_to_numpy_arrays(dictionary=t_dict, keys=["x", "y"])
    t_dict_recarray = convert_to_recarray(data_dict=t_dict)

    # Save un-normalized data
    savez_numpy_data(file_path=save_file_path, data=t_dict_recarray)

    # Normalize the data
    t_dict["x"] = Normalizer(t_dict["x"]).normalize()
    t_dict["y"] = Normalizer(t_dict["y"]).normalize()
    t_dict_recarray = convert_to_recarray(data_dict=t_dict)

    # Save normalized data
    savez_numpy_data(file_path=f"{save_file_path}_normalized", data=t_dict_recarray)

    print(f"@@@@@@@@@@ Processed wav files: {data_point_amount}")
