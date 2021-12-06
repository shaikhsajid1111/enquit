import base64

def convert_images_to_base64_list(li):
  base64_list = []
  for file in li:
    image_string = base64.b64encode(file.read())
    base64_list.append(image_string.decode("utf-8"))

  return str(base64_list)
