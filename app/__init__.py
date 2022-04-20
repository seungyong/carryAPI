import os

# config
from dotenv import load_dotenv

from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, ProductionConfig

"""
    api => 라우팅을 위한 파일
    model => 객체 모델을 정의
    service => 실제 로직이 돌아가는 곳
    util => 암호화, jwt 토큰 등 각종 기능 폴더
"""

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Carry Project',
          version='1.0',
          description='Python Flask를 이용한 API 서버'
          )

load_dotenv(verbose=True)
ENVIRONMENT = os.getenv('FLASK_ENV')


def create_app(config_name):
    app = Flask(__name__)
    app.register_blueprint(blueprint)

    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)

    app.app_context().push()

    return app


app = create_app(ENVIRONMENT)
db = SQLAlchemy(app)
Session = db.create_session(options={
    'autocommit': False,
    'autoflush': False,
    'bind': db.engine
})
session = Session()
migrate = Migrate(app, db)

# API
from .main.api import *
