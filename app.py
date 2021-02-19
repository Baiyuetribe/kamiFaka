
from sqlalchemy.sql.expression import false
from werkzeug.utils import redirect
from service.api.db import app

# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from service.api.user import base
from service.api.admin import admin
from service.api.common import common
# app.register_blueprint(base)
from flask_apscheduler import APScheduler
from service.util.auto_task import clean_tmp_order

bps = [base,admin,common]
[app.register_blueprint(bp) for bp in bps]

scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
# scheduler.add_job(func=change_price, id='change_price_job', trigger='interval', seconds=3, replace_existing=True)
scheduler.add_job(func=clean_tmp_order, id='clean_tmp_order', trigger='cron', day_of_week ='0-6',hour = 4,minute = 27,second = 0, replace_existing=True)
scheduler.start()

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')    