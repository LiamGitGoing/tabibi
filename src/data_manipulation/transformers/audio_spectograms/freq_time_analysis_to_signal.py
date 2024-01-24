def transform_spectogram_to_audio():
    train_dict = {"x_train": list(), "y_train": list(), "mix_name": list()}
    dim_for_padding = []
    data_point_multitude = 1

    data_point_amount = 0
    for foldername in os.listdir(f"{base_path}"):
        for mix_file_name in os.listdir(f"{base_path}/{foldername}/"):
            if mix_file_name.endswith(".wav"):
                print(f"@@ data_point: {mix_file_name}")

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
                # Uncomment if a pause is needed to prevent computer hardware becoming overwhelmed
                if data_point_amount == (data_point_multitude * 30):
                    print("Waiting for 30 seconds")
                    data_point_multitude += 1
                    time.sleep(30)
                """

                if bass_file_name is None:
                    continue
                bass_file_path = f"{bass_folder_path}/{bass_file_name}"

                mix_spectrogram = audio_to_freq_time_analysis(file_path=mix_file_path)
                bass_spectrogram = audio_to_freq_time_analysis(file_path=bass_file_path)

                train_dict["x_train"].append(mix_spectrogram)
                train_dict["y_train"].append(bass_spectrogram)
                train_dict["mix_name"].append(mix_file_name)

                dim_for_padding.append(mix_spectrogram.shape[1])

                # delete variables after use to free up memory
                del mix_spectrogram
                del bass_spectrogram
                del mix_file_name

    # Pad the x_train and y_train lists so that they all have the same dimensions
    max_dimension = max(dim_for_padding)
    train_dict["x_train"] = [
        np.pad(arr, ((0, 0), (0, max_dimension - arr.shape[1])))
        for arr in train_dict["x_train"]
    ]
    train_dict["y_train"] = [
        np.pad(arr, ((0, 0), (0, max_dimension - arr.shape[1])))
        for arr in train_dict["y_train"]
    ]

    # Save output into file
    train_dict = convert_dict_key_to_numpy_arrays(
        dictionary=train_dict, keys=["x_train", "y_train"]
    )
    train_dict_recarray = convert_to_recarray(data_dict=train_dict)

    # Save un-normalized data
    savez_numpy_data(file_path=train_file_path, data=train_dict_recarray)

    print(f"@@@@@@@@@@ Processed wav files: {data_point_amount}")

    # Normalize the data
    train_dict["x_train"] = Normalizer(train_dict["x_train"]).normalize()
    train_dict["y_train"] = Normalizer(train_dict["y_train"]).normalize()

    # Save normalized data
    savez_numpy_data(
        file_path=f"{train_file_path}_normalized", data=train_dict_recarray
    )
