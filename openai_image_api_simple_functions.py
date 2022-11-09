import os
import openai
import time
import base64
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def createImageUrl(promptText, numberOfImages, imgSize):
    start = time.perf_counter()

    response = openai.Image.create(
    prompt=promptText,
    n=numberOfImages,
    size=imgSize
    )
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}ms".format(request_time))
    return (response)


def createImageB64(promptText, numberOfImages, imgSize):
    start = time.perf_counter()
    
    response = openai.Image.create(
    prompt=promptText,
    n=numberOfImages,
    size=imgSize,
    response_format="b64_json"
    )

    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}ms".format(request_time))

    image_64_encode = json.loads(str(response))["data"][0]["b64_json"]
    image_64_decode = base64.b64decode(image_64_encode)
    fileName = promptText.replace(' ', '_') + '.png'
    image_result = open(fileName, 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)

# Uncomment to run the function
#imgUrl = createImageUrl("Ukraine IT product companies", 1, "1024x1024")
#print (json.loads(str(imgUrl))["data"][0]["url"])

def imageEditUrl(promptText, numberOfImages, imgSize, uploadedImgPath, maskImgPath):


    response  = openai.Image.create_edit(
    image=open(uploadedImgPath, "rb"),
    mask=open(maskImgPath, "rb"),
    prompt=promptText,
    n=numberOfImages,
    size=imgSize
    )

    return (response)

def imageEditUrl(promptText, numberOfImages, imgSize, uploadedImgPath, maskImgPath):


    response  = openai.Image.create_edit(
    image=open(uploadedImgPath, "rb"),
    mask=open(maskImgPath, "rb"),
    prompt=promptText,
    n=numberOfImages,
    size=imgSize
    )

    return (response)

def imageEditB64(promptText, numberOfImages, imgSize, uploadedImgPath, maskImgPath):


    response  = openai.Image.create_edit(
    image=open(uploadedImgPath, "rb"),
    mask=open(maskImgPath, "rb"),
    prompt=promptText,
    n=numberOfImages,
    size=imgSize,
    response_format="b64_json"
    )

    image_64_encode = json.loads(str(response))["data"][0]["b64_json"]
    image_64_decode = base64.b64decode(image_64_encode)
    fileName = promptText.replace(' ', '_') + '.png'
    image_result = open(fileName, 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)

# Uncomment to run the function. Put related image in folder, and change name in function arguments
#print(imageEditUrl("Space warfare star wars in the sky above the forest", 1, "1024x1024", "kolochava-ukraine-1024.png", "kolochava-ukraine-1024-mask.png"))