try:
  import requests,re
except ModuleNotFoundError:
  print("Download dependencies first!")

def get_image(gender,age):
  try:
    url = "https://fakeface.rest/face/json?maximum_age={}&gender={}"\
      .format(age,gender)
    print("URL",url)
    response = requests.get(url.lower()).json()
    return response['image_url']
  except Exception as ex:
    print("Get Image: ",ex)

def password_is_valid(string):
  return True if (re.fullmatch(r'^[A-Za-z0-9@#$%^&+=]{8,}$',string)) else False

