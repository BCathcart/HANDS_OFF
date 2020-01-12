#!/usr/bin/env python
# coding: utf-8

import pyautogui
import speech_recognition as sr

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
# currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.


# Mouse movement functions

def mouse_down(percent):
    pixels = percent/100.0 * screenHeight
    pyautogui.move(0, pixels) 

def mouse_up(percent):
    pixels = percent/-100.0 * screenHeight
    pyautogui.move(0, pixels)   
    
def mouse_right(percent):
    pixels = percent/100.0 * screenWidth
    pyautogui.move(pixels, 0)
    
def mouse_left(percent):
    pixels = percent/-100.0 * screenWidth
    pyautogui.move(pixels, 0)
    
def bit_down():
    pyautogui.move(0, 10) 
    
def bit_up():
    pyautogui.move(0, -10) 
    
def bit_right():
    pyautogui.move(10, 0) 
    
def bit_left():
    pyautogui.move(-10, 0) 
    
def click():
    pyautogui.click()
    
def doubleclick():
    pyautogui.doubleClick()
    
# Scrolling only works if in correct cursor location (maybe move to center)
def scroll_up(scroll_amount):
     pyautogui.scroll(scroll_amount) 
    
def scroll_down(scroll_amount):
     pyautogui.scroll(scroll_amount) 
        
def scroll_right(scroll_amount):
    pyautogui.hscroll(scroll_amount)

def scroll_left(scroll_amount):
     pyautogui.hscroll(scroll_amount)


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source) #analyze the audio source for 1 second
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #   update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


# Basic way to approach commands, probably changing this to be more versitatile later
def perform_action(speech):
    speech = speech.lower()
    speech_tokens = speech.split()
    print("\nSpeech tokens: ")
    print(speech_tokens)

    # Move mouse
    if ('mouse' in speech_tokens):
        try:
            percent = int(speech_tokens[-1])
        except ValueError:
            percent = 20
        if ('down' in speech_tokens):
            mouse_down(percent)
        elif ('up' in speech_tokens):
            mouse_up(percent)
        elif ('right' in speech_tokens):
            mouse_right(percent)
        elif ('left' in speech_tokens):
            mouse_left(percent)

    # Move mouse slightly
    elif ('bit' in speech_tokens):
        if ('down' in speech_tokens):
            bit_down(bit_amount)
        elif ('up' in speech_tokens):
            bit_up(bit_amount)
        elif ('right' in speech_tokens):
            bit_right(bit_amount)
        elif ('left' in speech_tokens):
            bit_left(bit_amount)

    # Scroll
    elif ('scroll' in speech_tokens):
        try:
            scroll_amount = int(speech_tokens[-1])
        except ValueError:
            scroll_amount = 10
        if ('down' in speech_tokens):
            scroll_down(scroll_amount)
        elif ('up' in speech_tokens):
            scroll_up(scroll_amount)
        elif ('right' in speech_tokens):
            scroll_right(scroll_amount)
        elif ('left' in speech_tokens):
            scroll_left(scroll_amount)

    # Click
    elif ('click' in speech_tokens):
        click()


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # End phrase after a 200ms under energy lvl
    recognizer.pause_threshold = 0.3
    recognizer.non_speaking_duration = 0.3

    # Adjust for ambient noise
    recognizer.dynamic_energy_threshold = True
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        print("Waiting for command...")
        print(recognizer.energy_threshold)

        response = recognize_speech_from_mic(recognizer, mic)
        speech =  response['transcription']
        print(response)

        if (response['error'] == None):
            perform_action(speech)
            print("Speech" + speech)

        print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n\n{}' \
            .format(response['success'],
                    response['error'],
                    '-'*17,
                    response['transcription']))

        print(recognizer.energy_threshold)
