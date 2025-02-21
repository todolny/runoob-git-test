from flask import Blueprint, request, render_template, g, redirect, url_for
from sqlalchemy import or_

from decorators import login_requried
from exts import db
#用.forms是为了指定在当前目录下进行导入
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel

bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def index():
    # 获取当前页码，默认为 1
    page = request.args.get("page", 1, type=int)
    # 分页，每页 10 条记录
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).paginate(page=page, per_page=10)

    # 确保 questions 是 Pagination 对象
    print(f"当前页: {questions.page}, 总页数: {questions.pages}, 数据量: {len(questions.items)}")

    # questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()# 获取所有问题，并按照创建时间降序排列
    return render_template("index.html", questions=questions)  # 渲染模板，并将问题列表传递给前端

@bp.route("/qa/public", methods=['GET', 'POST'])
@login_requried
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        # 当post请求时，需要使用request.form来获取数据
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            #todo:跳转到这篇问答的详情页面，
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/qa/detail/<qa_id>")
@login_requried
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)

@bp.route("/answer/public", methods=["POST"])
# @bp.post("/answer/public")
@login_requried
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))




@bp.route('/search')
@login_requried
def search():
    #/search?q=flask
    #/search/<q>
    #post, request.form
    q = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    if q:
        questions = QuestionModel.query.filter(
            or_(
                QuestionModel.title.contains(q),
                QuestionModel.content.contains(q)
            )
        ).paginate(page=page, per_page=10) #page=1 这个地方暂时改为1，等之后再看怎么实现分页搜寻的具体代码改法，可以了，是缺少了前置的page参数
    else:
        questions = None
    return render_template("index.html", questions=questions)


