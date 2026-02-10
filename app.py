from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evenements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HistoryEntry(db.Model) :
    __tablename__ = 'evenements'
    
    id = db.Column(db.Integer, primary_key = True) 
    titre = db.Column(db.Text, nullable = False) 
    type = db.Column(db.Text, nullable = False)
    date = db.Column(db.Date, nullable = False)   
    lieu = db.Column(db.Text, nullable = False) 
    description = db.Column(db.Text, nullable = False)
    
    def __repr__(self):
        return f"evenements('{self.titre}', '{self.type}', '{self.date}', '{self.lieu}', '{self.description}')"

with app.app_context():
    db.create_all()
    

@app.route ("/accueil") 
def accueil():
    evenements = HistoryEntry.query.all()
    return render_template("index.html", evenements = evenements)
    
    

@app.route("/ajouter", methods = ["GET", "POST"])
def formulaire():
    
    titre = ""
    type = ""
    date = ""
    lieu = ""
    description = ""
    
    if request.method == "POST" :
        
        titre = request.form.get("titre")
        type = request.form.get("type")
        date = request.form.get("date")
        date_obj = datetime.strptime(date, "%Y-%m-%d").date() 
        lieu = request.form.get("lieu")
        description = request.form.get("description")
        
    
        entry = HistoryEntry (
            titre = titre,
            type = type,
            date = date_obj,
            lieu = lieu,
            description = description
        )
        
        db.session.add(entry)
        db.session.commit()

        flash("Événement enregistré avec succès.", "success")
        return redirect(url_for("formulaire"))
        
    
    return render_template("ajouter.html")


@app.route("/evenements/<int:evenement_id>/supprimer") 
def delete_history(evenement_id):
    
    entry = HistoryEntry.query.get(evenement_id)
    
    db.session.delete(entry) 
    db.session.commit()    
    
    flash("Entrée d'historique supprimée avec succès.", "success")
    return redirect(url_for("accueil"))
    
if __name__ == "__main__":
    app.run(debug=True)