import pickle

def pickle_df(file_name, df):
    with open(file_name, 'wb') as f:
        pickle.dump(df, f)
        f.close()

def unpickle_data(file_name):
    df = 0
    try:
        with open(file_name, 'rb') as f:
            df = pickle.load(f)
            f.close()
    except Exception as e:
        msg = 'An error occurred in trying to unpickle data\n' + str(e)
        print(msg)
    finally:
        return df
