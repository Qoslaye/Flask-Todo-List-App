from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        todo_title = request.form['title']
        desc_todo = request.form['desc']
        data = Todo(title=todo_title, desc=desc_todo)
        db.session.add(data)
        db.session.commit()
        # Redirect to avoid duplicate submissions on refresh
        return redirect(url_for('hello_world'))
    
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.run(debug=False)
