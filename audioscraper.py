import PySimpleGUI as sg
import webbrowser as wb
from pytube import YouTube
import string
import os

# Create the window layout
def generateLayout():

    sg.theme("DarkTeal10")

    input_style = {
        'background_color': "light grey",
        'text_color': "black",
        'font': ('Arial', 14)
    }

    layout = [
        [sg.Text("Enter URL:", font=('Arial', 14)), sg.Input(key="-URL-", **input_style), sg.Button("Search YouTube")],
        [sg.Text("Save destination:", font=('Arial', 14)), sg.Input(key="-DEST-", **input_style), sg.FolderBrowse()],
        [sg.HorizontalSeparator()],
        [sg.Text('', size=(15, 1)), sg.Button("Download Audio", pad=(10, 5), size=(15, 1)), sg.Exit("Exit", button_color = ("white", "tomato"), pad=(10, 5), size=(8, 1))],
        [sg.HorizontalSeparator()],
        [sg.Text("", key="-STATUS-", text_color='light green')]
    ]

    return layout

# Set the window theme
def windowTheme():
    sg.theme("DarkTeal10")
    sg.set_options(font=("Arial, 14"))

# Open YouTube in a new window
def launchYoutube():
    yt_url = "https://www.youtube.com/"
    wb.open(yt_url)

# Replace spaces in filename for saving purposes
def cleanFilename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename.replace(' ', '_')

# Use pytube to download the audio
def downloadAudio(window, url, download_directory):
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()

        if stream is None:
            raise Exception("No suitable audio stream found.")

        clean_filename = cleanFilename(video.title)
        file_path = os.path.join(download_directory, f"{clean_filename}.mp3")
        stream.download(output_path=download_directory, filename=f"{clean_filename}.mp3")
        window["-STATUS-"].update(f"Successfully downloaded audio: {clean_filename}.mp3")
        window["-URL-"].update(value="")

    except Exception as e:
        clean_filename = ""
        window["-STATUS-"].update(f"Error downloading {clean_filename}.mp3", text_color='tomato')

def main():
    windowTheme()
    layout = generateLayout()
    window = sg.Window("♫ YouTube Audio Scraper ♫", layout, use_custom_titlebar=True, keep_on_top=True, resizable=False)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "Download Audio":
            url = values["-URL-"]
            save_dest = values["-DEST-"]
            downloadAudio(window, url, save_dest)
        if event == "Search YouTube":
            launchYoutube()

    window.close()

if __name__ == "__main__":
    main()
