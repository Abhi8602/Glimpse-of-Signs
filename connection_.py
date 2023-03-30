from pymongo import MongoClient
import datetime,random,matplotlib.pyplot as plt


client = MongoClient("mongodb+srv://tp8602:why12345@cluster0.sxfyske.mongodb.net/test")
mydatabase = client['mongo']

user_info = mydatabase['user_info']
password = mydatabase['password']


#Extra
def zodiac_counter():
    count_={}
    zod_list= ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Pisces","Aquarius"] 
    for zod in zod_list:
        count_[zod]=user_info.count_documents({"zodiac": zod.lower()})
    return count_

def max_zod():
    count_=zodiac_counter()
    for key,value in count_.items():
        if int(value) == max(count_.values()):
            return (f"The most common zodiac sign is {key}  :  {value}")



def show_signs():
    counta=zodiac_counter()
    labels = list(counta.keys())
    values = list(counta.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title('Zodiac Distribution Pie Chart')
    plt.ylabel("")
    plt.legend(labels, loc='center left', bbox_to_anchor=(-0.35, .5),fontsize=8)
    return fig


def num_docs_(): 
 num_docs = user_info.count_documents({})
 print (num_docs)

def otp():
    random_str = ""
    for i in range(6):
        index = random.randint(0,9)
        random_str += str(index)
    return random_str

def get_next_user_id():
    high=user_info.find_one(sort=[('id',-1)])
    if high is None:
        return 1
    else: 
        return high['id']+1
    
def get_id(email):
    for record in user_info.find({"email": email}):
        id=record["id"]
        return id
     
def show_user_name():
    cursor = user_info.find()
    a=[]
    for record in cursor:
        a.append(record)
    return a

def verify_pass(email):
    for record in password.find({"email": email}):
        pass_=record["password"]
        return pass_
    
def status(email):
    for record in password.find({"email": email}):
        pass_=record["status"]
        return pass_

def delete(email):
    id = get_id(email)
    for record in user_info.find({"id": int(id)}):
        email=record["email"]
        password.find({"email": email})
        user_info.delete_one({"id": int(id)})

def get_db(id):
    for record in user_info.find({"id": int(id)}):
        db=record["db"]
        return db

def update(name,email,db,status):
    id=get_id(email)
    for record in password.find({"email": str(email)}):
            a=record
            a["status"]=status
            password.find_one_and_replace({"email": str(email)},a)
    for record in user_info.find({"email": str(email)}):
            a=record
            a["name"]=name
            a["email"]=email
            a["db"]=db
            user_info.find_one_and_replace({"id": int(id)},a)
    
def update_pass(email,old_pass,new_pass):
    if old_pass==verify_pass(email):
        for record in password.find({"email": str(email)}):
            a=record
            a["password"]=new_pass
            password.find_one_and_replace({"email": str(email)},a)

def update_pass_(email,new_pass):
    for record in password.find({"email": str(email)}):
        a=record
        a["password"]=new_pass
        password.find_one_and_replace({"email": str(email)},a)

def login_times(email):
    a=password.find_one({"email":email})
    b=a["no_of_logins"]+1
    a["no_of_logins"]=b
    password.find_one_and_replace({"email":email},a)   
    
def get_zodiac(dob):
    Birthdate = dob
    Birthdate = datetime.datetime.strptime(Birthdate,"%Y-%m-%d")
    if (Birthdate.month) == 1:
        if (Birthdate.day)>=(20):
            return "aquarius"
        else: return "capricorn"
    elif (Birthdate.month) == 2:
        if (Birthdate.day)>=(19):
            return "pisces"
        else: return "aquarius"
    elif (Birthdate.month) == 3:
        if (Birthdate.day)>=(21):
            return "aries"
        else: return "pisces"
    elif (Birthdate.month) == 4:
        if (Birthdate.day)>=(20):
            return "taurus"
        else: return "aries"
    elif (Birthdate.month) == 5:
        if (Birthdate.day)>=(21):
            return "gemini"
        else: return "taurus" 
    elif (Birthdate.month) == 6:
        if (Birthdate.day)>=(22):
            return "cancer"
        else: return "gemini"
    elif (Birthdate.month) == 7:
        if (Birthdate.day)>=(23):
            return "leo"
        else: return "cancer"
    elif (Birthdate.month) == 8:
        if (Birthdate.day)>=(23):
            return "virgo"
        else: return "leo"  
    elif (Birthdate.month) == 9:
        if (Birthdate.day)>=(22):
            return "libra"
        else: return "virgo" 
    elif (Birthdate.month) == 10:
        if (Birthdate.day)>=(23):
            return "scorpio"
        else: return "libra"
    elif (Birthdate.month) == 11:
        if (Birthdate.day)>=(22):
            return "sagittarius"
        else: return "scorpio" 
    elif (Birthdate.month) == 12:
        if (Birthdate.day)>=(19):
            return "capricorn"
        else: return "sagittarius"

def insert_one(name,email,dob):
    record = { "id": int(get_next_user_id()),"name": str(name),"email": str(email),"db":str(dob),"zodiac":str(get_zodiac(dob))}
    user_info.insert_one(record)    

def insert_user(name,email,password_,dob):
    record = {"email": str(email),"password":str(password_),"no_of_logins":0,"status":"user"}
    password.insert_one(record)
    insert_one(name,email,dob)

def email_verify(email_):
    for record in password.find({"email": email_}):
            return record["email"]
