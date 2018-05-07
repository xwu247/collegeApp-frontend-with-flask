from flask import Flask, render_template, redirect, request, url_for, session
from flask_session import Session
import requests
import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
import ast

application = Flask(__name__)
sess = Session()
application.secret_key=='secretX R~XHH!jmN]LWX/?RT'
application.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(application)

boto3.setup_default_session(region_name='us-east-1')
cognito_identity = boto3.client('cognito-idp')
print "created cognito identity"


service = 'execute-api'
region = 'us-east-1'
accessKey='AKIAIO7PHZTGAOSQMGYA'
secretKey='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'


@application.route('/')
def index():
    return render_template("index.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/ranking")
def ranking():
    return render_template("ranking.html")

@application.route("/recommend")
def recommend():
    if 'registered_username' in session:
        user_n = session['registered_username']
    elif 'logged_username' in session:
        user_n = session['logged_username']
    user_n = str(user_n)
    print(user_n)
    body2 = {
    "UserId":user_n
    }    
    api_url_recommend = 'https://z2iaedljoi.execute-api.us-east-1.amazonaws.com/demo2/recommendation'
    r2 = requests.post(api_url_recommend, data=json.dumps(body2))
    print('recommending schools!')
    result = r2.text
    result = ast.literal_eval(result)
    print(result)
    return render_template("recommend.html",result=result)

@application.route("/school_info_columbia")
def school_info_columbia():
    return render_template("school_info_columbia.html")

@application.route("/school_info_madison")
def school_info_madison():
    return render_template("school_info_madison.html")

@application.route("/single_post")
def single_post():
    return render_template("single-post.html")

@application.route("/survey")
def survey():
    return render_template("survey.html")

@application.route("/login_info", methods=["POST"])
def login_info():
    print request.form
    print "works 0"
    cognito_identity = boto3.client('cognito-idp')
    r2 = cognito_identity.admin_initiate_auth(
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
        "USERNAME": request.form['username'],
        "PASSWORD": request.form['password'],
        },
        ClientId='957hjs6nr0nfcva5af73f0lcs',
        UserPoolId='us-east-1_qDxVSNMZz'
        )
    print(r2)
    if r2['ResponseMetadata']['HTTPStatusCode'] == 200:
        session['logged_username'] = request.form['username']
        print "Successfully logged in!"
        return redirect(url_for('recommend'))
        return json.dumps({'status':'success'})
    return('abc')
    #return redirect(url_for('recommand'))
    #return json.dumps({'status':'success'})


@application.route("/register_info", methods=["POST"])
def register_info():
    print request.form
    #error = None
    cognito_identity = boto3.client('cognito-idp')
    r = cognito_identity.sign_up(
        ClientId = '957hjs6nr0nfcva5af73f0lcs',
        Username=request.form['email'],
        Password=request.form['password'],
        UserAttributes=[{
        'Name':'email',
        'Value':request.form['email']
        }]
        )
    print(r['UserConfirmed'])
    if r['UserConfirmed']==True:
        print "Successfully signed up!"
        session['registered_username'] = request.form['email']
        return redirect(url_for('survey'))
        return json.dumps({'status':'success'})
    return('bcd')
    ##UsernameExistsException:
        #print('Error - User already exist!')
    #except InvalidPasswordException:
        #print('Password did not conform with policy: Password must be at leat 8 characters with Uppercase, lowercase and symbol')

@application.route("/survey_info", methods=["POST"])
def survey_info():
    print request.form
    if 'registered_username' in session:
        user_n = session['registered_username']
    elif 'logged_username' in session:
        user_n = session['logged_username']

    body = {
    "UserId":user_n,
    "Cost":request.form['cost'],
    "GPA":request.form['gpa'],
    "GRE":request.form['gre'],
    "State":request.form['state'],
    "Weather":request.form['weather'],
    "Writing":request.form['writing'],
    "Rank":request.form['rank'],
    }
    print(body)
    api_url_survey = 'https://z2iaedljoi.execute-api.us-east-1.amazonaws.com/demo2/survey'
    #auth = AWS4Auth(accessKey, secretKey, region, service, session_token=access_token)
    r = requests.post(api_url_survey, data=json.dumps(body))#,auth = auth)
    print(r.text)
    return redirect(url_for('survey'))
    return json.dumps({'status':'success'})
    #username = request.form["username"]
    #return "adads"

@application.route("/recommend_info", methods=["POST"])
def recommend_info():
    """
    user_n = session['logged_username']
    if 'registered_username' in session:
        user_n = session['registered_username']
    elif 'logged_username' in session:
        user_n = session['logged_username']
    user_n = str(user_n)
    print(user_n)
    body2 = {
    "UserId":user_n
    }    
    api_url_recommend = 'https://z2iaedljoi.execute-api.us-east-1.amazonaws.com/demo2/recommendation'
    r2 = requests.post(api_url_recommend, data=json.dumps(body2))
    print('recommending schools!')
    result = json.loads(r2.text)
    print(result)
    """
    #return render_template('recommand.html',name="Joe")
    return ('aabb')
    
    """
    print request.form
    username = request.form["username"]
    data = {"Userid":username}
    json_resp = requests.get("https://r4ds4cfk2j.execute-api.us-east-1.amazonaws.com/test/recommandation", params=data).content
    data_map = json.loads(json_resp)
    return json.dumps({"school":data_map["events"]["school"]})
    """

if __name__ == '__main__':
    
    application.debug=True
    application.run()#(host="localhost", port=8088, debug=True)
    #print "start to run server on http://localhost:8088"
