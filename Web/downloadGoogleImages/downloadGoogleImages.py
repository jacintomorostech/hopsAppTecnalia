import shutil
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from flask import Flask
import ghhops_server as hs

app = Flask(__name__)
hops = hs.Hops(app)


@hops.component(
    "/downloadGoogleImages1",
    name="Download Google Images",
    nickname="DGI",
    description="image",
    icon=r"C:/hopsAppTecnalia/Web/downloadGoogleImages/tecnaliaGHlogoogleimages.png",
    inputs=[
        hs.HopsString("search", "search", "search"),
        hs.HopsString("pathSave", "pathSave", "pathSave"),
        hs.HopsNumber("numberImages", "numberImages", "numberImages"),
    ],
    outputs=[
        hs.HopsString("imageFilePaths", "imageFilePaths", "imageFilePaths"),
    ]
)
def downloadGoogleImages(search, pathSave, numberImages):
    # define the name of the directory to be created
    keys = [search]

    for item in keys:
        from selenium import webdriver

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        # Opens up web driver and goes to Google Images
        PATH_CHROME = "C:\hopsAppTecnalia\Web\downloadGoogleImages\chromedriver.exe"
        driver = webdriver.Chrome(
            executable_path=PATH_CHROME, chrome_options=options)
        driver.implicitly_wait(3)

        driver.set_window_size(1024, 600)
        driver.maximize_window()

        driver.get('https://www.google.es/')
        driver.find_element("xpath", '//*[@id="L2AGLb"]/div').click()

        box = driver.find_element(
            "xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
        box.send_keys(str(item))
        box.send_keys(Keys.ENTER)

        images = driver.find_element(
            "xpath", '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')
        images.click()

        # Will keep scrolling down the webpage until it cannot scroll no more
        last_height = driver.execute_script(
            'return document.body.scrollHeight')
        while True:
            driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            new_height = driver.execute_script(
                'return document.body.scrollHeight')
            try:
                driver.find_element(
                    "xpath", '//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
                time.sleep(2)
            except:
                pass
            if new_height == last_height:
                break
            last_height = new_height

        name_folder = item.replace(" ", "_")
        path_save = pathSave+str(name_folder)
        if os.path.exists(path_save):
            shutil.rmtree(path_save)
        os.makedirs(path_save)

        cantidad_fotos = numberImages
        for i in range(1, cantidad_fotos):
            try:
                driver.find_element("xpath", '//*[@id="islrg"]/div[1]/div['+str(
                    i)+']/a[1]/div[1]/img').screenshot(path_save+'/'+str(name_folder)+str(i)+'.jpg')
                print(i)
            except:
                print('except')
                pass
    return path_save


if __name__ == "__main__":
    app.run(debug=True)
