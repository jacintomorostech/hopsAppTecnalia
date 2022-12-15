from flask import Flask
import ghhops_server as hs
import rhino3dm

###fjfhe
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
        hs.HopsString("prompt","prompt","prompt"),
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
        hs.HopsString("prompt","prompt","prompt"),
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

if __name__ == "__main__":
    app.run(debug=True)