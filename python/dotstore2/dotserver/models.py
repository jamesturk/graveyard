from google.appengine.ext import db
from google.appengine.ext import blobstore

class UserDetail(db.Model):
    email = db.EmailProperty(required=True)
    password_hash = db.StringProperty(required=True)
    current_token = db.StringProperty(required=True)
    token_expiration = db.DateProperty()

class File(db.Model):
    owner = db.ReferenceProperty(UserDetail, collection_name='files')
    path = db.StringProperty()
    upload_time = db.DateTimeProperty(auto_now=True)
    mtime = db.FloatProperty()
    hash = db.StringProperty()
    blob = blobstore.BlobReferenceProperty()
