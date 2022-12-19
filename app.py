from flask import Flask
import ghhops_server as hs
import rhino3dm

# fjfhe
# register hops app as middleware
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)


@hops.component(
    "/whisper",
    name="Whisper",
    nickname="Whi",
    description="Get prompt from recording",
    icon="pointat.png",
    inputs=[
        hs.HopsString("size", "size", "size"),
        hs.HopsString("audioPath", "audioPath", "audioPath"),
    ],
    outputs=[
        hs.HopsString("prompt", "prompt", "prompt"),
    ]
)
def audio_to_txt(size, audioPath):

    import whisper
    model = whisper.load_model(size)
    result = model.transcribe(audioPath, fp16=False, language='English')
    return result["text"]


@hops.component(
    "/stable-diffusion",
    name="Stable Diffusion",
    nickname="SD",
    # description="image",
    # icon="pointat.png",
    inputs=[
        hs.HopsString("prompt", "prompt", "prompt"),
    ],
    outputs=[
        hs.HopsString("prompt", "prompt", "prompt"),
    ]
)
def prompt_to_image(prompt):

    # make sure you're logged in with `huggingface-cli login`
    from torch import autocast
    from diffusers import StableDiffusionPipeline

    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        use_auth_token=True
    ).to("cuda")

    with autocast("cuda"):
        image = pipe(prompt)["sample"][0]

    image.save("astronaut_rides_horse.png")

    return image


@hops.component(
    "/edge_detection",
    name="Edge Detection",
    nickname="EdegeD",
    # description="image",
    # icon="pointat.png",
    inputs=[
        hs.HopsString("image", "image", "image"),
    ],
    outputs=[
        hs.HopsString("prompt", "prompt", "prompt"),
    ]
)
def edge_detection(path):
    '''
    For using this Script you need to install OpenCV in your machine
    '''
    # Importing openCV library
    import cv2 as cv

    # Taking path of input from the user
    img = cv.imread(path)
    img = cv.resize(img, (640, 640))  # resizing the image

    # Printing the original image
    cv.imshow('Original', img)
    # Reducing the noise from the image
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # Using Canny algorithm to detect the edges of the image
    final = cv.Canny(gray, 100, 200)
    print('Number of edges' + '=' + str(len(final)))  # printing Number of edges
    numberEdges = str(len(final))
    return numberEdges

@hops.component(
    "/PDFToWord",
    name="PDF To Word",
    nickname="PDFTW",
    # description="image",
    # icon="pointat.png",
    inputs=[
        hs.HopsString("PDF Path", "PDF Path", "PDF Path"),
    ],
    outputs=[
        hs.HopsString("done?", "done?", "done?"),
    ]
)
def PDFToWord(pdfPath):
    # pip install
    # fire==0.4.0
    # lxml==4.9.1
    # pdf2docx==0.5.1
    # PyMuPDF==1.18.12
    # python-docx==0.8.10
    # six==1.15.0
    # termcolor==1.1.0

    from pdf2docx import Converter
    import os 
    import sys

    # Take PDF's path as input 
    pdf = pdfPath
    assert os.path.exists(pdf), "File not found at, "+str(pdf)
    f = open(pdf,'r+')

    # Use the same name as pdf
    # Get the file name from the path provided by the user
    pdf_name = os.path.basename(pdf)
    # Get the name without the extension .pdf
    doc_name =  os.path.splitext(pdf_name)[0] + ".docx"

        
    # Convert PDF to Word
    cv = Converter(pdf)

    #Path to the directory
    path = os.path.dirname(pdf)

    cv.convert(os.path.join(path, "", doc_name) , start=0, end=None)
    cv.close()
    return print("Word doc created!")

@hops.component(
    "/Weather-App",
    name="Weather App",
    nickname="WA",
    # description="image",
    # icon="pointat.png",
    inputs=[
        hs.HopsString("city", "city", "city"),
    ],
    outputs=[
        hs.HopsString("temperature", "temperature", "temperature"),
    ]
)
def weatherAPP(city):
    import requests
    from bs4 import BeautifulSoup

    # Storing City You Want to Check Temperaature
    search = "weather in" + city
    # Searching it on google
    url = f"https://www.google.com/search?&q={search}"
    # Sending and Receiving Requests
    r = requests.get(url)
    # Scraping Details
    s = BeautifulSoup(r.text, "html.parser")
    # Storing Details
    update = s.find("div", class_="BNeawe").text
    # Printing Details
    print("Temperature in " + city + " is: " + update)
    return update

@hops.component(
    "/countdowmTime",
    name="Countdown Time",
    nickname="CT",
    # description="image",
    # icon="pointat.png",
    inputs=[
        hs.HopsString("countdowmTime", "countdowmTime", "countdowmTime"),
    ],
    outputs=[
        hs.HopsString("temperature", "temperature", "temperature"),
    ]
)
def countdowmTime(time_sec):
    import time
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1
    return print("stop")
    

if __name__ == "__main__":
    app.run(debug=True)
