from __init__ import _message
from generic import EyeTracker

import os
import cv2
import PIL
import numpy

def setup(imgdir=None, mode=u'RGB', **kwargs):
	
	tracker = ImageTracker(imgdir=imgdir, mode=mode, **kwargs)
	
	up = 2490368
	down = 2621440
	left = 2424832
	right = 2555904
	space = 32
	escape = 27

	
	running = True
	while running:
		
		
		success, frame = tracker._get_frame()

		
		if success:

			
			cv2.putText(frame, u"pupthresh = %d" % (tracker._pupt), \
				(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
		
		if success:
			
			cv2.imshow('PyGazeTracker Setup', frame)
			
			keycode = cv2.waitKey(10)
			if keycode != -1:
				print keycode
			if keycode == up:
				tracker._pupt += 1
			elif keycode == down:
				tracker._pupt -= 1
			elif keycode == left:
				tracker._glit -= 1
			elif keycode == right:
				tracker._glit += 1
			elif keycode == space or keycode == escape:
				running = False
	
	return tracker



class ImageTracker(EyeTracker):
	
	def connect(self, imgdir=None, mode=u'RGB', **kwargs):
		

		if not self._connected:
			
			# Set mode and camera number
			self._imgdir = imgdir
			self._mode = mode

			# DEBUG message.
			_message(u'debug', u'images.ImageTracker.connect', \
				u"Checking directory %s." % (self._imgdir))
		
			# Check whether the directory exists.
			if self._imgdir == None:
				_message(u'error', u'images.ImageTracker.connect', \
					u"No directory specified; use the imgdir keyword to pass the path to a directory with eye images.")
			if not os.path.isdir(self._imgdir):
				_message(u'error', u'images.ImageTracker.connect', \
					u"Image directory does not exist ('%s')" \
					% (self._imgdir))
			self._framenames = os.listdir(self._imgdir)
			self._framenames.sort()
			self._framenr = 0
			self._nframes = len(self._framenames)
			self._connected = True

			# DEBUG message.
			_message(u'debug', u'images.ImageTracker.connect', \
				u"Successfully connected to directory %s!" % (self._imgdir))

	
	def _get_frame(self):
		

		if self._framenr >= self._nframes:
			ret = False
			self._connected = False
		# Load the next image.
		else:
			# Construct the path to the current image.
			framepath = os.path.join(self._imgdir, \
				self._framenames[self._framenr])

			frame = cv2.imread(framepath)

			if frame is None:
				ret = False
			else:
				ret = True

			self._framenr += 1
		
		
		if ret:
			# Return the red component of the obtained frame.
			if self._mode == 'R':
				return ret, frame[:,:,2]
			# Return the green component of the obtained frame.
			elif self._mode == 'G':
				return ret, frame[:,:,1]
			# Return the blue component of the obtained frame.
			elif self._mode == 'B':
				return ret, frame[:,:,0]
			# Convert to grey.
			elif self._mode == 'RGB':
				return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# Throw an exception if the mode can't be recognised.
			else:
				_message(u'error', u'webcam.WebCamTracker._get_frame', \
					u"Mode '%s' not recognised. Supported modes: 'R', 'G', 'B', or 'RGB'." \
					% (self._mode))
		
		# If a new frame wasn't available, return None.
		else:
			return ret, None
	
	def _close(self):
		
		"""Doesn't really do anything, but is implemented for consistency's
		sake.
		"""

		# DEBUG message.
		_message(u'debug', u'images.ImageTracker.close', \
			u"Closed connection.")


# # # # #
# DEBUG #
if __name__ == u'__main__':

	import os
	import time
	from matplotlib import pyplot
	
	from __init__ import _EYECASCADE, _FACECASCADE
	import generic

	# Constants
	MODE = 'B'
	DUMMY = True
	DEBUG = False
	IMGDIR = './example'

	# In DUMMY mode, load an existing image (useful for quick debugging).
	if DUMMY:
		filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'test.jpg')
		img = cv2.imread(filepath)
		# Return the red component of the obtained frame.
		if MODE == 'R':
			frame = img[:,:,0]
		# Return the green component of the obtained frame.
		elif MODE == 'G':
			frame = img[:,:,1]
		# Return the blue component of the obtained frame.
		elif MODE == 'B':
			frame = img[:,:,2]
		# Convert to grey.
		elif MODE == 'RGB':
			frame = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		t0 = time.time()
	# If not in DUMMY mode, obtain a frame through the _get_frame method.
	else:
		# Initialise a new tracker instance.
		tracker = ImageTracker(imgdir=IMGDIR, mode=MODE, debug=DEBUG)
		# Get a single frame.
		success = False
		while not success:
			t0 = time.time()
			success, frame = tracker._get_frame()
		# Close the connection with the tracker.
		tracker.close()

	# Cascades
	face_cascade = cv2.CascadeClassifier(_FACECASCADE)
	eye_cascade = cv2.CascadeClassifier(_EYECASCADE)

	# Crop the face and the eyes from the image.
	success, facecrop = generic._crop_face(frame, face_cascade, \
		minsize=(30, 30))
	success, eyes = generic._crop_eyes(facecrop, eye_cascade, \
		Lexpect=(0.7,0.4), Rexpect=(0.3,0.4), maxdist=None, maxsize=None)
	# Find the pupils in both eyes
	B = generic._find_pupils(eyes[0], eyes[1], glint=True, mode='diameter')
	t1 = time.time()

	# Process results
	print("Elapsed time: %.3f ms" % (1000*(t1-t0)))
	pyplot.figure(); pyplot.imshow(facecrop, cmap='gray')
	pyplot.figure(); pyplot.imshow(eyes[0], cmap='gray')
	pyplot.figure(); pyplot.imshow(eyes[1], cmap='gray')
# # # # #
