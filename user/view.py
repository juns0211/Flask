from flask import request, Response, session
from flask.views import MethodView
from . import user_db
import json, traceback


#API
class user_view(MethodView):
    def get(self):
        '''file: ./spec/test_get.yaml'''
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

    def post(self):
        '''file: ./spec/test_post.yaml'''
        try:
            insert = request.get_json()
            name = insert['name']
            acc = insert['acc']
            password = insert['password']
            obj = user_db.mysql_db(**{'name':name, 'acc':acc, 'password':password})
            user_db.db.session.add(obj)
            user_db.db.session.commit()
            result = user_db.mysql_db.query.filter_by(acc=acc).first()
            return Response(json.dumps({'success':True, 'message':'', 'data':{'name':result.name, 'acc':result.acc, 'password':result.password}}, ensure_ascii=False), status=200, mimetype='application/json')
        except KeyError:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
        except Exception:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
            
    def put(self):
        '''file: ./spec/test_put.yaml'''
        try:
            insert = request.get_json()
            name = insert['name']
            acc = insert['acc']
            password = insert['password']
            result = user_db.mysql_db.query.filter_by(acc=acc)
            if not result.first():
                return Response(json.dumps({'success':True, 'message':'查無此會員', 'data':{}}, ensure_ascii=False), status=200, mimetype='application/json')
            result.update(dict(name=name, acc=acc, password=password))
            user_db.db.session.commit()
            return Response(json.dumps({'success':True, 'message':'', 'data':{'name':name, 'acc':acc, 'password':password}}, ensure_ascii=False), status=200, mimetype='application/json')
        except KeyError:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
        except Exception:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
        
    def delete(self):
        '''file: ./spec/test_delete.yaml'''
        try:
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
        except KeyError:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':[]}, ensure_ascii=False),status=401, mimetype='application/json')
        except Exception:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':[]}, ensure_ascii=False),status=401, mimetype='application/json')