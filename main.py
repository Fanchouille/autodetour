import os
from fastapi import FastAPI, File, UploadFile
import uvicorn

import torch
import numpy as np

from sod.utils import parse_config
from sod.model import BASNet, infer

from starlette.responses import HTMLResponse
from starlette.responses import FileResponse
from skimage import io
from PIL import Image

app = FastAPI()

# Get environment from env variable
environment = os.environ["ENVIRONMENT"] if ("ENVIRONMENT" in os.environ) else "development"

# Load configuration from ENVIRONMENT variable
conf = parse_config(path="./config/{}.yml".format(environment))

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

net = BASNet(3, 1)
net.load_state_dict(torch.load(conf["model_path"]))
if torch.cuda.is_available():
    net.cuda()
net.eval()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/get-detour")
async def get_detour(file: UploadFile = File(...)):
    try:
        os.remove("output.png")
    except:
        pass
    img = Image.open(file.file)  # img is from PIL.Image.open(path)
    img = img.convert('RGB')
    mask = infer(np.asarray(img), net)
    empty = Image.new("RGBA", img.size, 0)
    img_detour = Image.composite(img, empty, mask.convert("L"))
    img_detour.save("output.png")
    headers = {
        "Content-Type": 'image',
        "Content-Disposition": 'attachment; filename="{}"'.format("output.png")
    }
    response = FileResponse("output.png", headers=headers)
    return response

@app.post("/get-mask")
async def get_detour(file: UploadFile = File(...)):
    try:
        os.remove("output.png")
    except:
        pass
    img = Image.open(file.file)  # img is from PIL.Image.open(path)
    img = img.convert('RGB')
    mask = infer(np.asarray(img), net)
    mask.convert("L").save("mask.png")
    headers = {
        "Content-Type": 'image',
        "Content-Disposition": 'attachment; filename="{}"'.format("mask.png")
    }
    response = FileResponse("mask.png", headers=headers)
    return response


@app.get("/detour")
async def get_detour_file():  # add multiple if needed #style="display: none;"
    content = """
       <html>
       <body>
       </form>
           <form action="/get-detour/" enctype="multipart/form-data" method="post">
           <input type="file" name="file"></label>
           <input type="submit" value="Go">
       </form>
       </body>
       </html>
   """
    return HTMLResponse(content=content)

@app.get("/mask")
async def get_mask_file():  # add multiple if needed #style="display: none;"
    content = """
       <html>
       <body>
       </form>
           <form action="/get-mask/" enctype="multipart/form-data" method="post">
           <input type="file" name="file"></label>
           <input type="submit" value="Go">
       </form>
       </body>
       </html>
   """
    return HTMLResponse(content=content)


#
#    headers = {
#        "Content-Type": 'image',
#        "Content-Disposition": 'attachment; filename="{}"'.format(filename),
#    }
#    return FileResponse(filename, headers=headers)


# @app.get("/")
# async def main():  # add multiple if needed #style="display: none;"
#   content = """
#       <html>
#       <body>
#       </form>
#           <form action="/file2docx/" enctype="multipart/form-data" method="post">
#           <input type="file" name="file"></label>
#           <input type="submit" value="Go">
#       </form>
#       </body>
#       </html>
#   """
#   return HTMLResponse(content=content)


if __name__ == '__main__':
    # main()
    uvicorn.run("main:app")
