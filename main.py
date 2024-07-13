import random

import speech_recognition as sr
import os
import win32com.client
import webbrowser
from apikey import key
import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cv2  # Import OpenCV for camera access and image capture
import datetime

s = win32com.client.Dispatch("SAPI.SpVoice")
awsbuilderPass="AWSbuilderid@1"
# Your credentials

CLIENT_ID = "fab47bc7c3074e9e87a42ce7aeb18629"
CLIENT_SECRET = "e83ea36245c64a92b461da866ecc8aa0"
REDIRECT_URI = "http://localhost:8000/callback"

# Create an instance of the SpotifyOAuth class
sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope="user-modify-playback-state")

chatting = ""
def chat(query):
    global chatting
    print(chatting)
    apikey = key
    openai.api_key = apikey
    chatting += f"User: {query}\n RadheyShyam: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatting,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        s.Speak(response["choices"][0]["text"])
        chatting += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except Exception as e:
        print("NO choices found")

    
def ai(prompt):
    apikey = key
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n*****************************************************************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        print(response["choices"][0]["text"])
        text += response["choices"][0]["text"]
    except Exception as e:
        print("NO choices found")
    if not os.path.exists("openai_prompt"):
        os.mkdir("openai_prompt")

    with open(f"openai_prompt/{prompt[0:30]}", "w") as f:
        f.write(text)
def takecommand():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("\nProcessing Query.....")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "Sorry didn't get it, lemme hear it again"

if __name__ == '__main__':

    # s.Speak("Good Eve Master, this is your personal virtual assistant")
    s.Speak("I'm listening master")

    # Create a spotipy client using the token
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    sites = [
        ["YouTube", "https://www.youtube.com"],
        ["Google", "https://www.google.com"],
        ["Facebook", "https://www.facebook.com"],
        ["Amazon", "https://www.amazon.com"],
        ["Twitter", "https://www.twitter.com"],
        ["Instagram", "https://www.instagram.com"],
        ["LinkedIn", "https://www.linkedin.com"],
        ["Pinterest", "https://www.pinterest.com"],
        ["Reddit", "https://www.reddit.com"],
        ["Wikipedia", "https://www.wikipedia.org"],
        ["Tumblr", "https://www.tumblr.com"],
        ["Netflix", "https://www.netflix.com"],
        ["eBay", "https://www.ebay.com"],
        ["Yahoo", "https://www.yahoo.com"],
        ["Microsoft", "https://www.microsoft.com"],
        ["Apple", "https://www.apple.com"],
        ["Stack Overflow", "https://stackoverflow.com"],
        ["GitHub", "https://www.github.com"],
        ["Quora", "https://www.quora.com"],
        ["Medium", "https://www.medium.com"],
        ["Dropbox", "https://www.dropbox.com"],
        ["Spotify", "https://www.spotify.com"],
        ["Adobe", "https://www.adobe.com"],
        ["CNN", "https://www.cnn.com"],
        ["BBC", "https://www.bbc.com"],
        ["Buzzfeed", "https://www.buzzfeed.com"],
        ["HuffPost", "https://www.huffpost.com"],
        ["Forbes", "https://www.forbes.com"],
        ["The New York Times", "https://www.nytimes.com"]
    ]

    action = False

    while True:
        print("Listening.....")
        query = ""
        query = takecommand()

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                s.Speak(f"Opening {site[0]} for you sir")
                webbrowser.open(site[1])
                action = True
                break

        if action:
            continue

        if "play song on Spotify".lower() in query.lower():
            s.Speak("Sure, Master. Please tell me the name of the song.")
            song_name = takecommand().lower()
            s.Speak(f"Playing {song_name} on Spotify")
            results = sp.search(q=song_name, limit=1, type='track')
            if results['tracks']['items']:
                track_id = results['tracks']['items'][0]['uri']
                sp.start_playback(uris=[track_id])
            else:
                s.Speak(f"Sorry, Master. I couldn't find the song {song_name} on Spotify.")

        elif "open camera".lower() in query.lower():
            s.Speak("Opening camera for you, Master")
            camera = cv2.VideoCapture(0)  # Open the camera
            while True:
                ret, frame = camera.read()
                cv2.imshow("Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            camera.release()
            cv2.destroyAllWindows()

        # Check if the user wants to capture a photo
        elif "capture photo".lower() in query.lower():
            s.Speak("Capturing a photo for you, Master")
            camera = cv2.VideoCapture(0)  # Open the camera
            while True:
                ret, frame = camera.read()
                cv2.imshow("Camera", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('c'):
                    # Capture photo
                    photo_name = f"photo_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                    cv2.imwrite(photo_name, frame)
                    s.Speak(f"Photo captured and saved as {photo_name}")
                    break
            camera.release()
            cv2.destroyAllWindows()

        elif "what's the time".lower() in query.lower() or "tell me the time".lower() in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            s.Speak(f"Sure, this is Radhe shyam and the current time is {strfTime}")

        elif "using open ai".lower() in query.lower():
            ai(prompt=query)

        elif "new chat".lower() in query.lower() or "new one".lower() in query.lower() or "reset".lower() in query.lower():
            chatting = ""

        elif "ok bye".lower() in query.lower() or "no thanks".lower() in query.lower():
            s.Speak("Okie bye Master, See you soon")
            break

        else:
            print("Chatting.....")
            chat(query)

    s.Speak("anything else i can do for you master, do lemme know")
        # chatting = ""
        # s.Speak(query)



#todo: able to play music on spotify