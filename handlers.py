import webapp2
import jinja2
from google.appengine.api import users


class IndexHandler(webapp2.RequestHandler):
    """
    This is the main page. Here the user can upload new data and run MapReduce jobs.
    """
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                                      autoescape=True)

    def get(self):
        user = users.get_current_user()
        username = user.nickname()
        logout_url = users.create_logout_url('/')

        self.response.out.write(self.template_env.get_template('index.html').render(
            {
                'username': username,
                'logout_url': logout_url
            }
        ))