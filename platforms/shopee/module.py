import requests

def get_all_session():
    url = 'https://shopee.tw/api/v4/flash_sale/get_all_sessions'
    params = {'category_personalization_type':0}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return {'success':False, 'message':f'取得活動時間與ID失敗, status_code={resp.status_code}', 'data':''}
    return {'success':True, 'message':'', 'data':resp.json()['data']['sessions']}