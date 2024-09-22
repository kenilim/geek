import speech_recognition as sr
from pydub import AudioSegment

# Paths
m4a_path = "/Users/kenilim/geek/transcribe_audio/Marina Bay Link Mall 2.m4a"
wav_path = "/Users/kenilim/geek/transcribe_audio/Marina_Bay_Link_Mall_2.wav"

# Convert M4A to WAV
audio = AudioSegment.from_file(m4a_path, format="m4a")
audio.export(wav_path, format="wav")

# Transcribe the WAV file in chunks
recognizer = sr.Recognizer()
with sr.AudioFile(wav_path) as source:
    # Adjust the chunk size (in milliseconds)
    chunk_length_ms = 30000  # 30 seconds
    audio_length = len(audio)
    transcription = ""

    for i in range(0, audio_length, chunk_length_ms):
        chunk_audio = audio[i:i + chunk_length_ms]
        chunk_wav_path = f"/Users/kenilim/geek/transcribe_audio/chunk_{i // chunk_length_ms}.wav"
        chunk_audio.export(chunk_wav_path, format="wav")

        with sr.AudioFile(chunk_wav_path) as chunk_source:
            chunk_audio_data = recognizer.record(chunk_source)
            try:
                chunk_transcription = recognizer.recognize_google(chunk_audio_data)
                transcription += chunk_transcription + " "
            except sr.RequestError as e:
                print(f"Error recognizing chunk {i // chunk_length_ms}: {e}")
            except sr.UnknownValueError:
                print(f"Could not understand chunk {i // chunk_length_ms}")

print(transcription)