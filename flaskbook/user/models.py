from mongoengine import signals
from flask import url_for
import os

# APP MODULES
from application import db
from utilities.common import utc_now_ts as now
from settings import STATIC_IMAGE_URL, AWS_BUCKET, AWS_CONTENT_URL

class User(db.Document):
    username = db.StringField(db_field="u", required=True, unique=True)
    password = db.StringField(db_field="p", required=True)
    email = db.EmailField(db_field="e", required=True, unique=True)
    first_name = db.StringField(db_field="fn", max_length=50)
    last_name = db.StringField(db_field="ln", max_length=50)
    created = db.IntField(db_field="c", default=now())
    bio = db.StringField(db_field="b", max_length=160)
    email_confirmed = db.BooleanField(db_field="ecf", default=False)
    change_configuration = db.DictField(db_field="cc")
    profile_image = db.StringField(db_field="i", default=None)
    
    # lowercase the username and email
    @classmethod
    def pre_save(cls, sender, document, **kwargs): #class, sender(who's sending this method), document(actual document we are going to save) 
        # builtin mongoengine method (presave) => This method is call before every object is written to the database
        document.username = document.username.lower()
        document.email = document.email.lower()
    
    def profile_imgsrc(self, size):
        if self.profile_image:
            if AWS_BUCKET:
                return os.path.join(AWS_CONTENT_URL, AWS_BUCKET, 'user', '%s.%s.%s.png' % (self.id, self.profile_image, size) )
            else:
                return url_for('static', filename=os.path.join(STATIC_IMAGE_URL, 'user', '%s.%s.%s.png' % (self.id, self.profile_image, size) ))
        else:
            return url_for('static', filename=os.path.join(STATIC_IMAGE_URL, 'user', 'no-profile.%s.png' % (size) ))
            
    meta = {
        'indexes': ['username', 'email', '-created'] #poniendo el - delante decimos que sea en orden inverso (los mas recientes primero en el caso del campo created)
    }

# signals es la forma en que mongodb utiliza el method pre_save
signals.pre_save.connect(User.pre_save, sender=User)