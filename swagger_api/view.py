from flask import request, Response
import json, traceback
from flask.views import MethodView

datas = [{'name':'juns', 'id':'1'}]
# API
class swagger_view(MethodView):
    def get(self):
        '''file: ./spec/swagger_list.yaml'''
        result = {}
        id = request.args.get('id')
        if not id :
          return {'success':False, 'message':'未輸入欄位:id', 'data':{}}
        for data in datas:
          if data['id'] == str(id):
              result['id'] = data['id']
              result['name'] = data['name']
              break
        return Response(json.dumps({'success':True, 'message':'', 'data': result}, ensure_ascii=False))
    def post(self):
      pass