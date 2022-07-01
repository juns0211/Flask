from importlib_metadata import method_cache
from user import user_db
from flask import render_template, request, Response, url_for, redirect, flash
from flask.views import MethodView
import json, traceback
from flask_login import login_required, login_user, logout_user
from setting import app
from .forms import LoginForm


#login_api
# class login_view(MethodView):
    # def post(self):
    #     '''file: ./spec/login_post.yaml'''
    #     try:
    #         insert = request.get_json()
    #         acc = insert['acc']
    #         pw = insert['password']
    #         result = user_db.mysql_db.query.filter_by(acc=acc).first()
    #         if not result:
    #             return Response(json.dumps({'success':False, 'message':'no user', 'data':{}}))
    #         if result.verify_password(pw):
    #             result.id = acc
    #             login_user(result)
    #             return Response(json.dumps({'success':False, 'message':'login success', 'data':{}}))
    #         else:
    #             return Response(json.dumps({'success':False, 'message':'error password', 'data':{}}))
    #     except KeyError:
    #         print('\n' + traceback.format_exc())
    #         return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
    #     except Exception:
    #         print('\n' + traceback.format_exc())
    #         return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')

@app.route('/login', methods=['GET','POST'])
def login_api():
    try:
        form = LoginForm()
        if not form.validate_on_submit():
            return render_template('login.html', form=form)
        result = user_db.mysql_db.query.filter_by(acc=form.acc.data).first()
        if not result:
            flash('Invalid username or password')
            return render_template('login.html', form=form)
            #return Response(json.dumps({'success':False, 'message':'no user', 'data':{}}))
        if result.verify_password(form.password.data):
            result.id = form.acc.data
            login_user(result, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
            #return Response(json.dumps({'success':False, 'message':'login success', 'data':{}}))
        else:
            flash('Invalid username or password')
            return render_template('login.html', form=form)
            #return Response(json.dumps({'success':False, 'message':'error password', 'data':{}}))
    except Exception as e:
        print('\n' + traceback.format_exc())
        flash(e)
        return render_template('login.html', form=form)
        #return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login.html'))