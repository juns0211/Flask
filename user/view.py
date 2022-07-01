from flask import request, Response, session, abort
from flask.views import MethodView
from . import user_db
import json, traceback
from flasgger import swag_from
from configs.config import validation_error_handler, validation_function


#API
class user_view(MethodView):
    @swag_from('spec/test_get.yaml')
    def get(self):
        try:
            data = {}
            acc = request.args['acc']
            # result = sql_db.db.session.query(sql_db.mysql_db).filter_by(id=id).first()
            resp = user_db.mysql_db.query.filter_by(acc=acc).first()
            if resp:
                data['acc'] = resp.acc
                data['name'] = resp.name
            return Response(json.dumps({'success':True, 'message':'', 'data':data}, ensure_ascii=False), status=200, mimetype='application/json')
        except KeyError:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
        except Exception:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')

    @swag_from('spec/test_post.yaml', validation=True, validation_function=validation_function, validation_error_handler=validation_error_handler)
    def post(self):
        insert = request.get_json()
        name = insert['name']
        acc = insert['acc']
        pw = insert['password']
        obj = user_db.mysql_db(**{'name':name, 'acc':acc, 'password':pw})
        user_db.db.session.add(obj)
        user_db.db.session.commit()
        result = user_db.mysql_db.query.filter_by(acc=acc).first()
        return Response(json.dumps({'success':True, 'message':'', 'data':{'name':result.name, 'acc':result.acc}}, ensure_ascii=False), status=200, mimetype='application/json')
        
    @swag_from('spec/test_put.yaml', validation=True, validation_function=validation_function, validation_error_handler=validation_error_handler) 
    def put(self):
        insert = request.get_json()
        name = insert['name']
        acc = insert['acc']
        pw = user_db.mysql_db()
        pw.password = insert['password']
        result = user_db.mysql_db.query.filter_by(acc=acc)
        if not result.first():
            return Response(json.dumps({'success':True, 'message':'查無此會員', 'data':{}}, ensure_ascii=False), status=200, mimetype='application/json')
        result.update(dict(name=name, acc=acc, password_hash=pw.password_hash))
        user_db.db.session.commit()
        return Response(json.dumps({'success':True, 'message':'', 'data':{'name':name, 'acc':acc, 'password':insert['password']}}, ensure_ascii=False), status=200, mimetype='application/json')

    @swag_from('spec/test_delete.yaml', validation=True, validation_function=validation_function, validation_error_handler=validation_error_handler) 
    def delete(self):
        result = []
        insert = request.get_json()
        accs = insert['acc']
        for acc in accs:
            resp = user_db.mysql_db.query.filter_by(acc=acc)
            if not resp.first():
                continue
            result.append({'id':resp.first().acc, 'name':resp.first().name})
            resp.delete()
        user_db.db.session.commit()
        return Response(json.dumps({'success':True, 'message':'刪除成功', 'data':result}, ensure_ascii=False), status=200, mimetype='application/json')