import pickle


def write_pickle_data(data, file_path):
    with open(file_path, "wb") as pickle_file:
        pickle.dump(data, pickle_file)
        pickle_file.close()


def read_pickle_data(file_path):
    with open(file_path, "rb") as pickle_file:
        data = pickle.load(pickle_file)
        pickle_file.close()

    return data
