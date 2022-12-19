from flask import Flask
import ghhops_server as hs
import rhino3dm

# fjfhe
# register hops app as middleware
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)

@hops.component(
    "/edge_detection",
    name="Edge Detection",
    nickname="EdegeD",
    # description="image",
    # icon="pointat.png",
    inputs=[
        hs.HopsString("imagePath", "imagePath", "imagePath"),
    ],
    outputs=[
        hs.HopsString("numberEdges", "numberEdges", "numberEdges"),
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



if __name__ == "__main__":
    app.run(debug=True)
