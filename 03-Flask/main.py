###
### Intergrate with HTML

from flask import Flask, redirect, url_for, render_template, request

app= Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/success/<int:score>')
def success(score):
    res='PASSED'
    return render_template('result.html',result=res,mark=score)

@app.route('/fail/<int:score>')
def fail(score):
    return "The Person has failed and the marks is "+ str(score)

## result checker
@app.route('/resultchecker/<int:score>')
def resultchecker(score):
    result=''
    if score>40:
        result='success'
    else:
        result='fail'

    return redirect(url_for(result,score=score))

## Result checker submit html page
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    total_score=''

    if request.method=='POST':
        science=float(request.form['science'])
        maths=float(request.form['maths'])
        c=float(request.form['c'])       
        datascience=float(request.form['datascience'])
        
        total_score= (science+maths+ c+datascience)/4

        res=''
        if total_score>50:
            res='success'
        else:
             res='fail'

        return redirect(url_for(res,score=total_score))
    

if __name__ =='__main__':
    app.run(debug=True)