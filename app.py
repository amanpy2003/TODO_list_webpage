from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://amanpy21:amanpy21@localhost/todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Define routes
@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        new_row = Todo(title=title, desc=desc)
        db.session.add(new_row)
        db.session.commit()
        return redirect('/')  # Redirect to refresh the page after adding a new todo
    
    allTodo = Todo.query.all()  # Get all todos from the database
    return render_template('home.html', allTodo=allTodo)  # Pass them to the template

@app.route('/edit/<int:sno>', methods=['GET', 'POST'])
def edit(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        date_created = datetime.now()
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.date_created = date_created
        db.session.add(todo)
        db.session.commit()
        return redirect('/')  # Redirect to refresh the page after editing a todo

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)  # Pass the todo to the template


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')  # Redirect to the home page after deletion

if __name__ == '__main__':
    # Create database and tables
    with app.app_context():
        db.create_all()  # Ensure that the tables are created if they don't exist
    app.run(debug=True, port=8000)
