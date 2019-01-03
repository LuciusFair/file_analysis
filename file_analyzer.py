#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from PIL import Image
    import logging
    import argparse
except ImportError:
    print "Please check the prerequisites: PIL (pillow), logging and argparse module."
    quit(1)

def pick_colour(my_byte):
    if my_byte <= 9:
        c_red = 243
        c_green = 229
        c_blue = 171
    elif my_byte == 10 or my_byte == 13:
        c_red = 255
        c_green = 216
        c_blue = 1
    elif (my_byte >= 97 and my_byte <= 122) or (my_byte >= 65 and my_byte <= 90):
        c_red = 82
        c_green = 208
        c_blue = 23
    elif my_byte >= 48 and my_byte <= 57:
        c_red = 128
        c_green = 128
        c_blue = 217
    elif my_byte > 128:
        c_red = 247
        c_green = 13
        c_blue = 26
    else:
        c_red = 255
        c_green = 255
        c_blue = 255

    return(c_red, c_green, c_blue)



# Start Logging
logging.basicConfig(filename="./log_file_analyzer.txt", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("Start of program file_analyzer.py")

# command-line arguments
parser = argparse.ArgumentParser(description='Show image of file structure.')
parser.add_argument("-i", "--input", help="File to be analyzed")
parser.add_argument("-o", "--output", help="Output file (image)")
parser.add_argument("-c", "--colour", help="colour (rate) bytes", action="store_true")
args = parser.parse_args()

if args.input:
    logging.info("Input file has been set to %s via command-line argument." % (args.input))

    # Can I read the input file?
    try:
        filehandle = open(args.input, 'r')
    except IOError:
        logging.error("Unable to read file %s" % (args.input))
        # User has a right to know
        print "Unable to read file %s" % (args.input)
        exit(2)

    my_infile = args.input
else:
    #my_infile = "/tmp/textfile.txt.bfe"
    print "No suitable file found. Please check the Syntax with the -h option."
    exit(2)

if args.output:
    my_outfile = args.output
else:
    #my_outfile = my_infile + '.bmp'
    my_outfile = '/tmp/file_analyzer.bmp'

with open(my_infile, 'rb') as my_file:
    my_file.seek(0, 2)
    my_size = my_file.tell()
    my_file.seek(0, 0)

    logging.debug("Filesize is %d Bytes" % (my_size))

    if my_size < 80:
        logging.error("File too small (%d Bytes)" % (my_size))
        # User has a right to know
        print "File too small (%d Bytes)" % (my_size)
        quit(3)

    my_ydim = 640 # At the moment, the picture will always be 640 pixels on the vertical axis
    my_xdim = (my_size / my_ydim) + 1

    my_maxsize = (my_xdim * my_ydim * 8) + 1

    logging.debug("Dimensions: x = %d | y = %d" % (my_xdim, my_ydim))

    my_bild = Image.new( 'RGB', (my_xdim, my_ydim), "black") # create a new black image
    my_pixels = my_bild.load() # create the pixel map

    my_seekindex = 0
    my_bildindex = 0

    for x in range (0, my_xdim):
        for y in range(0, my_ydim, 8):
            my_seektarget = my_seekindex
            my_file.seek(my_seektarget, 0)
            my_byte = my_file.read(1)

            for c in my_byte:
                if args.colour == True:
                    c_red, c_blue, c_green = pick_colour(ord(my_byte))
                else:
                    c_red = 255
                    c_green = 255
                    c_blue = 255

                my_binbyte = bin(ord(c))[2:].zfill(8)
                for pixel in range(0,8):
                    if int(my_binbyte[pixel]) == 1:
                        my_pixels[x,y+pixel] = (c_red, c_green, c_blue) # set the colour accordingly

            #logging.debug("x %d | y %d | byte %s | binbyte %s" % (x, y, str(my_byte), str(my_binbyte)))

            my_seekindex = my_seekindex + 1
            if (my_seekindex > my_maxsize):
                logging.error("seekindex %d > maxsize %d | x = %d | y = %d" % (my_seekindex, my_maxsize, x, y))
                # call it a day
                quit()
# Uncomment next line to show pic after generation
#my_bild.show()

try:
    my_bild.save(my_outfile)
    print "Image saved as %s" % (my_outfile)
except:
    print "Sorry, Image couldn't be saved - check filenames and permissions."
    exit(8)
