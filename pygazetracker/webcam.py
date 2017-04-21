from __init__ import _message
from generic import EyeTracker

import cv2
import PIL
import numpy

def setup(camnr=0, mode=u'RGB', **kwargs):
	
	
	tracker = WebCamTracker(camnr=camnr, mode=mode, **kwargs)
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

class WebCamTracker(EyeTracker):
	
	
	def connect(self, camnr=0, mode=u'RGB', **kwargs):
		
		if not self._connected:
			
			
			self._camnr = camnr
			self._mode = mode

			_message(u'debug', u'webcam.WebCamTracker.connect', \
				u"Connecting to webcam %d." % (self._camnr))
		
			
			self._vidcap = cv2.VideoCapture(self._camnr)
			self._connected = True

			
			_message(u'debug', u'webcam.WebCamTracker.connect', \
				u"Successfully connected to webcam %d!" % (self._camnr))

	
	def _get_frame(self):
		
		
		ret, frame = self._vidcap.read()
		
				
		if ret:
			
			if self._mode == 'R':
				return ret, frame[:,:,2]
			
			elif self._mode == 'G':
				return ret, frame[:,:,1]
			
			elif self._mode == 'B':
				return ret, frame[:,:,0]
			
			elif self._mode == 'RGB':
				return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
			else:
				_message(u'error', u'webcam.WebCamTracker._get_frame', \
					u"Mode '%s' not recognised. Supported modes: 'R', 'G', 'B', or 'RGB'." \
					% (self._mode))
		
		
		else:
			return ret, None
	
	def _close(self):
		
		
		_message(u'debug', u'webcam.WebCamTracker.close', \
			u"Disconnecting from webcam.")

		
		self._vidcap.release()

		
		_message(u'debug', u'webcam.WebCamTracker.close', \
			u"Successfully disconnected from webcam.")



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

	if DUMMY:
		filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'test.jpg')
		img = cv2.imread(filepath)
		if MODE == 'R':
			frame = img[:,:,0]
		elif MODE == 'G':
			frame = img[:,:,1]
		elif MODE == 'B':
			frame = img[:,:,2]
		elif MODE == 'RGB':
			frame = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		t0 = time.time()
	else:
		tracker = WebCamTracker(camnr=0, mode=MODE, debug=DEBUG)
		success = False
		while not success:
			t0 = time.time()
			success, frame = tracker._get_frame()
		tracker.close()

	face_cascade = cv2.CascadeClassifier(_FACECASCADE)
	eye_cascade = cv2.CascadeClassifier(_EYECASCADE)

	success, facecrop = generic._crop_face(frame, face_cascade, \
		minsize=(30, 30))
	success, eyes = generic._crop_eyes(facecrop, eye_cascade, \
		Lexpect=(0.7,0.4), Rexpect=(0.3,0.4), maxdist=None, maxsize=None)
	B = generic._find_pupils(eyes[0], eyes[1], glint=True, mode='diameter')
	t1 = time.time()

	print("Elapsed time: %.3f ms" % (1000*(t1-t0)))
	pyplot.figure(); pyplot.imshow(facecrop, cmap='gray')
	pyplot.figure(); pyplot.imshow(eyes[0], cmap='gray')
	pyplot.figure(); pyplot.imshow(eyes[1], cmap='gray')