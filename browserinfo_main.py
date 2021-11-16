from flask import Flask, request, render_template, redirect, url_for
import requests, re, uuid, json, jinja2, os

app = Flask(__name__)

# generate unique id for visitor // sets up visit_id for storing user date
def generateID(): 
    id = str(uuid.uuid4().hex)
    global visit_id
    visit_id = id
    return id

# dictionary for user data + update_file function 
user_data_list = {}
if os.path.exists("/Users/werickson/Documents/code-camp/code/dub-2021/werickson/browserinfo/users_data.json"):
    with open("/Users/werickson/Documents/code-camp/code/dub-2021/werickson/browserinfo/users_data.json", "r") as file:
        user_data_list = json.load(file)

else:
    print("file not found") # but whyyyyyyy

def update_file():
    with open("/Users/werickson/Documents/code-camp/code/dub-2021/werickson/browserinfo/users_data.json", "w") as file:
        file.write(json.dumps(user_data_list))
        print("file updated")

# homepage route
@app.route('/')
def homepage():
    return render_template('index.html')
    
@app.route('/copy_test_page')
def copy_test():
    return "This was a test page!"

@app.route('/demo') # adds a new test entry and displays all
def user_test():
    generateID()
    add_user_data("test","test","test","test","test")
    all_users_data = get_all_user_data()
    return str(all_users_data)

@app.route('/test') # generates a vistor ID and redirects to the results page with ID
def get_id():
    id = generateID()
    return redirect(url_for('get_results', user_id=id))

@app.route('/test/<user_id>') # creates page with the ID in the URL and displays request info
def get_results(user_id): 

    # if ID is already stored in user data list, load data from user data list
    for data in user_data_list:
        if user_id == data:
            bro = user_data_list[user_id]["browser"]
            ver = user_data_list[user_id]["version"]
            pla = user_data_list[user_id]["platform"]
            uas = user_data_list[user_id]["uas"]
            uip = user_data_list[user_id]["user_ip"]

            return render_template('returning_visitor.html', user_id=user_id, browser=bro, version=ver, platform=pla, uas=uas, user_ip=uip)

    # if ID is not stored, store user data
    bro = request.user_agent.browser.capitalize()
    ver = request.user_agent.version and int(request.user_agent.version.split('.')[0]) # removes full version number
    pla = request.user_agent.platform
    if pla == "macos":
        pla = "Mac OS"
    elif pla == "windows":
        pla = "Windows"
    uas = re.search("Mac ([a-z,A-Z,\s,0-9,_]*)", request.user_agent.string).group()
    if len(uas) < 1:
        uas = re.search("Windows [a-z,A-Z]* [0-9]*.[0-9]*", request.user_agent.string).group()
    uip = request.remote_addr

    add_user_data(bro, ver, pla, uas, uip)

    return render_template('new_visitor.html', user_id=user_id, browser=bro, version=ver, platform=pla, uas=uas, user_ip=uip)

@app.route("/user_result_data", methods = ['GET', 'POST'])
def user_result_data():

    if request.method == 'GET':
        return json.dumps(user_data_list)

    if request.method == 'POST':
        print("post")
        global visit_id
        user_data_list[visit_id] = request.json
        new_data = {"data": user_data_list[visit_id]}
        update_file()
        return json.dumps(new_data)

def get_all_user_data():

    response = requests.get("http://127.0.0.1:5000/user_result_data")
    return json.loads(response.content)

def add_user_data(bro,ver,pla,uas,uip):

    response = requests.post(
        url="http://127.0.0.1:5000/user_result_data",
        json={"browser": bro, "version": ver, "platform": pla, "uas": uas, "user_ip": uip},
        headers={"Content-Type": "application/json"}
    )
    print("user added")

# if __name__ == "__main__":
#     app.run(debug=True)