import logging
import datetime
import random
import hashlib
import json
import urllib

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import blobstore_handlers

from dotserver.models import UserDetail, File

def _check_token(request):
    token = request.headers.get('x-dotstore-token', request.get('_token'))
    return UserDetail.all().filter('current_token =', token).get()

def _make_token(email):
    return hashlib.sha1(email +
                        str(random.randint(0, 10000000)) +
                        str(datetime.datetime.now())).hexdigest()

class ApiRequestHandler(webapp.RequestHandler):
    def _return_json(self, obj):
        if not isinstance(obj, basestring):
            obj = json.dumps(obj, default=
                             lambda o: o.isoformat() if isinstance(o, datetime.datetime) else None)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(obj)

class RegisterHandler(ApiRequestHandler):
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        if not email or not password:
            self.error(400)
            self.response.out.write('Missing parameter')
            return

        if UserDetail.all().filter('email', email).count():
            self.error(400)
            self.response.out.write('email already registered')
        else:
            password_hash = hashlib.sha1(password).hexdigest()
            ud = UserDetail(email=email, password_hash=password_hash,
                            current_token=_make_token(email),
                            token_expiration=datetime.date.today() +
                            datetime.timedelta(days=60))
            ud.put()
            self._return_json('{"token": "%s"}' % ud.current_token)


class GetTokenHandler(ApiRequestHandler):
    def get(self):
        email = self.request.get('email')
        password = self.request.get('password')

        password_hash = hashlib.sha1(password).hexdigest()
        user = UserDetail.all().filter('email', email).get()

        if user and user.password_hash == password_hash:
            self._return_json('{"token": "%s"}' % user.current_token)
        elif not user:
            self.error(403)
            self.response.out.write('No Such User')
        else:
            self.error(403)
            self.response.out.write('Invalid Password')


class GetUploadUrlHandler(ApiRequestHandler):
    def get(self):
        if _check_token(self.request):
            self.response.out.write(blobstore.create_upload_url("/api/upload_file"))
        else:
            self.error(403)
            self.response.out.write('bad token')

class SuccessHandler(ApiRequestHandler):
    def get(self):
        self.response.out.write('upload success')

class FileListHandler(ApiRequestHandler):
    def get(self):
        ud = _check_token(self.request)
        if ud:
            file_list = [{'path': f.path, 'upload_time': f.upload_time,
                          'mtime': f.mtime, 'hash': f.hash} for f in ud.files]
            self._return_json(file_list)
        else:
            self.error(403)
            self.response.out.write('bad token')


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        ud = _check_token(self.request)
        if ud:
            path = self.request.get('path')
            mtime = float(self.request.get('mtime'))
            blob_info = self.get_uploads('file')[0]

            # calculate the hash of the file contents
            br = blobstore.BlobReader(blob_info.key())
            value = br.read()
            filehash = hashlib.sha1(value).hexdigest()

            # just save a new File -- when retrieving we grab by upload_time
            fileobj = File(owner=ud, path=path, hash=filehash,
                           mtime=mtime, blob=blob_info)
            fileobj.put()
            self.redirect('/api/success')
        else:
            self.error(403)
            self.response.out.write('bad token')


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        ud = _check_token(self.request)
        if ud:
            path = self.request.get('path')
            fileobj = ud.files.filter('path', path).get()
            if fileobj:
                self.send_blob(fileobj.blob)
            else:
                self.error(404)
                self.response.out.write('no such file')
        else:
            self.error(403)
            self.response.out.write('bad token')


def main():
    """
        /api/register
            POST username/password to register a new user
        /api/get_token?username=&password=
            test a user's login and password, returns a current API key
        /api/get_upload_url
            return a URL to post to
        /api/file_list
            get list of files
            {'path': '...', 'md5': 'xyz', 'modtime': 123}
        /api/upload_file
            POST a zip file containing all new files
        /api/get_file/<path>
            return contents of file
    """
    application = webapp.WSGIApplication([
        ('/api/register', RegisterHandler),
        ('/api/get_token', GetTokenHandler),
        ('/api/success', SuccessHandler),
        ('/api/get_upload_url', GetUploadUrlHandler),
        ('/api/file_list', FileListHandler),
        ('/api/upload_file', UploadHandler),
        ('/api/download_file', DownloadHandler),
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
