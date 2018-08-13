#升级数据库

from migrate.versioning import api
from config import DevelopmentConfig

SQLALCHEMY_DATABASE_URI = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = DevelopmentConfig.SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))