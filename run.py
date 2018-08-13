from app import app
from app.views import cmdb

#蓝图注册
app.register_blueprint(blueprint=cmdb,url_prefix='/cmdb')

app.run(
    host='0.0.0.0',
    port=8080,
    debug=True,
)