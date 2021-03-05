from sqlalchemy.orm import query
from service.database.models import TempOrder
from service.api.db import db
from datetime import datetime,timedelta

def clean_tmp_order():
    orders = TempOrder.query.all()
    c_now = datetime.utcnow()+timedelta(hours=8)
    # del_list = []
    if orders:
        with db.auto_commit_db():
            for i in orders:
                if (c_now - i.to_date()['updatetime']).days > 5:
                    # del_list.append(i)
                    db.session.delete(i)
        
