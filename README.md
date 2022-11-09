# OpenAI-image-generation-API-script-and-Postman-collection
OpenAI image generation API Postman collection + simple Python functions

OpenAI [release new image generation](https://beta.openai.com/docs/guides/images/introduction) capabilities with  DALL·E models.
All images (except compilated and screenshots) in this post were generated using OpenAI image generation API. 
According to **Your Content** [Terms of Use](https://openai.com/api/policies/terms/) chapter: "OpenAI hereby assigns to you all its right, title and interest in and to Output."

New users can use credit for $18 (Free trial usage). With this credit, you can **create or edit 900 images 1024x1024**

### API key

First, after registering and confirming your phone number, you need to [Generate your API key](https://beta.openai.com/account/api-keys)

With this API key, we can move forward.

I've created [OpenAI API images Postman collection](https://documenter.getpostman.com/view/2236597/2s8YehTcFr) that users can play with.

### Let's begin with generating the image


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4ejux7vw0xxxaec7uad5.png)

In Postman, when API opaeration body contain `response_format="b64_json"` we will receive base64 image string

POST API operation with body

```
{
    "prompt": "RESTfull API security",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
}
```

We received the following response.
```
{
    "created": 1667860720,
    "data": [
        {
            "b64_json": "iVBORw0KGgoAAA  ...."
        }
    ]
}
```

And then, we need to convert the base64 string into the image.

For this, let's use the following Postman Test script:

```js
var data = JSON.parse(responseBody)

const base64ImgData = `data:image/png;base64, ` + data.data[0].b64_json

const template = `
<img src="{{img}}">
`

pm.visualizer.set(template, {img: base64ImgData})
```

In base64ImgData, I've also concatenated `data:image/png;base64, ` string with b64_json encode string for the correct output in Postman.


And then clicking on the `Visualize` tab, we can see our generated image.



### Create image edit

Here inputs images and the results.


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8z65auneo2826oa7qgdz.png)

For creating your own mask, you can use a free online editor [https://www.photopea.com/](https://www.photopea.com/) or for the background removing [https://www.remove.bg/](https://www.remove.bg/)

**Python function to edit image:** 

```python
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

imageEditB64("DS-1 Death Star in the sky", 1, "1024x1024", "kolochava-ukraine-1024.png", "kolochava-ukraine-1024-mask.png")
```


The result of using the OpenAI library was **OpenAIObject**, so we need to convert it to a string for parsing and next image decoding.

Also, you can check simple Python source code [here](https://github.com/oborys/OpenAI-image-generation-API-script-and-Postman-collection/blob/main/openai_image_api_simple_functions.py).


### Create image variation 


To add a related image needed for an API request in Postman, click the 'Body' tab, and then in the 'VALUE' column, push the 'Select Files' button.


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/74he19t83sgremy83f2s.png)

Regarding API response time* (using my Postman collection)
- Image generations for size 1024x1024 take 6s-8s
- Create image edit for size 1024x1024, takes 15s-17s
- Create image variations for size 1024x1024, takes 12s-14s

> for prompts with 10-195 characters



During my work, I received diferent HTTP error codes, and the response description is excellent and informative.

Missing image
```
400 Bad request
{
    "error": {
        "code": null,
        "message": "'image' is a required property",
        "param": null,
        "type": "invalid_request_error"
    }
}
```

In case if uploaded image size is not one of 256x256, 512x512, or 1024x1024:
401 Unauthorised
```
{
    "error": {
        "code": null,
        "message": "Uploaded image must be a PNG and less than 4 MB.",
        "param": null,
        "type": "invalid_request_error"
    }
}
```

401 Unauthorised
```
{
    "error": {
        "code": null,
        "message": "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY), or as the password field (with blank username) if you're accesing the API from your browser and are prompted for a username and password. You can obtain an API key from https://beta.openai.com.",
        "param": null,
        "type": "invalid_request_error"
    }
}
```

In case the API key is wrong.
```
{
    "error": {
        "code": "invalid_api_key",
        "message": "Incorrect API key provided: sk-***********************. You can find your API key at https://beta.openai.com.",
        "param": null,
        "type": "invalid_request_error"
    }
}
```

But returning the wrong API key in response is not a good idea from a security perspective. For example, imagine that we print API errors in the console or the GUI of our APP with information about errors, and an external audience can see this. 


If you have a problem with limits, you will get the next response
400 Bad request
```
{
    "error": {
        "code": "billing_hard_limit_reached",
        "message": "Billing hard limit has been reached",
        "param": null,
        "type": "invalid_request_error"
    }
}
```









