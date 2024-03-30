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
    },
    "6406022610031":{
        "name":"Papop Sangeamsak",
        'id':'6406022610031',
        "depart":"INE",
        "year":3,
    },
    "6406022610040":{
        "name":"Pawaris Pitirit",
        'id':'6406022610040',
        "depart":"INE",
        "year":3,
    },
    "6406022610058":{
        "name":"Piyawan Nimpraprut",
        'id':'6406022610058',
        "depart":"INE",
        "year":3,
    },
    "6406022610023":{
        "name":"Nititat Bangpra",
        'id':'6406022610023',
        "depart":"INE",
        "year":3,
    },
    "6406022620011":{
        "name":"Jakapat Jodduangchan",
        'id':'6406022620011',
        "depart":"INE",
        "year":3,
    },

    "6406022620037":{
        "name":"Bunnapon",
        'id':'6406022620037',
        "depart":"INE",
        "year":3,
    },
    "6406022620053":{
        "name":"Watcharakron",
        'id':'6406022620053',
        "depart":"INE",
        "year":3,
    },
    "6406022620061":{
        "name":"Mathawee Robkhob",
        'id':'6406022620061',
        "depart":"INE",
        "year":3,
    },
    "6406022620070":{
        "name":"Rawiporn Suamsiri",
        'id':'6406022620070',
        "depart":"INE",
        "year":3,
    },
    "6406022620088":{
        "name":"Puntita Chaungchawna",
        'id':'6406022620088',
        "depart":"INE",
        "year":3,
    },
    "6406022630016":{
        "name":"Kamonwan Janmanee",
        'id':'6406022630016',
        "depart":"INE",
        "year":3,
    },
    "6406022420045":{
        "name":"Teeraporn Petchrote",
        'id':'6406022420045',
        "depart":"INET",
        "year":3,
    },
    
}

for key , value in data.items():
    ref.child(key).set(value)