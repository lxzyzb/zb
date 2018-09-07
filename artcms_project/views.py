#coding:utf8
import os
import datetime
import pymysql
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for,flash, session, Response,request
from forms import LoginForm, RegisterForm, ArtForms, ArtEditForm
from models import User,db, Art
from werkzeug.security import generate_password_hash
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"]= "12345678"
app.config["UP"]=os.path.join(os.path.dirname(__file__),'static/uploads')

def user_login_req(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login',next=request.url))
        return f(*args, **kwargs)
    return login_req

@app.route("/login/",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        flash("登录成功","ok")
        return redirect("/art/list/1/")
    return render_template('login.html',title="登陆", form=form)

@app.route("/register/",methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
        db.session.commit()
        flash(u"注册成功，请登录", "ok")
        return redirect("/login/")
    return render_template("register.html",title="注册",form=form)

@app.route("/logout/",methods = ["GET"])
@user_login_req
def logout():
    session.pop("user",None)
    return redirect("/login/")

def change_name(name):
    info = os.path.splitext(name)
    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex)+info[-1]
    return name

@app.route("/art/add/",methods = ["GET","POST"])
@user_login_req
def art_add():
    form = ArtForms()
    if form.validate_on_submit():
        data = form.data
        file = secure_filename(form.logo.data.filename)
        logo = change_name(file)
        if not os.path.exists(app.config["UP"]):
            os.makedirs(app.config["UP"])
        form.logo.data.save(app.config["UP"] + '/' + logo)
        user = User.query.filter_by(name = session["user"]).first()
        user_id = user.id
        art = Art(
            title = data["title"],
            cate = data["cate"],
            user_id = user_id,
            logo = logo,
            content = data["content"],
            addtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(art)
        db.session.commit()
        flash("发布成功","ok")

    return render_template("art_add.html",title="发布文章",form=form)

@app.route("/art/edit/<int:id>",methods = ["GET","POST"])
@user_login_req
def art_edit(id):
    art = Art.query.get_or_404(int(id))
    form = ArtEditForm()
    if request.method == "GET":
        form.content.data = art.content
        form.cate.data = art.cate
        form.logo.data = art.logo
    if form.validate_on_submit():
        data = form.data
        # 上传logo
        file = secure_filename(form.logo.data.filename)
        logo = change_name(file)
        if not os.path.exists(app.config["UP"]):
            os.makedirs(app.config["UP"])
        # 保存文件
        form.logo.data.save(app.config["UP"] + "/" + logo)
        art.logo = logo
        art.title = data["title"]
        art.content = data["content"]
        art.cate = data["cate"]
        db.session.add(art)
        db.session.commit()
        flash(u"编辑文章成功！", "ok")
    return render_template("art_edit.html",form=form,  title=u"编辑文章", art=art)

@app.route("/art/del/<int:id>",methods = ["GET"])
@user_login_req
def art_del(id):
    art=Art.query.get_or_404(int(id))
    db.session.delete(art)
    db.session.commit()
    flash("删除成功","ok")
    return redirect("/art/list/1")

@app.route("/art/list/<int:page>/",methods=["GET"])
@user_login_req
def art_list(page = None):
    if page is None:
        page =1
    user = User.query.filter_by(name = session["user"]).first()
    page_data = Art.query.filter_by(
        user_id = user.id
    ).order_by(Art.addtime.desc()
               ).paginate(page = 1, per_page=3)
    cate = [(1,u"科技"), (2,u"搞笑"),(3,u"军事")]
    return render_template("art_list.html",title="文章列表",page_data = page_data, cate = cate)

@app.route("/codes/",methods=["GET"])
def codes():
    from codes import Codes
    c = Codes()
    info = c.create_code()
    image = os.path.join(os.path.dirname(__file__),"static/Codes") + "/" + info["img_name"]
    with open(image,'rb') as f:
        image = f.read()
    session["code"] = info["codes"]
    return Response(image,mimetype="jpeg")


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8080)