from flask import Flask, request, render_template, redirect, flash, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evenements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"

db = SQLAlchemy(app)

class Evenements(db.Model) :
    __tablename__ = 'evenements'
    
    id = db.Column(db.Integer, primary_key = True) 
    titre = db.Column(db.Text, nullable = False) 
    type_evenement = db.Column(db.Text, nullable = False)
    date = db.Column(db.Date, nullable = False)   
    lieu = db.Column(db.Text, nullable = False) 
    description = db.Column(db.Text, nullable = False)
    
    def __repr__(self):
        return f"evenements('{self.titre}', '{self.type_evenement}', '{self.date}', '{self.lieu}', '{self.description}')"
    


with app.app_context():
    db.create_all()
    

@app.route ("/") 
def accueil():
    titrePage = "IntraEvent - Accueil"
    evenements = Evenements.query.all()
    
    return render_template("index.html", evenements = evenements, titrePage = titrePage)
    
    

@app.route("/ajouter", methods = ["GET", "POST"])
def ajouter_evenement():
    
    titrePage = "IntraEvent - Ajout événement"
    
    if request.method == "POST" :
        
        titre = request.form.get("titre").strip()
        type_evenement = request.form.get("type").strip()
        date = request.form.get("date")
        date_obj = datetime.strptime(date, "%Y-%m-%d").date() 
        lieu = request.form.get("lieu").strip()
        description = request.form.get("description").strip()
        
        if not titre or not type_evenement or not date or not lieu or not description:
            flash("Tous les champs doivent être remplie.", "danger")
            return redirect(url_for("ajouter_evenement"))
    
        
        date_actuelle = datetime.today().date()
        if date_obj < date_actuelle :
            flash ("Date invalide car inférieur à date actuelle", "danger")
            return redirect(url_for("ajouter_evenement"))
        
    
        entry = Evenements (
            titre = titre,
            type_evenement = type_evenement,
            date = date_obj,
            lieu = lieu,
            description = description
        )
        
        db.session.add(entry)
        db.session.commit()

        flash("Événement enregistré avec succès.", "success")
        return redirect(url_for("ajouter_evenement"))
        
    
    return render_template("ajouter.html", titrePage = titrePage)


@app.route("/evenements/<int:evenement_id>/supprimer") 
def supprimer_evenement(evenement_id):
    
    entry = Evenements.query.get(evenement_id)
    
    if not entry :
        flash("L'événement n'existe pas", "danger")
        return redirect(url_for("accueil"))
    
    db.session.delete(entry) 
    db.session.commit()    
    
    flash("Entrée d'historique supprimée avec succès.", "success")
    return redirect(url_for("accueil"))


@app.route("/api/evenements", methods=["GET"])
def list_evenements():
    
    date_actuelle = datetime.today().date()
    
    evenements = (Evenements.query
                .filter(Evenements.date >= date_actuelle)
                .order_by(Evenements.date.asc())
                .limit(5)
                .all())
    
    list_evenement = []
    
    for evenement in evenements :
        
        list_evenement.append({
            "titre": evenement.titre,
            "type_evenement": evenement.type_evenement,
            "date": evenement.date.strftime("%Y-%m-%d"),
            "lieu": evenement.lieu,
            "description": evenement.description
        })

    return jsonify({
        "evenements" : list_evenement
    })

if __name__ == "__main__":
    app.run(debug=True)