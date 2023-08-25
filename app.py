from flask import Flask

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def inex():
    return "This is demo for the machine learning Project"

if __name__=='__main__':
    app.run(debug=True)
