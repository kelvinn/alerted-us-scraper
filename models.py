import logging
from google.appengine.ext import ndb


class Settings(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.StringProperty()

  @staticmethod
  def get(name, backup_value):
    NOT_SET_VALUE = backup_value
    retval = Settings.query(Settings.name == name).get()
    if not retval:
        retval = Settings()
        retval.name = name
        retval.value = NOT_SET_VALUE
        retval.put()
    if retval.value == NOT_SET_VALUE:
        logging.info("Had to set default name")
    return retval.value

