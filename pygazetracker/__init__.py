import os

_VERBOSITY = 2


_DEBUG = False


_DIR = os.path.abspath(os.path.dirname(__file__)).decode(u'utf-8')
# Get the directory for DEBUG images.
_DEBUGDIR = os.path.join(_DIR, 'DEBUG')
# Face detection cascade from:
# https://github.com/shantnu/FaceDetect
_FACECASCADE = os.path.join(_DIR, u'haarcascade_frontalface_default.xml')
# Eye detection cascade from:
# http://www-personal.umich.edu/~shameem/haarcascade_eye.html
_EYECASCADE = os.path.join(_DIR, u'haarcascade_eye.xml')


def _message(msgtype, sender, msg):
	
	if msgtype == u'error':
		raise Exception(u"ERROR in pygazetracker.%s: %s" \
			% (sender, msg))
	
	elif msgtype == u'warning' and _VERBOSITY >= 1:
		print(u"WARNING in pygazetracker.%s: %s" % (sender, msg))
	
	elif msgtype == u'message' and _VERBOSITY >= 2:
		print(u"MSG from pygazetracker.%s: %s" % (sender, msg))
	
	elif msgtype == u'debug' and _VERBOSITY >= 3:
		print(u"DEBUG pygazetracker.%s: %s" % (sender, msg))