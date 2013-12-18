import webapp2

from handlers import IndexHandler

app = webapp2.WSGIApplication(
    [
        ('/', IndexHandler)
    ],
    debug=True
)