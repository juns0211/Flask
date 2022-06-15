from flask import request, Response, Blueprint
from . import sql_db
import json
import traceback

test_api_app = Blueprint('test_api_app', __name__)

#開API
@test_api_app.route("/test", methods=['GET', 'POST'])
def test():
    try:
        if request.method == 'POST':
            insert = request.get_json()
            user = insert['name']
            if insert.get('id'):
                id = insert['id']
                obj = sql_db.mysql_db(**{'id':id, 'name':user})
            else:
                obj = sql_db.mysql_db(**{'name':user})
            sql_db.db.session.add(obj)
            sql_db.db.session.commit()
            result = sql_db.mysql_db.query.filter_by(name=user).first()
            return Response(json.dumps({'success':True, 'message':'', 'data':{'id':result.id, 'name':result.name}}, ensure_ascii=False), status=200, mimetype='application/json')
        else:
            id = request.args['id']
            # result = sql_db.db.session.query(sql_db.mysql_db).filter_by(id=id).first()
            result = sql_db.mysql_db.query.filter_by(id=id).first()
            if not result:
                return Response(json.dumps({'success':True, 'message':'', 'data':{}}, ensure_ascii=False), status=200, mimetype='application/json')
            return Response(json.dumps({'success':True, 'message':'', 'data':{'id':result.id, 'name':result.name, }}, ensure_ascii=False), status=200, mimetype='application/json')
    except KeyError:
        print('\n' + traceback.format_exc())
        return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
    except Exception:
        print('\n' + traceback.format_exc())
        return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')

#開post_API
# @app.route("/test", methods=['GET'])
# def test_get():
#     try:
#         id = request.args['id']
#        # result = sql_db.db.session.query(sql_db.mysql_db).filter_by(id=id).first()
#         result = sql_db.mysql_db.query.filter_by(id=id).first()
#         if not result:
#             return Response(json.dumps({'success':True, 'message':'', 'data':{}}, ensure_ascii=False), status=200, mimetype='application/json')
#         return Response(json.dumps({'success':True, 'message':'', 'data':{'id':id, 'name':result.name, }}, ensure_ascii=False), status=200, mimetype='application/json')
#     except KeyError:
#         print('\n' + traceback.format_exc())
#         return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
#     except Exception:
#         print('\n' + traceback.format_exc())
#         return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')