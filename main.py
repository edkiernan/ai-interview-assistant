import threading
import os

import record_audio
import get_ai_response

if __name__ == "__main__":
    starting_question = '''What is a piece of technology that you don't like and that you don't feel comfortable using? '''
    previous_question = starting_question
    while True:
        filename = "output.wav"
        recording_thread = threading.Thread(target=record_audio.record_audio, args=(filename,))
        recording_thread.start()
        record_audio.wait_for_enter()
        recording_thread.join()
        answer_to_question = record_audio.transcribe_audio(filename)
        record_audio.reset_recording()
        os.remove(filename)
        
        if answer_to_question:
            next_question = get_ai_response.get_best_followup(answer_to_question, previous_question)
            previous_question = next_question
            if next_question:
                print(f"NEXT QUESTION: {next_question}")
                input("\nPress 'Enter' to record your next response or 'Ctrl + C' to exit.")
