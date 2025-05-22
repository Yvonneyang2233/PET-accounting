from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 設定資料庫
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料表定義
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    expenses = Expense.query.all()
    total = sum(exp.amount for exp in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    note = request.form['note']

    new_expense = Expense(date=date, category=category, amount=amount, note=note)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    search_date = request.form['search_date']
    filtered = Expense.query.filter_by(date=search_date).all()
    total = sum(exp.amount for exp in filtered)
    return render_template('search.html', expenses=filtered, total=total, date=search_date)

# Delete expense
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

# Edit expense - show form
@app.route('/edit/<int:expense_id>', methods=['GET'])
def edit(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return render_template('edit.html', expense=expense)

# Edit expense - submit update
@app.route('/update/<int:expense_id>', methods=['POST'])
def update(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    expense.date = request.form['date']
    expense.category = request.form['category']
    expense.amount = float(request.form['amount'])
    expense.note = request.form['note']
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
