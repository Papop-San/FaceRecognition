import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("./Encode_app/faceattenreal-time-firebase-adminsdk-vdkyg-eaaec9b1c6.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattenreal-time-default-rtdb.firebaseio.com/"
})
 
ref = db.reference("Students")

data = {
    "6406022620096":{
        "name":"Chalonrath Kodsrivong",
        "id":'6406022620096',
        "depart":"INE",
        "year":3,
        "gpa": 2.5,
        "province":"PrachinBuri"
    },
    "6406022610031":{
        "name":"Papop Sangeamsak",
        'id':'6406022610031',
        "depart":"INE",
        "year":3,
        "gpa": 3.08,
        "province":"Sisaket"
    }
}

for key , value in data.items():
    ref.child(key).set(value)