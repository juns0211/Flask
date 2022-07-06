from flask import request, Response, session, abort
from flask.views import MethodView
from sqlalchemy import exc
from user import user_db
import json, traceback
from flasgger import swag_from
from configs.config import validation_error_handler, validation_function
import pandas as pd

# 上傳檔案API
class upload_view(MethodView):
    @swag_from('spec/upload_post.yaml')
    def post(self):
        try:
            csv = request.files.get('file', None)
            if not csv:
                return Response(json.dumps({'success':False, 'message':'無上傳內容'}, ensure_ascii=False), status=200, mimetype='application/json')
            datas = pd.read_csv(csv)
            if sorted(['name', 'acc', 'password']) != sorted(list(datas.columns)):
                return Response(json.dumps({'success':False, 'message':'csv欄位名稱錯誤, 依序 name > acc > password'}, ensure_ascii=False), status=200, mimetype='application/json')
            user_db.db.session.add_all(
                                        [user_db.mysql_db(**{'name':str(data['name']), 'acc':str(data['acc']), 'password':str(data['password'])})
                                            for data in datas.to_dict('recode')]
                                        )
            user_db.db.session.commit()
            return Response(json.dumps({'success':True, 'message':''}, ensure_ascii=False), status=200, mimetype='application/json')
        except exc.IntegrityError as e:
            return Response(json.dumps({'success':False, 'message':str(e.orig)}, ensure_ascii=False), status=200, mimetype='application/json')
