from user import user_db
from flask import request, Response, session
from flask.views import MethodView
import json, traceback

#login_api
class login_view(MethodView):
    def post(self):
        '''file: ./spec/login_post.yaml'''
        try:
            insert = request.get_json()
            acc = insert['acc']
            pw = insert['password']
            result = user_db.mysql_db.query.filter_by(acc=acc)
            if not result.first():
                return Response(json.dumps({'success':False, 'message':'no user', 'data':{}}))
            if pw == result.first().password:
                session['acc'] = result.first().acc
                session['user_name'] = result.first().name
                # 開啓session有效期
                session.permanent = True
                print(session.accessed)
                return Response(json.dumps({'success':False, 'message':'login success', 'data':{}}))
            else:
                return Response(json.dumps({'success':False, 'message':'error password', 'data':{}}))
        except KeyError:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
        except Exception:
            print('\n' + traceback.format_exc())
            return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')