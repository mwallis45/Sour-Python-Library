from sour import Sour

if __name__ == "__main__":
    sr = Sour()
    # sr.audio_to_image("example_audio.wav", mono=True, style="SLICE", max_size=700, chunk_size=2, save_as="temp_img.png", fill=True, sour_png=True, full_resize=True)
    # sr.image_to_audio("temp_img.sour")

    # sr.audio_to_image("example_audio.wav", mono=True, save_as="Full size")
    # sr.audio_to_image("example_audio.wav", mono=True, full_resize=True, max_size=640, save_as="Full 640x640")
    # sr.audio_to_image("example_audio.wav", mono=True, style="SLICE", chunk_size=64, save_as="chunk of 64 Slice")
    # sr.audio_to_image("example_audio.wav", mono=True, style="AVG", chunk_size=64, save_as="chunk of 64 Avg")
    # sr.audio_to_image("example_audio.wav", mono=True, style="SLICE", chunk_size=64, max_size=1000, fill=True, save_as="Large repeat")

    # sr.image_to_audio("example_image.png", meta_data=[".mp3", "44100", "16", "1"], save_as="test_audio")
    sr.audio_to_image("test_audio.mp3", save_as="test_image")

    print("done")