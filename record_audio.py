import pyaudio
import wave
import speech_recognition as sr
import threading
import os

# Global flag to control recording
is_recording = True

def record_audio(filename, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100):
    """Function to record audio until the global flag is set to False."""
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    frames = []
    print("Recording... Press Enter to stop.")

    while is_recording:
        data = stream.read(chunk)
        frames.append(data)

    print("Recording stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    """Function to transcribe the recorded audio to text."""
    print("Transcribing audio...")
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        #text = recognizer.recognize_sphinx(audio)
        #text = recognizer.recognize_whisper(audio)
        print("Transcription: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")

def wait_for_enter():
    """Function to wait for the user to press Enter."""
    global is_recording
    input()  # Wait for Enter key
    is_recording = False

if __name__ == "__main__":
    filename = "output.wav"

    # Start recording in a separate thread
    recording_thread = threading.Thread(target=record_audio, args=(filename,))
    recording_thread.start()

    # Wait for the user to press Enter
    wait_for_enter()

    # Wait for the recording thread to finish
    recording_thread.join()

    # Transcribe the recorded audio
    transcribe_audio(filename)

    # Optionally, delete the WAV file after transcription
    os.remove(filename)