import webapp2
import jinja2


class IndexHandler(webapp2.RequestHandler):
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                                      autoescape=True)

    def get(self):
        self.response.out.write(self.template_env.get_template('index.html').render())