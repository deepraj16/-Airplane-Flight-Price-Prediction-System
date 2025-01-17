from flask import Flask ,render_template,flash,url_for
from forms import InputForm
import pandas as pd
import joblib 
import numpy

app =Flask(__name__) 

app.config["SECRET_KEY"]="love_to"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title="home")



model =joblib.load("model.joblib")

#m predict
@app.route("/predict",methods=["GET","POST"])
def predict(): 
    form =InputForm()
    if form.validate_on_submit():
        x_new =pd.DataFrame(dict(
            airline=[form.airline.data],
            date_of_journey=[form.date_of_journey.data.strftime("%Y-%m-%d")],
            source=[form.source.data],
            destination=[form.destination.data],
            dep_time=[form.dep_time.data.strftime("%H:%M:%S")],
            arrival_time=[form.arrival_time.data.strftime("%H:%M:%S")],
            duration=[form.duration.data],
            total_stops=[form.total_stops.data],
            additional_info=[form.additional_info.data]
        )) 
        prediction =model.predict(x_new)[0]
        prediction-=1000
        message =f"The prediction value is {prediction} INR"
    else:
        message="please provid valid input details!!"
    return render_template("predict.html",tilte="prdict",form=form,output=message)

@app.route("/about")
def about():
    return render_template("about.html",title="about")

if __name__ =="__main__":
    app.run(debug=True)