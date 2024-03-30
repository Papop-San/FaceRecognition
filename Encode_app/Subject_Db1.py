import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("./Encode_app/faceattenreal-time-firebase-adminsdk-vdkyg-eaaec9b1c6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattenreal-time-default-rtdb.firebaseio.com/"
})

ref = db.reference('Subject')

data = {
    "INE": {
        "23:03:2024": {
            "09:00:00": {
                'subject_name': 'English',
                'time_for_test': '09:00:00-12:00:00'
            },
            "13:00:00": {
                'subject_name': 'Thai',
                'time_for_test': '13:00:00-16:00:00'
            }
        },
        "24:03:2024": {
            "09:00:00": {
                'subject_name': 'Cyber Security',
                'time_for_test': '09:00:00-12:00:00'
            },
            "13:00:00": {
                'subject_name': 'Machine Learning',
                'time_for_test': '13:00:00-16:00:00'
            }
        },
         "28:03:2024": {
            "09:00:00": {
                'subject_name': 'Telecomunication',
                'time_for_test': '09:00:00-12:00:00'
            },
            "13:00:00": {
                'subject_name': 'COOP-Perative',
                'time_for_test': '13:00:00-16:00:00'
            }
        },
    },
    "INET": {
        "23:03:2024": {
            "06:00:00": {
                'subject_name': 'Computer Science',
                'time_for_test': '06:00:00-09:00:00'
            },
            "09:00:00": {
                'subject_name': 'Cybersecurity',
                'time_for_test': '09:00:00-12:00:00'
            },
            "13:00:00": {
                'subject_name': 'Thai',
                'time_for_test': '13:00:00-16:00:00'
            }

        },
        "24:03:2024": {
            "09:00:00": {
                'subject_name': 'English',
                'time_for_test': '09:00:00-12:00:00'
            },
            "13:00:00": {
                'subject_name': 'Thai',
                'time_for_test': '13:00:00-16:00:00'
            }
        },
        "28:03:2024": {
            "09:00:00": {
                'subject_name': 'Data Stucture',
                'time_for_test': '09:00:00-12:00:00'
            },
            "13:00:00": {
                'subject_name': 'Cyber Security',
                'time_for_test': '13:00:00-16:00:00'
            }
        },
    },
}

for key, value in data.items():
    ref.child(key).set(value)
