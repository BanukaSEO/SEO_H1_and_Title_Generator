import PySimpleGUI as sg
import openai
import os

import openai
openai.api_key = "YOUR-API-KEY"

# Define the function to generate titles and H1s
def generate_titles_and_h1s(keywords, business_type, company_name):
    prompt = f"""Keywords:\n{keywords}\n\n\"Using the keywords provided, write 10 long SEO optimized CTA H1 tags and page titles for a {business_type} website.\nEach H1 tag should be more than 100 characters long.\nH1 tag should have the exact keyword from the keywords provided.\nUse the exact keywords from the keywords list in the H1 tags and titles.\nDo not use similar keywords in the H1 tags and titles.\"\n\nUse the Format,\nTitle: Title | {company_name}\nH1: H1 Tag"""

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=2000,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the titles and H1s from the API response
    titles_and_h1s = []
    for choice in completions.choices:
        choice_text = choice.text.strip()
        if "|" in choice_text:
            title, h1 = choice_text.split("|", 1)
            titles_and_h1s.append((title.strip(), h1.strip()))

    # Return the titles and H1s
    return titles_and_h1s


# Define the UI layout
layout = [
    [sg.Text("Enter keywords (one per line):")],
    [sg.Multiline(key="keywords", size=(None, 5))],
    [sg.Text("Enter business type:")],
    [sg.Input(key="business_type")],
    [sg.Text("Enter company name:")],
    [sg.Input(key="company_name")],
    [sg.Button("Generate Titles & H1s"), sg.Quit()],
    [sg.Output(size=(None, 30))]
]

# Create the UI window
window = sg.Window("SSS Builder", layout)

# Start the UI event loop
while True:
    event, values = window.read()
    if event == "Quit" or event == sg.WIN_CLOSED:
        break
    elif event == "Generate Titles & H1s":
        keywords = values["keywords"].strip()
        business_type = values["business_type"].strip()
        company_name = values["company_name"].strip()
        if not keywords or not business_type or not company_name:
            sg.popup("Please fill in all the fields!")
            continue
        titles_and_h1s = generate_titles_and_h1s(keywords, business_type, company_name)
        if not titles_and_h1s:
            sg.popup("Failed to generate titles and H1s. Please try again!")
            continue
        for title, h1 in titles_and_h1s:
            print(f"Title: {title} | {company_name}")
            print(f"H1: {h1}\n")

# Close the UI window
window.close()
