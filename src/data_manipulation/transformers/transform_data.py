from src.__helpers__.constants import (
    MODEL1_BASE_PATH,
    MODEL2_BASE_PATH,
    MODEL1_TRAIN_FILE_PATH,
    MODEL1_TEST_FILE_PATH,
    MODEL2_TRAIN_FILE_PATH,
    MODEL2_TEST_FILE_PATH,
)
from src.data_manipulation.transformers.data_splitter.train_test_split import (
    train_test_splitter,
)
from src.data_manipulation.transformers.audio_spectrograms.signal_to_freq_time_analysis import (
    transform_audio_to_spectrogram,
)


def transform_data(flag):
    if flag == "audio separation":
        BASE_PATH = MODEL1_BASE_PATH
        TRAIN_FILE_PATH = MODEL1_TRAIN_FILE_PATH
        TEST_FILE_PATH = MODEL1_TEST_FILE_PATH
    elif flag == "tab transcription":
        BASE_PATH = MODEL2_BASE_PATH
        TRAIN_FILE_PATH = MODEL2_TRAIN_FILE_PATH
        TEST_FILE_PATH = MODEL2_TEST_FILE_PATH
    else:
        raise Exception("Invalid flag passed to transform_data function.")

    # Split data into train/test
    print("@@@@@@ Splitting data into train/test @@@@@@")
    train_files, test_files = train_test_splitter(BASE_PATH)

    # Transform training data and receive max_dimension
    print("@@@@@@ Transforming training data @@@@@@")

    # Transform training data
    transform_audio_to_spectrogram(
        base_path=BASE_PATH,
        files_to_transform=train_files,
        save_file_path=TRAIN_FILE_PATH,
        flag=flag,
    )
    # Transform testing data
    print("@@@@@@ Transforming testing data @@@@@@")
    transform_audio_to_spectrogram(
        base_path=BASE_PATH,
        files_to_transform=test_files,
        save_file_path=TEST_FILE_PATH,
        flag=flag,
    )
