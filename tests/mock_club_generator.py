import json

def generate_mock_clubs():
    points = ["0", "5", "12", "15"]

    clubs = [{
        "name":f"Club{id}",
        "email":f"club{id}@test.com",
        "points":point
    } for (id, point) in enumerate(points)]
    
    clubs_json = {
        "clubs": clubs
    }

    with open('tests/test_global_clubs.json', 'w') as json_file:
        json.dump(clubs_json, json_file, indent=4)
    
    clubs.append({'name': 'Unknown', 'email': 'unknown@unknown.com', 'points': '5'})

    return clubs

