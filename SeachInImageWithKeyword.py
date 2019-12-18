import sys

from PIL import Image
import pytesseract
import glob, os
import shutil

currentPath = os.getcwd()
print ("The current working directory is %s" % currentPath)

path = input("Enter folder path : ")
os.chdir(path)

keyword = input("Enter keyword : ")

outputPath = "%s/output_%s" % (path, keyword)
try:
    os.mkdir(outputPath)
except OSError:
    print ("Creation of the directory %s failed" % outputPath)
else:
    print ("Successfully created the directory %s " % outputPath)

for file in glob.glob("*.png"):
    im = Image.open(file)
    text = pytesseract.image_to_string(im, lang="eng")
    #TO DO : If image is processed once then store retrieved text in JSON file, it will reduce processing time of image.

    if(keyword in text):
        try:
            shutil.copy(file, outputPath)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            exit(1)

print("Done with searching")
