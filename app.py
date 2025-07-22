from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

### タスクを表示する　＃＃＃
@app.route('/')
def home():
    # データベースから全てのTodoレコードを取得
    todo_list = Todo.query.all()
    # 取得したTodoリストをindex.htmlテンプレとに渡し、ウェブページをして表示
    return render_template("index.html", todo_list=todo_list)

### タスク追加　＃＃＃
@app.route("/add", methods=["POST"])
def add():
    # ユーザから送信されたフォームデータからタイトルを取得
    title = request.form.get("title")
    # 新しいTodoオブジェクトを作成
    new_todo = Todo(title=title)
    # データベースに新しいTodoを追加
    db.session.add(new_todo)
    # データベースの変更をコミット
    db.session.commit()
    # タスク追加後にホームページにリダイレクト
    return redirect(url_for("home"))

### タスク削除　＃＃＃
@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    #　URLから返されたIDに基づいて、該当するTodoをデータベースから取得
    todo = Todo.query.filter_by(id=todo_id).first()
    # 取得したTodoをデータベースセッションから削除
    db.session.delete(todo)
    # 変更をデータベースにコミット
    db.session.commit()
    # タスク削除後、ホームページにリダイレクト
    return redirect(url_for("home"))

### タスク完了状態切り替え　＃＃＃
@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    # URLから渡されたIDに基づいて、該当するTodoをデータベースから取得
    todo = Todo.query.filter_by(id=todo_id).first()
    # 完了状態を反転
    todo.completed = not todo.completed
    # 変更をデータベースにコミット
    db.session.commit()
    # ホームページにリダイレクト
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)