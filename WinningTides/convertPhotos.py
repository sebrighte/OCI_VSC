import os
from PIL import Image, ImageFont, ImageDraw

workingdir = os.path.abspath(os.getcwd())

# directory = workingdir + f"/WinningTides/Scan"
# for filename in sorted(os.listdir(directory)):
#     f = os.path.join(directory, filename)
#     my_image = Image.open(f)

#     width, height = my_image.size
#     my_image = my_image.resize((int(width/4), int(height/4)),Image.ANTIALIAS)

#     if " n" in filename:my_image.save(workingdir + f"/WinningTides/baseimages/Other/North/{filename}.jpg")
#     if " nw" in filename:my_image.save(workingdir + f"/WinningTides/baseimages/Other/West/{filename}.jpg")
#     if " sw" in filename:my_image.save(workingdir + f"/WinningTides/baseimages/Other/SWest/{filename}.jpg")
#     if " e" in filename:my_image.save(workingdir + f"/WinningTides/baseimages/Other/East/{filename}.jpg")
    
#     print(filename)

directory = workingdir + f"/WinningTides/baseimages/NWest"
my_image = Image.open(f"{directory}/36 nwm2.png")
width, height = my_image.size
my_image = my_image.resize((int(width/4), int(height/4)),Image.ANTIALIAS)
my_image.save(f"{directory}/36-nw-m-2.jpg")

directory = workingdir + f"/WinningTides/baseimages/North"
for filename in sorted(os.listdir(directory)):
    f = os.path.join(directory, filename)

    #my_image = Image.open(f)
    #width, height = my_image.size
    #my_image = my_image.resize((int(width/4), int(height/4)),Image.ANTIALIAS)
    #my_image.save(workingdir + f"/WinningTides/baseimages/North/{filename}")

    # filename2 = filename.replace(" ", "-")
    # filename2 = filename2.replace("-n", "-n-")
    # filename2 = filename2.replace("-m", "-m-")
    # filename2 = filename2.replace(".png", "")
    # filename2 = filename2.replace("-n-", "-n-p-")
    # filename2 = filename2.replace("-p-m", "-m")
    # filename2 = filename2.replace("hw", "0")

    #print(filename,filename2)

    #os.rename(directory + "/" + filename, directory + "/" + filename2)

directory = workingdir + f"/WinningTides/baseimages/East/"
for filename in sorted(os.listdir(directory)):
    f = os.path.join(directory, filename)

    # filename2 = filename.replace(" ", "-")
    # filename2 = filename2.replace("-e", "-e-")
    # filename2 = filename2.replace("-m", "-m-")
    # filename2 = filename2.replace(".png", "")
    # filename2 = filename2.replace("-e-", "-e-p-")
    # filename2 = filename2.replace("-p-m", "-m")
    # filename2 = filename2.replace("hw", "0")

    #print(filename,filename2)

    #os.rename(directory + "/" + filename, directory + "/" + filename2)

directory = workingdir + f"/WinningTides/baseimages/SWest/"
for filename in sorted(os.listdir(directory)):
    f = os.path.join(directory, filename)

    filename2 = filename.replace("p-m", "m")
    # filename2 = filename.replace("p-p", "p")
    # filename2 = filename.replace(" ", "-")
    # filename2 = filename2.replace("-sw", "-sw-")
    # filename2 = filename2.replace("-m", "-m-")
    # filename2 = filename2.replace(".png", "")
    # filename2 = filename2.replace("-sw-", "-sw-p-")
    # filename2 = filename2.replace("-p-m", "-m")
    # filename2 = filename2.replace("hw", "0")

    #print(filename,filename2)

    #os.rename(directory + "/" + filename, directory + "/" + filename2)

directory = workingdir + f"/WinningTides/baseimages/SWest/"
for filename in sorted(os.listdir(directory)):
    f = os.path.join(directory, filename)

    # filename2 = filename.replace(" ", "-")
    # filename2 = filename2.replace("-nw", "-nw-")
    # filename2 = filename2.replace("-m", "-m-")
    # filename2 = filename2.replace(".png", "")
    # filename2 = filename2.replace("-nw-", "-nw-p-")
    # filename2 = filename2.replace("-p-m", "-m")
    # filename2 = filename2.replace("hw", "0")

    #print(filename,filename2)

    #os.rename(directory + "/" + filename, directory + "/" + filename2)
    