from flask import Flask, render_template, url_for, request, redirect
import connexion
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return "<Memo %r>" % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        memo_content = request.form['content']
        new_memo = Memo(content=memo_content)

        try:
            db.session.add(new_memo)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your memo"
    else:
        memos = Memo.query.order_by(Memo.date_created).all()
        return render_template('index.html', memos=memos)

@app.route('/delete/<int:id>')
def delete(id) :
    memo_to_delete=Memo.query.get_or_404(id)

    try:
        db.session.delete(memo_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting that memo"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id) :
    memo = Memo.query.get_or_404(id)
    if request.method == 'POST':
        memo.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating that memo"
    else:

        return render_template('update.html', memo=memo)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
