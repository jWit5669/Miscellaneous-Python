# A bunch of imports that I most definitely do not need all of
from PIL import Image
import pandas as pd
import shutil
import csv
import os
import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
os.chdir("VanGogh/vincent-van-gogh/vincent-van-gogh")

#Basically, going through every folder and every picture and adding
#relevant data such as name and dimension to the array
arry = []
for folder in os.listdir("."):

  for images in os.listdir(folder):

      if ( images.endswith( ".jpg" ) ):
        img = Image.open( "./" + folder + "/" + images)
        arry.append( [ images, folder, img.width, img.height ] )

#storing the array to a csv in case I want to use it later on
with open('picData.csv', 'w') as f:
    writer = csv.writer(f)
    for x in arry:
      writer.writerow(x)

#moving the picData file out of main directory
shutil.move('./picData.csv', '../../picData.csv')

#reading in picData as a pandas DataFrame
picDF = pd.read_csv( "../../picData.csv", names = [ 'Name', 'Year', 'Width', 'Height' ] )

#takes random picture, picks it apart by the frequency of each color, and rearranges the pixels
def generatePic(orientation):

    #psuedorandomly generated number to choose picture from
    index = random.randint(0, len(picDF) - 1)
    im = Image.open('./' + str(picDF['Year'].iloc[index]) + '/' + str(picDF['Name'].iloc[index]))
    pix = im.load()
    print(im.size)
    plt.imshow(im)
    plt.show()

    #I have no clue why I initialized colors this way
    #Colors is just an array of all of the pixels in order and their RGB value
    colors = [3]
    for y in range(0, im.height):
        for x in range(0, im.width):
            colors.append(pix[x, y])

    #This makes a frequency set of all the colors and how many times they occur
    data = Counter(colors)
    most = data.most_common()
    print(most[0][0])

    #Fill in a color "block" with all of the colors for the number of times they occur in order of most to least frequent
    colorBlock = []
    for x in most:
        for y in range(0, x[1]):
            colorBlock.append(x[0])
    print(len(colorBlock))

    #Creating a matrix to store colors in because I know I can convert it to plt picture
    nMat = np.zeros((im.height, im.width), dtype=(int, 3))

    #nice option to choose how the pixels are oriented when placed
    if orientation == 1:
        for x in range(im.width):
            for y in range(im.height):
                nMat[y][x] = colorBlock[(y + 1) * x]

    elif orientation == 2:
        count = 0
        for x in range(im.height):
            for y in range(im.width):
                nMat[x][y] = colorBlock[count]
                count += 1

    else:
        count = 0
        for x in range(im.width):
            for y in range(im.height):
                nMat[y][x] = colorBlock[count]
                count += 1

  plt.imshow(nMat)
  plt.show()  

  if int( input( "Would you like to save the image? " ) ) == 1:
    im = Image.fromarray((nMat * 1).astype(np.uint8))
    im1 = im.save("fard.jpg")


def main():
    generatePic( int(input("Enter 1 for Diagonal, 2 for Horizontal, 3 for Vertical: ")))

main()
