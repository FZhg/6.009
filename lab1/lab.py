#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

def blur_kernel(size, c=1):
    """
    return a box blur kernel if a given size n*n,
    the parameter c is used to scale the value of
    the kernel element
    """
    return [[c/size**]]

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_indice(self, x, y):
        """
        return the indice in the list pixels
        if the pixel is in position (x,y)
        """
        return y * self.width + x

    def get_pixel(self, x, y):
        """
        give the pixel value at position (x, y)
        return the edge pixels if the (x,y) falls out of the bound of the image
        """
        x = max(min(self.width-1, x), 0)
        y = max(min(self.height-1, y), 0)
        return self.pixels[self.get_indice(x, y)]

    def set_pixel(self, x, y, c):
        """
        set the pixel at postion (x, y) to a new value c
        """
        self.pixels[self.get_indice(x, y)] = c

    def apply_per_pixel(self, func):
       result = Image.new(self.width, self.height)
       for x in range(result.width):
           for y in range(result.height):
               color = self.get_pixel(x, y)
               newcolor = func(color)
               result.set_pixel(x, y, newcolor)
       return result

    def inverted(self):
        return self.apply_per_pixel(lambda c: 255-c)
    
    def correlate(self, kernel):
        """
        give back the image munipulated by the kernel;
        kernel is represented as a list of lists, where the sub lists
        are the rows of the kernel.
        kernel are assumed to be square, and odd demensions.
        first compute the kernel output for a single pixel
        then loop over all pixels and update to form the result image
        """
        #sqrt returns a float use int to round to an interger
        ker_size = len(kernel)
        
        #the biggest difference of position between the targeted pixel and pixels around it
        #the first pixel to multiply with a kernel element
        init = ker_size // 2
        
        def one_pixel_ker(im, x, y, kernel):
            """
            compute the kernel output for a single pixel
            """
            out = 0
            for i in range(ker_size):
                for j in range(ker_size):
                    out = out + kernel[j][i] * self.get_pixel(x-init+i, y-init+j)
            return out

        #loop over all pixels
        result = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                newcolor = one_pixel_ker(self, x, y, kernel)
                result.set_pixel(x, y, newcolor)
        return result

    def clipper(self):
        """
        round to interger.
        truncate the pixel value in the range[0,255].
        loop over all the pixels
        """
        
        def inner(c):
            """
            c is the value of the pixel.
            the inner fucntion deals with a single pixel
            """
            c = int(c)
            return max(0, min(c, 255))
        return self.apply_per_pixel(inner)

        
    def blurred(self, n):
        """
        use a n dimension box-blur kernel,
        the kernel whose element values are 1/n,
        identical that sum to 1, to input into the correlate method,
        and output a blurred image.
        """
        result = self.correlate(kernel)
        return result.clipper()

    def sharpened(self, n):
        """
        first caculate the sharpen kernel
        the kernel is same as the blurring one except the middle is 2-1/n**2
        correlate the kernel and the image
        cipper it to ensure every pixel is an interger in range[0,256]
        """
        kernel = []
        for i in range(n**2):
        if i == (n**2+1)/2:
            kernel.append(2-1/n**2)
        else:
                kernel.append(1/n**2)
        print(kernel)
        result = self.correlate(kernel)
        return result.clipper()
            
        
                    
                
                
                
                    
            


    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            oimg = PILImage.open(img_handle)
            img = oimg.convert('L')
            w, h = img.size
            d = list(img.getdata())
            return cls(w, h, d)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
