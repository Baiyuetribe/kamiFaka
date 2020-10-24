
from service.api.db import app

# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from service.api.user import base
from service.api.admin import admin
from service.api.common import common
# app.register_blueprint(base)

bps = [base,admin,common]
[app.register_blueprint(bp) for bp in bps]

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')    