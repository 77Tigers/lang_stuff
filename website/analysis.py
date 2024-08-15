if __name__ == "__main__":
    with open(f'songs/{song_name}/chunks.pkl', 'rb') as f:
        song_data = pickle.load(f)