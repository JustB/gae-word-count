import webapp2

from handlers import IndexHandler
from handlers import UploadHandler

app = webapp2.WSGIApplication(
    [
        ('/', IndexHandler),
        ('/upload', UploadHandler)
    ],
    debug=True
)