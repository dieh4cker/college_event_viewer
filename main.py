from flask import Flask, render_template,request,flash,redirect,url_for,session,send_file
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
from collections import Counter

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "king-754345"

db = SQLAlchemy(app)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    passwd = db.Column(db.String(50), nullable=False)

class Notice(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(5000), nullable=False)

class Athletic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    judges = db.Column(db.String(500), nullable=False)

class Sports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    judges = db.Column(db.String(500), nullable=False)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    message = db.Column(db.String(500), nullable=False)

class GamesRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    sbrn = db.Column(db.String(50), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)

#client side page 
@app.route("/")
def index():
    data = Notice.query.all()
    return render_template('index.html', notices=data)

@app.route("/athletic")
def athletic():
    eventdata = Athletic.query.all()

    for event in eventdata:
        event.formatted_date = datetime.strptime(
            event.date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        event.formatted_time = datetime.strptime(
            event.time, "%H:%M"
        ).strftime("%I:%M %p")
    return render_template('athletic.html' , events=eventdata)

@app.route("/sports")
def sports():
    eventdata = Sports.query.all()

    for event in eventdata:
        event.formatted_date = datetime.strptime(
            event.date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        event.formatted_time = datetime.strptime(
            event.time, "%H:%M"
        ).strftime("%I:%M %p")
    return render_template('sports.html' , events=eventdata)

@app.route("/examination")
def examination():
    return render_template('examination.html')

@app.route("/event-register" , methods=['GET', 'POST'])
def event_register():
    reg_type = request.args.get("type")

    if reg_type == "athletic":
        eventdata = Athletic.query.all()

    elif reg_type == "sports":
        eventdata = Sports.query.all()

    else:
        eventdata = []
   
    if request.method == 'POST':
        name = request.form.get('full_name')
        branch = request.form.get('branch')
        email = request.form.get('email')
        semester = request.form.get('semester')
        phone_no = request.form.get('phone')
        sbrn = request.form.get('rollno')
        games = request.form.getlist('games')
        games_str = ", ".join(games)
        event_type = request.form.get("event_type")
        registered_data = GamesRegister(name=name , branch = branch , email=email, semester=semester , phone =phone_no , sbrn=sbrn , game=games_str, event_type=event_type)
        db.session.add(registered_data)
        db.session.commit()
        return redirect("/event-register?type=" + event_type)

    return render_template('registration.html' , events=eventdata , reg_type=reg_type)

@app.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        data = Contact(name=name,email=email,message=message)
        db.session.add(data)
        db.session.commit()
        return redirect("/contact")

    return render_template('contact.html')

# admin page backend
@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    if "admin" in session:
        return redirect("/admin")
     
    if request.method == 'POST':
        email = request.form.get('email') 
        passwd = request.form.get('password')

        user = Admin.query.filter_by(email=email, passwd=passwd).first()

        if user:
            session['admin'] = user.name
            return redirect("/admin")
        else:
            return "Invalid Email or Password"

    return render_template("admin-login.html")

@app.route("/admin")
def admin_dashboard():

    if 'admin' not in session:
        return redirect("/admin-login")

    users = GamesRegister.query.all()

    total_users = len(users)
    total_athletic = Athletic.query.count()
    total_sports = Sports.query.count()

    game_list = []
    for u in users:
        for g in u.game.split(","):
            game_list.append(g.strip())

    game_counts = Counter(game_list)

    game_labels = list(game_counts.keys())
    game_values = list(game_counts.values())

    branch_counts = Counter([u.branch for u in users])
    branch_labels = list(branch_counts.keys())
    branch_values = list(branch_counts.values())

    return render_template(
        "admin.html",
        total_users=total_users,
        total_athletic=total_athletic,
        total_sports=total_sports,
        game_labels=game_labels,
        game_values=game_values,
        branch_labels=branch_labels,
        branch_values=branch_values
    )

@app.route("/register-admin", methods=['GET', 'POST'])
def adminregister():
    if 'admin' not in session:
        return redirect("/admin-login")
    if request.method == 'POST':
        name = request.form.get('admin_name') 
        email  = request.form.get('email')
        passwd  = request.form.get('password')
        admin_data=Admin(name=name,email=email,passwd=passwd)
        db.session.add(admin_data)
        db.session.commit()
    return render_template("rigester-admin.html")

@app.route("/logout")
def logout():
    if 'admin' not in session:
        return redirect("/admin-login")
    session.pop('admin', None)
    return redirect("/admin-login")

@app.route("/manage-athletic", methods=['GET', 'POST'])
def add_event():

    if 'admin' not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        if "csv_file" in request.files:

            file = request.files.get("csv_file")

            if file and file.filename.endswith(".csv"):

                csv_file = TextIOWrapper(file, encoding="utf-8")
                reader = csv.DictReader(csv_file)

                for row in reader:
                    new_event = Athletic(
                        eventName=row["eventName"],
                        date=row["date"],
                        time=row["time"],
                        judges=row["judges"]
                    )
                    db.session.add(new_event)

                db.session.commit()
                return redirect("/manage-athletic")

        else:
            name = request.form.get('event_name')
            date = request.form.get('event_date')
            time = request.form.get('event_time')
            judges = request.form.get('judges')

            event_data = Athletic(
                eventName=name,
                date=date,
                time=time,
                judges=judges
            )

            db.session.add(event_data)
            db.session.commit()

            return redirect("/manage-athletic")

    return render_template("athletic-manage.html")

@app.route("/delete-event")
def manage_event():
    if 'admin' not in session:
        return redirect("/admin-login")
    eventdata = Athletic.query.all()

    for event in eventdata:
        event.formatted_date = datetime.strptime(
            event.date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        event.formatted_time = datetime.strptime(
            event.time, "%H:%M"
        ).strftime("%I:%M %p")
    return render_template("delete-event.html", events=eventdata)

@app.route("/delete-event/<int:id>", methods=['GET','POST'])
def delete_event(id):
    if 'admin' not in session:
        return redirect("/admin-login")
    eventdata = Athletic.query.get(id)
    if eventdata:
        db.session.delete(eventdata)
        db.session.commit()
    return redirect("/delete-event")

@app.route("/manage-sports", methods=['GET', 'POST'])
def add_sports_event():

    if 'admin' not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        if "csv_file" in request.files:

            file = request.files.get("csv_file")

            if file and file.filename.endswith(".csv"):

                csv_file = TextIOWrapper(file, encoding="utf-8")
                reader = csv.DictReader(csv_file)

                for row in reader:
                    new_event = Sports(
                        eventName=row["eventName"],
                        date=row["date"],
                        time=row["time"],
                        judges=row["judges"]
                    )
                    db.session.add(new_event)

                db.session.commit()
                return redirect("/manage-sports")

        else:
            name = request.form.get('event_name')
            date = request.form.get('event_date')
            time = request.form.get('event_time')
            judges = request.form.get('judges')

            event_data = Sports(
                eventName=name,
                date=date,
                time=time,
                judges=judges
            )

            db.session.add(event_data)
            db.session.commit()

            return redirect("/manage-sports")

    return render_template("sports-manage.html")

@app.route("/delete-sports-event")
def manage_sports_event():
    if 'admin' not in session:
        return redirect("/admin-login")
    eventdata = Sports.query.all()

    for event in eventdata:
        event.formatted_date = datetime.strptime(
            event.date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        event.formatted_time = datetime.strptime(
            event.time, "%H:%M"
        ).strftime("%I:%M %p")
    return render_template("deleteSportsEvent.html", events=eventdata)

@app.route("/delete-sports-event/<int:id>", methods=['GET','POST'])
def delete_sports_event(id):
    if 'admin' not in session:
        return redirect("/admin-login")
    eventdata = Sports.query.get(id)
    if eventdata:
        db.session.delete(eventdata)
        db.session.commit()
    return redirect("/delete-sports-event")

@app.route("/notice", methods=['GET', 'POST'])
def notice():
    if 'admin' not in session:
        return redirect("/admin-login")
    if request.method == 'POST':
        title = request.form.get('title') 
        desc  = request.form.get('desc')
        notice=Notice(title=title,desc=desc)
        db.session.add(notice)
        db.session.commit()
        flash("Student updated.", "success")
        return redirect(url_for('notice'))
    return render_template("notice.html")

@app.route("/delete-notice")
def manage_notice():
    if 'admin' not in session:
        return redirect("/admin-login")
    notices = Notice.query.all()   
    return render_template("deletenotice.html", notices=notices)

@app.route("/delete-notice/<int:id>", methods=['GET','POST'])
def delete_notice(id):
    if 'admin' not in session:
        return redirect("/admin-login")
    
    notice = Notice.query.get(id)
    if notice:
        db.session.delete(notice)
        db.session.commit()
    return redirect("/delete-notice")

@app.route("/manage-registered")
def manage_registered():
    if 'admin' not in session:
        return redirect("/admin-login")
    
    sports_events = Sports.query.all()
    athletic_events = Athletic.query.all()

    users = GamesRegister.query.all()
    return render_template('registration-manage.html',  users=users , sports=sports_events,
    athletics=athletic_events)

@app.route("/download-filtered-pdf", methods=["POST"])
def download_filtered_pdf():

    payload = request.json

    data = payload["rows"]
    game = payload["game"]

    buffer = io.BytesIO()

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(f"{game} Registration List", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1,20))

    table_data = [["Name","Branch","Semester","Email","Phone","Game"]]

    for row in data:
        table_data.append([
            row["name"],
            row["branch"],
            row["semester"],
            row["email"],
            row["phone"],
            row["game"]
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('GRID',(0,0),(-1,-1),1,colors.grey),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),

        ('BOTTOMPADDING',(0,0),(-1,0),12)

    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    total = Paragraph(f"Total Participants: {len(data)}", styles['Heading3'])
    elements.append(total)

    pdf = SimpleDocTemplate(buffer)

    pdf.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="participants.pdf",
        mimetype="application/pdf"
    )

@app.route("/clear-registrations", methods=["POST"])
def clear_registrations():

    if 'admin' not in session:
        return redirect("/admin-login")

    GamesRegister.query.delete()

    db.session.commit()

    return redirect("/manage-registered")

@app.route("/manage-contact")
def maanage_contact():
    if 'admin' not in session:
        return redirect("/admin-login")
    
    data=Contact.query.all()
    return render_template('manage-contact.html',contactdata=data)

@app.route("/delete-contact/<int:id>", methods=['GET','POST'])
def delete_contact(id):
    if 'admin' not in session:
        return redirect("/admin-login")
    
    data = Contact.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect("/manage-contact")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)