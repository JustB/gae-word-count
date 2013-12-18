import datetime
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from models import FileMetadata
from pipelines import WordCountPipeline


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    """
    This handler upload data to the blobstore
    """
    def post(self):
        upload_files = self.get_uploads('file')
        blob_key = upload_files[0].key()
        name = self.request.get('name')
        user = users.get_current_user()
        username = user.nickname()
        date = datetime.datetime.now()
        str_blob_key = str(blob_key)

        key = FileMetadata.getKeyName(username, date, str_blob_key)
        m = FileMetadata(key_name=key)
        m.filename = name
        m.uploadedOn = date
        m.owner = user
        m.blobkey = str_blob_key
        m.put()

        self.redirect('/')


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
        upload_url = blobstore.create_upload_url("/upload")

        first = FileMetadata.getFirstKeyForUser(username)
        last = FileMetadata.getLastKeyForUser(username)
        q = FileMetadata.all()
        q.filter('__key__ >', first)
        q.filter('__key__ <', last)
        results = q.fetch(10)
        items = [_ for _ in results]
        length = len(items)

        self.response.out.write(self.template_env.get_template('index.html').render(
            {
                'username': username,
                'logout_url': logout_url,
                'upload_url': upload_url,
                'items': items,
                'length': length
            }
        ))

    def post(self):
        filekey = self.request.get('filekey')
        blobkey = self.request.get('blobkey')
        # Start pipelines
        pipeline = WordCountPipeline(filekey, blobkey, with_combiner=False)
        pipeline.start()
        self.redirect(pipeline.base_path + '/status?root=' + pipeline.pipeline_id)