import requests
import json
# print(response.json())



if __name__ == "__main__":
    sample_patient = {
        "pid":"HN1234567890",
        "pname":"นายสมชาย",
        "psurname":"เด็กมทส",
        "Data":[124,164,146,153,183.1,112,142,111.2,135,164.1,153.2,121.1,152,132]
    }
    print(sample_patient)
    json_object = json.dumps(sample_patient, indent = 4) 

    response = requests.post('http://localhost:8080/nail', data=json_object)
    print(response.text)