import requests

url = "http://gideonotieno.pythonanywhere.com/predict"
image_path = "weed1.jpg"

with open(image_path, "rb") as img:
    response = requests.post(url, files={"image": img})

print(response.json())
