from flask import Flask, render_template, request
import json, requests, uuid, os

app = Flask(__name__)

# Default user data in the list
user_data_list = {}
if os.path.exists("werickson/browserinfo/users_data.json"):
    with open("werickson/browserinfo/users_data.json", "r") as file:
        user_data_list = json.load(file)
        print("file found")
        print(user_data_list)
else:
    print("file not found")

def update_file():
    with open("werickson/browserinfo/users_data.json", "w") as file:
        file.dump(json.dumps(user_data_list))
        print("file updated")

# generate unique id for visitor
def generateID(): 
    id = str(uuid.uuid4().hex)
    global visit_id
    visit_id = id
    return id

@app.route("/user_result_data", methods = ['GET', 'POST'])
def user_result_data():
    if request.method == 'GET':
        return json.dumps(user_data_list)

    if request.method == 'POST':
        print("posting user data")
        global visit_id
        user_data_list[visit_id] = request.json
        result = {"data": user_data_list[visit_id]}
        print("post")
        update_file()
        return json.dumps(result)

def get_all_user_data():

    response = requests.get("http://127.0.0.1:5000/user_result_data")
    return json.loads(response.content)

def add_user_data(bro,ver,pla,uas,uip):

    response = requests.post(
        url="http://127.0.0.1:5000/user_result_data",
        json={"browser": bro, "version": ver, "platform": pla, "uas": uas, "user_ip": uip},
        headers={"Content-Type": "application/json"}
    )

play_now = True

if __name__ == "__main__":
    while play_now:

        generateID()

        print("visit id: "+visit_id)

        add_user_data("test","test","test","test","test")
        
        user_data_list = get_all_user_data() # updates user_data_list with new user data

        for uid in user_data_list:
            print(uid)
            for data in user_data_list[uid]:
                print("> "+data+" : "+user_data_list[uid][data])

        play_now = False