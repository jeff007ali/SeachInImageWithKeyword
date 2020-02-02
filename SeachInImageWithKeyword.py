import sys

from PIL import Image
import pytesseract
import glob, os
import shutil
import pyexiv2

currentPath = os.getcwd()
print ("The current working directory is {}".format(currentPath))

path = input("Enter images folder path : ")
# change the current working directory to specified path
os.chdir(path)

keyword = input("Enter search keyword : ").lower()

outputPath = "%s/output_%s" % (path, keyword)
try:
    os.mkdir(outputPath)
except OSError:
    print ("Creation of the directory {} failed".format(outputPath))
else:
    print ("Successfully created the directory {}".format(outputPath))

for file in glob.glob("*.png"):
    # To get exif data using pyexiv library we have to create image object
    exiv_image = pyexiv2.Image(file)

    # To clear exif data of all images
    if keyword == "clear exif data":
        exiv_image.clear_exif()    
        continue

    # Read EXIF data of image
    exif_data = exiv_image.read_exif()
    # Check if exif data of text_from_image is present or not
    if exif_data.get('Exif.Photo.UserComment'):
        text_from_image = exif_data.get('Exif.Photo.UserComment')
    
    else:
        pillow_image = Image.open(file)
        # image_to_string() this function can work if we pass image name directly
        # no need to create Image object.
        # TODO : Check the impact of directly passing image name in argument over image object
        text_from_image = pytesseract.image_to_string(pillow_image, lang="eng")
        text_from_image = text_from_image.replace("\n", "").lower()

        # TODO : Add text_from_image as dictionary not as direct string for future enhancement
        exif_data['Exif.Photo.UserComment'] = text_from_image
        exiv_image.modify_exif(exif_data)

    if(keyword in text_from_image):
        try:
            shutil.copy(file, outputPath)
        except IOError as e:
            print("Unable to copy file. {}".format(e))
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            exit(1)

if keyword == "clear exif data":
    print("EXIF data of all images are deleted")
else: 
    print("Done with searching")


# see exiv2’s documentation for a list of valid EXIF tags : https://exiv2.org/tags.html
