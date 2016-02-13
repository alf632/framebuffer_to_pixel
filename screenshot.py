#!/usr/bin/python

import gtk.gdk
import opc
import sys
from PIL import Image

address="172.16.2.217:7890"
MATRIX_WIDTH=128
MATRIX_HEIGHT=64

opcClient = opc.Client(address)

if opcClient.can_connect():
  print('connected to %s' % address)
else:
  print "cannot connect!!"
  sys.exit(1)


while True:
  w = gtk.gdk.get_default_root_window()
  sz = w.get_size()
  pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
  pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
  height=pb.get_height()
  width=pb.get_width()
  
  image = Image.frombuffer("RGB", (width,height) ,pb.pixel_array, 'raw', 'RGB', 0, 1)
  image_width, image_height = image.size
 
  image.thumbnail((MATRIX_WIDTH, MATRIX_HEIGHT), Image.ANTIALIAS) 
  x_offset=0
  y_offset=0
  cropped_image = image.crop((
              0+x_offset,  # left
              0+y_offset,  # upper
              MATRIX_WIDTH + x_offset,  # right
              MATRIX_HEIGHT + y_offset  # lower
          ))
  data = cropped_image.tobytes()
  opcClient.put_data(data, channel=0)
