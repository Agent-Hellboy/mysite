import PySimpleGUI as sg


def file_handle(text):
    layout = [
        [sg.Text(text, size=(100, 100))],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Window Title').Layout(layout)

    while True:                 # Event Loop
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break

    window.Close()
