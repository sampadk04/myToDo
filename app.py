from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databases/ToDo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Defining the Schema: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
class ToDo(db.Model):
    todo_id = db.Column(db.Integer, primary_key=True)
    todo_title = db.Column(db.String(40), nullable=False)
    todo_desc = db.Column(db.String(120))
    todo_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id}: {self.title}"


@app.route("/", methods=["GET", "POST"])
def home():
    # extracting the form inputs 'via' POST methods
    # the 'input' variable names in todo_home.html are 'title' and 'desc'
    if request.method == "POST":
        input_title = request.form["title"]
        input_desc = request.form["desc"]
        # creating a todo instance, everytime we add some input into the form
        todo = ToDo(todo_title=input_title, todo_desc=input_desc)
        db.session.add(todo)
        db.session.commit()
    # querying the todo instance into a list
    todo_list = ToDo.query.all()
    # passing the list into the jinja template
    return render_template("todo_home.html", todo_list=todo_list)


@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    # This brings in the updated titles and desc from the 'update/id.html' page and updates it in the database corresponding to the 'todo_id' id value.
    if request.method == "POST":
        updated_title = request.form["title"]
        updated_desc = request.form["desc"]
        # updating the data with id = todo_id, with the updated values in the database
        updated_todo = ToDo.query.filter_by(todo_id=todo_id).first()
        updated_todo.todo_title = updated_title
        updated_todo.todo_desc = updated_desc
        db.session.add(updated_todo)
        db.session.commit()
        # redirecting to the home page
        return redirect("/")

    # This takes in the 'id' to be updated from the home page to redirect to the 'update/id.html' page and show the existing content.
    update_todo = ToDo.query.filter_by(todo_id=todo_id).first()
    return render_template("todo_update.html", update_todo=update_todo)


@app.route("/delete/<int:todo_id>", methods=["GET", "POST"])
def delete(todo_id):
    # Selects the 'id' to be deleted from the database
    delete_todo = ToDo.query.filter_by(todo_id=todo_id).first()
    # Deletes the item from the database
    db.session.delete(delete_todo)
    db.session.commit()
    # Redirects to the home page.
    return redirect("/")


@app.route("/about")
def about():
    return render_template("todo_about.html")


if __name__ == "__main__":
    app.run(debug=False)
