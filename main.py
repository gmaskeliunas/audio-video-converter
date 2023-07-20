import subprocess
import os
import sys
import time
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import which
import PySimpleGUI as sg


AudioSegment.converter = which("ffmpeg")

# Define the global variables
LT_FLAG_PATH = "Icons\\lt.png"
EN_FLAG_PATH = "Icons\\usa.png"
VALID_ICON_PATH = "Icons\\valid.ico"
INVALID_ICON_PATH = "Icons\\invalid.ico"
ICON_PATH = "Icons\\icon.ico"


ENGLISH = {
    'language': 'EN',
    'ok_text': 'OK',
    'cancel_text': 'Cancel',
    'message_title_text': 'Message',
    'welcome_text': 'Welcome to my converter App!',
    'menu_text': [
        ["Options", ["Change theme", "Change font size", "Change language", "---", "Exit"]]
    ],
    'change_theme_popup_title': 'Theme settings',
    'selection_text': 'Select what you would like to convert:',
    'drop_down_text': ["Audio", "Video"],
    'browse_btn_text': 'Browse',
    'next_button_text': 'Next',
    'your_file_text': 'Your file:',
    'convert_to_text': 'Convert to:',
    'save_to_text': 'Save to:',
    'convert_text': 'Convert',
    'conversion_popup_title': 'Message',
    'conversion_successful_text': 'File was converted successfully!\n Conversion took ',
    'conversion_failed_text': 'File was not converted!\n (Output format should not\n match the input format)',
    'font_conversion_popup_title': 'Font settings',
    'select_font_size_text': 'Select font size:',
    'language_popup_title': 'Language settings',
    'select_language_text': 'Select language:',
    'back_text': 'Back',
    'window_title': 'Audio/Video Converter',
    'exit_text': 'Exit'
}


LITHUANIAN = {
    'language': 'LT',
    'ok_text': 'Gerai',
    'cancel_text': 'Atšaukti',
    'message_title_text': 'Message',
    'welcome_text': 'Sveiki atvykę į mano konverterio programą!',
    'menu_text': [
        ["Parinktys", ["Pakeisti temą", "Pakeisti šrifto dydį", "Pakeisti kalbą", "---", "Uždaryti"]]
    ],
    'change_theme_popup_title': 'Temos parinktys',
    'selection_text': 'Pasirinkite, ką norite konvertuoti:',
    'drop_down_text': ["Audio", "Video"],
    'browse_btn_text': 'Naršyti',
    'next_button_text': 'Toliau',
    'your_file_text': 'Jūsų failas:',
    'convert_to_text': 'Konvertuoti į:',
    'save_to_text': 'Išsaugoti kaip:',
    'convert_text': 'Konvertuoti',
    'conversion_popup_title': 'Žinutė',
    'conversion_successful_text': 'Failas konvertuotas sėkmingai!\n Konvertacija užtruko ',
    'conversion_failed_text': 'Failas nebuvo konvertuotas!\n (Failo plėtinys neturėtų sutapti\n su originalaus failo plėtiniu)',
    'font_conversion_popup_title': 'Šrifto parinktys',
    'select_font_size_text': 'Pasirinkite šrifto dydį:',
    'language_popup_title': 'Kalbos parinktys',
    'select_language_text': 'Pasirinkite kalbą',
    'back_text': 'Atgal',
    'window_title': 'Audio/Video Konverteris',
    'exit_text': 'Uždaryti'
}


def make_window1(language):
    """
    Create a window for selecting the type of file.

    Args:
        language (dict): Dictionary containing the text for the window.

    Returns:
        sg.Window: The window for selecting the type of file.
    """
    sg.theme(sg.user_settings_get_entry("theme", None))
    big_text_font = ("Helvetica", 20)

    #Create a column layout
    col_layout = [
        [sg.Menu(language['menu_text'])],
        [sg.Text(language['welcome_text'], font=big_text_font)],
        [sg.Text(language['selection_text'], key="-SELECT TEXT-"), sg.DropDown(["Audio", "Video"], key="-TYPE-", enable_events=True, readonly=True)],
        [sg.InputText(key="-FILEPATH-", size=(45, 1), disabled=True),
         sg.Button(language['browse_btn_text'], key="-BROWSE-", disabled=True, enable_events=True)],
        [sg.Button(language['next_button_text'], key="-NEXT-", disabled=True)],
    ]
    # column layout allows for a nice content justification, so everything is lined up.
    column = sg.Column(col_layout, justification='left')
    layout = [[column]]
    return sg.Window(language['window_title'], layout, size=(600, 250), resizable=True, finalize=True, icon=ICON_PATH)


def make_window2(output_file, tpl, font_size, language):
    """
    Create a window for converting a file.

    Args:
        output_file (str): The path to the output file.
        tpl (tuple): A tuple containing the name and extensions of the input file.
        font_size (int): The font size.
        language (dict): Dictionary containing the text for the window.

    Returns:
        sg.Window: The window for converting a file.
    """
    # Format extensions and create a new list of extensions
    extensions = tpl[0][1]
    extensions = extensions.split(";")
    extensions = [element.replace('*', '') for element in extensions]

    # In this window, output file is passed, then stripped of its full path, so only the name and extension is left, because I want to display it for the user in the first line.
    path_obj = Path(output_file)
    file_name_with_extension = path_obj.name
    text_font = ("Helvetica", font_size)

    col_layout = [
        [sg.Menu(language['menu_text'])],
        [sg.Text(language['your_file_text'], key="-FILE TEXT-", font=text_font), sg.InputText(file_name_with_extension, key="-FILEPATH-", size=(30, 1), disabled=True)],
        [sg.Text(language['convert_to_text'], key="-CONVERT TEXT-", font=text_font), sg.DropDown(extensions, key="-EXTENSIONS-", font=text_font, enable_events=True, readonly=True)],
        [sg.Text(language['save_to_text'], key="-SAVE TO TEXT-", font=text_font), sg.InputText(key="-NEWFILEPATH-", size=(30, 1), disabled=True), sg.Button(language['browse_btn_text'], key="-DIRBUTTON-", disabled=True)],
        [sg.Button(language['convert_text'], key="-CONVERT-", disabled=True)],
        [sg.Button(language['back_text'], key="-BACK-")]
    ]
    column = sg.Column(col_layout, justification='left')
    layout = [[column]]
    return sg.Window(language['window_title'], layout, size=(500, 300), finalize=True, resizable=True, icon=ICON_PATH)


def custom_popup_ok(message, title, size, icon, language):
    """
    Display a popup window with an OK button.

    Args:
        message (str): The message to display.
        title (str): The title of the popup window.
        size (tuple): The size of the popup window.
        icon (str): The path to the icon file.
        language (dict): Dictionary containing the text for the popup window.
    """
    layout = [
        [sg.Column([[sg.Text(message, justification='center', size=(size[0], size[1]-1))]], vertical_alignment='center', justification='center')],
        [sg.Column([[sg.Button(language['ok_text'], size=(10, 1))]], vertical_alignment='bottom', justification='center')],
    ]

    window = sg.Window(title, layout, size=size, finalize=True, icon=icon)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == language['ok_text']:
            break

    window.close()


def change_font_size_popup(window, element_list, font_size, size, language):
    """
    Display a popup window for changing the font size.

    Args:
        window (sg.Window): The window to update.
        element_list (list): List of elements to update.
        font_size (int): The current font size.
        size (tuple): The size of the popup window.
        language (dict): Dictionary containing the text for the popup window.

    Returns:
        int: The new font size.
    """
    font_sizes = ["8", "10", "12", "14", "16", "18", "20"]
    ev, vals = sg.Window(language['font_conversion_popup_title'], [[sg.Text(language['select_font_size_text'],
                                                                            key="-FILE TEXT-", font=(None, font_size)),
                                                                            sg.DropDown(font_sizes, k="-FONT SIZE LIST-",
                                                                            default_value = font_size, readonly=True),
                                                                            sg.OK(language['ok_text']),
                                                                            sg.Cancel(language['cancel_text'])]], size=size).read(close=True)
    if ev == language['ok_text']:
        font_size = int(vals["-FONT SIZE LIST-"])
        update_window_font_size(window, element_list, font_size)
    return font_size


def update_window_font_size(window, element_list, font_size):
    """
    Update the font size of the elements in the window.

    Args:
        window (sg.Window): The window to update.
        element_list (list): List of elements to update.
        font_size (int): The new font size.
    """
    for element in element_list:
        window[element].update(font=("Helvetica", font_size))
    window.finalize()


def language_selection_popup(language):
    """
    Display a popup window for selecting the language.

    Args:
        language (dict): Dictionary containing the text for the popup window.

    Returns:
        str: The selected language.
    """
    if language['language'] == 'EN':
        _en_default = True
        _lt_default = False
    else:
        _en_default = False
        _lt_default = True
    layout = [
        [sg.Text(language['select_language_text'], font=('AnyFont', 14))],
        [sg.Radio('English', "language", default=_en_default, font=('AnyFont', 12), key='-EN-'),
         sg.Image(filename=EN_FLAG_PATH, key='-EN_FLAG-')],
        [sg.Radio('Lietuvių', "language", default=_lt_default, font=('AnyFont', 12), key='-LT-'),
         sg.Image(filename=LT_FLAG_PATH, key='-LT_FLAG-')],
        [sg.Button(language['ok_text'], font=('AnyFont', 12))]
    ]

    window = sg.Window(language['language_popup_title'], layout, finalize=True, modal=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == language['ok_text']:
            window.close()
            break

    window.close()
    return 'English' if values['-EN-'] else 'Lithuanian'


def check_if_extensions_dont_match(input_extension, output_extension):
    """
    Check if the input and output file extensions don't match.

    Args:
        input_extension (str): Input file extension.
        output_extension (str): Output file extension.

    Returns:
        bool: True if the extensions don't match, False otherwise.
    """
    input_extension = input_extension.lower()
    output_extension = output_extension.lower()
    if input_extension != output_extension:
        return True
    else:
        return False


def convert(input_path, output_path):
    """
    Convert audio or video using FFmpeg.

    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to the output file.

    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    audio_extensions = ["mp3", "wav", "ogg", "flac", "adts", "ipod", "aiff"]
    video_extensions = ["mp4", "mkv", "avi", "mov", "webm"]

    input_file_name_with_extension = os.path.split(input_path)[1]
    input_file_extension = os.path.splitext(input_file_name_with_extension)[1]
    input_file_extension = input_file_extension[1:]

    output_file_name_with_extension = os.path.split(output_path)[1]
    output_file_extension = os.path.splitext(output_file_name_with_extension)[1]
    output_file_extension = output_file_extension[1:]

    # If extensions don not match, then conversion proceeds, otherwise False is returned
    if check_if_extensions_dont_match(input_file_extension, output_file_extension):
        try:
            if output_file_extension == "aac":
                output_file_extension = "adts"
            if output_file_extension == "m4a":
                output_file_extension = "ipod"

            if output_file_extension != "webm":
                video_command = ["ffmpeg", "-y", "-i", input_path, "-c", "copy", output_path]
            else:
                video_command = ["ffmpeg", "-y", "-i", input_path, "-c:v", "libvpx-vp9", "-crf", "30", "-c:a", "libvorbis", "-f", "webm", output_path]

            if output_file_extension in audio_extensions:
                return convert_audio(input_path, output_path, output_file_extension)
            elif output_file_extension in video_extensions:
                return convert_video(video_command)
            else:
                # If output file extension is other than the available extensions the error is raised
                raise ValueError("Unknown output file extension")
        except Exception as e:
            raise e
    else:
        return False


def convert_audio(input_path, output_path, output_format):
    """
    Convert audio using FFmpeg.

    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to the output file.
        output_format (str): Desired format of the output file.

    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    try:
        # Load the audio file
        audio = AudioSegment.from_file(input_path)

        # Convert the audio to the desired format
        audio.export(output_path, format=output_format)
        print(f"Conversion successful. {input_path} has been converted to {output_path}")
        return True
    except Exception as e:
        print(f"Error occurred during conversion: {str(e)}")
        return False


def convert_video(command):
    """Convert video using FFmpeg.

    Args:
        command (str): command to be executed.

    Returns:
        bool: True if the command was executed successfully, False otherwise.
    """
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False


def main():
    """
    This is the main function of the app. It creates the window and runs it.
    """
    # Here we define initial values for audio and video formats, as well as other defaults
    audio_file_types = (("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.aac;*.m4a;*.aiff"),)
    video_file_types = (("Video Files", "*.mp4;*.mkv;*.avi;*.mov;*.webm"),)
    output_file = ""
    font_size = "10"
    popup_size = (250, 125)
    font_popup_size = (400, 100)
    # Here are elements of which font sizes can be changed
    win1_change_font_elements = ["-SELECT TEXT-", "-TYPE-"]
    win2_change_font_elements = ["-FILE TEXT-", "-CONVERT TEXT-", "-SAVE TO TEXT-", "-EXTENSIONS-"]
    # Default language
    selected_language = ENGLISH
    window = make_window1(selected_language)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == selected_language['exit_text']:
            break

        # In this portion of the code we listen for events. The events of elements are checked if the window event variable is equal to element's key, which can be set like this: "-KEY-".
        if event == "-TYPE-":
            match values['-TYPE-']:
                case "Audio":
                    window["-BROWSE-"].update(disabled=False)
                    window["-BROWSE-"].FileTypes = audio_file_types

                case "Video":
                    window["-BROWSE-"].update(disabled=False)
                    window["-BROWSE-"].FileTypes = video_file_types

                case _:
                    break

        # If a file is selected, then the code updates the small window with the selected file path.
        if event == "-BROWSE-":
            output_file = sg.popup_get_file('Enter the output file name:', no_window=True, file_types=window["-BROWSE-"].FileTypes)
            window["-FILEPATH-"].update(output_file)

        # Next button is enabled or disabled depending on whether the file is selected or not.
        if output_file == "":
            window["-NEXT-"].update(disabled=True)
        elif output_file != "":
            window["-NEXT-"].update(disabled=False)

        # We listen for an event whose key is the same as the button being pressed
        if event == selected_language['menu_text'][0][1][0]:
            ev, vals = sg.Window(selected_language['change_theme_popup_title'], [[sg.Combo(sg.theme_list(), k="-THEME LIST-"),
                                                                                  sg.OK(selected_language['ok_text']),
                                                                                  sg.Cancel(selected_language['cancel_text'])]
                                                                                  ]).read(close=True)
            if ev == selected_language['ok_text']:
                window.close()
                sg.user_settings_set_entry("theme", vals["-THEME LIST-"])
                window = make_window1(selected_language)

        if event == selected_language['menu_text'][0][1][1]:
            font_size = change_font_size_popup(window, win1_change_font_elements, font_size, font_popup_size, selected_language)

        if event == selected_language['menu_text'][0][1][2]:
            selected_language = ENGLISH if language_selection_popup(selected_language) == 'English' else LITHUANIAN
            window = make_window1(selected_language)


        if event == "-NEXT-":
            # If Next button is clicked we hide the fisrt window and output the second window.
            window.Hide()
            window2 = make_window2(output_file, window["-BROWSE-"].FileTypes, font_size, selected_language)
            new_output_file = ""
            while True:
                event2, values2 = window2.read()

                # Change theme
                if event2 == selected_language['menu_text'][0][1][0]:
                    ev, vals = sg.Window(selected_language['change_theme_popup_title'], [[sg.Combo(sg.theme_list(), k="-THEME LIST-"),
                                                                                        sg.OK(selected_language['ok_text']),
                                                                                        sg.Cancel(selected_language['cancel_text'])]
                                                                                        ]).read(close=True)
                    if ev == selected_language['ok_text']:
                        window2.close()
                        window.close()
                        sg.user_settings_set_entry("theme", vals["-THEME LIST-"])
                        window = make_window1(selected_language)
                        window.Hide()
                        window2 = make_window2(output_file, window["-BROWSE-"].FileTypes, font_size, selected_language)

                # We listen for the second window events.
                if event2 == selected_language['menu_text'][0][1][1]:
                    font_size = change_font_size_popup(window2, win2_change_font_elements, font_size, font_popup_size, selected_language)
                    update_window_font_size(window, win1_change_font_elements, font_size)

                if event2 == sg.WINDOW_CLOSED or event2 == selected_language['exit_text']:
                    sys.exit()

                if event2 == selected_language['menu_text'][0][1][2]:
                    selected_language = ENGLISH if language_selection_popup(selected_language) == 'English' else LITHUANIAN
                    window.close()
                    window2.close()
                    window = make_window1(selected_language)
                    window.Hide()
                    window2 = make_window2(output_file, window["-BROWSE-"].FileTypes, font_size, selected_language)

                if event2 == "-BACK-":
                    window2.close()  # Close the second window
                    window.UnHide()  # Re-open the first window when "Back" is pressed
                    break

                if event2 == "-EXTENSIONS-":
                    window2["-DIRBUTTON-"].update(disabled=False)

                if event2 == "-DIRBUTTON-":
                    new_output_file = sg.popup_get_file('Enter the output file name:', save_as=True, no_window=True, file_types=(("File", f"*{values2['-EXTENSIONS-']}"),))
                    window2["-NEWFILEPATH-"].update(new_output_file)

                if new_output_file == "":
                    window2["-CONVERT-"].update(disabled=True)
                elif new_output_file != "":
                    window2["-CONVERT-"].update(disabled=False)

                if event2 == "-CONVERT-":
                    # Here, the time is calculated, how long does the conversion take to complete.
                    start_time = time.time()
                    if convert(output_file, new_output_file):
                        end_time = time.time()
                        execution_time = end_time - start_time
                        custom_popup_ok(f"{selected_language['conversion_successful_text']} {execution_time:.2f} s.",
                                        title=selected_language['conversion_popup_title'],
                                        size=popup_size,
                                        icon=VALID_ICON_PATH,
                                        language=selected_language)
                    else:
                        custom_popup_ok(selected_language['conversion_failed_text'],
                                        title=selected_language['conversion_popup_title'],
                                        size=popup_size,
                                        icon=INVALID_ICON_PATH,
                                        language=selected_language)

            window2.close()

    window.close()

if __name__ == '__main__':
    main()
