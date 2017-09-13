from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'mydb')

app.secret_key = 'KeepItSecretKeepItSafe'

@app.route('/')
def index():
    query = "SELECT * FROM emails"                           # define your query
    emails = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_emails=emails)

@app.route('/validate', methods=['POST'])
def validate():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "SELECT * FROM  emails WHERE email = :email"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'email': request.form['email']
           }
    # Run query, with dictionary values injected into the query.
    result = mysql.query_db(query, data)
    print "result:" , result
    if len(result)==0:
        print "ok to enter"
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        mysql.query_db(query, data)
        return redirect('/success/')
    else:
        flash ('Email not valid, already in the database')
    return redirect('/')


@app.route('/success/')
def success():
    query = "SELECT * FROM emails"                          
    emails = mysql.query_db(query)       
    return render_template('success.html', all_emails=emails)


app.run(debug=True)