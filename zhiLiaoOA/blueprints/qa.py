from flask import Blueprint, request, render_template, g, redirect, url_for, current_app
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required

bp = Blueprint('qa', __name__,url_prefix='/')

@bp.route('/')
def index():
    questions=QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()#.desc() 是一个方法，表示按照降序排列。这意味着查询结果将按照 create_time 字段从最新到最旧的顺序排列。
    return render_template("index.html",questions=questions)

#问题发布的页面
@bp.route("/qa/public",methods=['GET','POST'])
@login_required
def public_question():
    if request.method=="GET":
        return render_template("public_question.html")
    else:#如果是发布问题
        form=QuestionForm(request.form)
        if form.validate():#先验证是否合格
            title=form.title.data
            content=form.content.data
            #合格了就加入到数据库
            question=QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

#问题详情页面
@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question=QuestionModel.query.get(qa_id)
    return render_template('detail.html',question=question)

#添加回答
@bp.route('/answer/public',methods=['POST'])
@login_required
def public_answer():
    #当post请求时，需要使用request.form来获取数据
    form=AnswerForm(request.form)#接受回答者的表单
    if form.validate():#验证表单是否合格
        content=form.content.data
        question_id=form.question_id.data
        #加入到数据库
        answer=AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question.id")))

#搜索界面
@bp.route('/search')
def search():
    #三种传参方式
    #/search?q=flask
    #/search/<q>
    #post,request.form
    q=request.args.get("q")
    #在数据库中寻找包含的
    questions=QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    #找到后把结果渲染到模板中
    return render_template("index.html",questions=questions)


