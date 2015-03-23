import png  #a module that simplifies the process of reading and writing images

#writes a greyscale image to a file with the specified filename
def write_image(filename, image):
    print 'writing image...'
    height = len(image)
    width = len(image[0])
    file = open(filename, 'wb')
    w = png.Writer(width, height, greyscale=True)
    w.write(file, image)
    file.close()
    print 'image saved as', filename
