from app import db
from config import DevelopmentConfig
from migrate.versioning import api
import os

SQLALCHEMY_DATABASE_URI = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = DevelopmentConfig.SQLALCHEMY_MIGRATE_REPO

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))