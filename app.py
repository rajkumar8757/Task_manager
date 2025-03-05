from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///works.db'
db = SQLAlchemy(app)

# Database Model
class Works(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Home Route
@app.route('/')
def home():
    work_items = Works.query.all()
    return render_template('index.html', work_items=work_items)

# Add Work
@app.route('/add', methods=['POST'])
def add_work():
    description = request.form.get('description')
    if description:
        new_work = Works(description=description, done=False)  # Ensure 'done' is initialized
        db.session.add(new_work)
        db.session.commit()
    return redirect(url_for('home'))

# Mark Work as Completed
@app.route('/complete/<int:item_id>')
def complete(item_id):
    work_item = Works.query.get(item_id)
    if work_item:
        work_item.done = not work_item.done  # Toggle the status
        db.session.commit()
    return redirect(url_for('home'))

# Delete Work
@app.route('/delete/<int:item_id>')
def remove_work(item_id):
    work_item = Works.query.get(item_id)
    if work_item:
        db.session.delete(work_item)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
