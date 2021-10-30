try:
  import requests
except ModuleNotFoundError:
  print("Download dependencies first!")

def get_image(gender,age):
  try:
    url = "https://fakeface.rest/face/json?maximum_age={}&gender={}"\
      .format(age,gender)
    response = requests.get(url).json()
    return response['image_url']
  except Exception as ex:
    print("Get Image: ",ex)

def password_is_valid(string):
  return len(string) > 5
  #return True if (re.fullmatch(r'^[A-Za-z0-9@#$%^&+=]{8,}$',string)) else False

