# attractions_data.py

def get_attractions(destination):
    attractions_db = {
        'Paris': [
            {'name': 'Eiffel Tower', 'description': 'Iconic symbol of Paris.'},
            {'name': 'Louvre Museum', 'description': 'World\'s largest art museum.'},
            {'name': 'Notre-Dame Cathedral', 'description': 'Famous medieval cathedral.'}
        ],
        'London': [
            {'name': 'Big Ben', 'description': 'Famous clock tower.'},
            {'name': 'London Eye', 'description': 'Giant Ferris wheel on the South Bank of the Thames.'},
            {'name': 'Tower of London', 'description': 'Historic castle located on the north bank of the River Thames.'}
        ],
        'New York': [
            {'name': 'Statue of Liberty', 'description': 'Iconic National Monument.'},
            {'name': 'Central Park', 'description': 'Urban park in Manhattan.'},
            {'name': 'Times Square', 'description': 'Major commercial intersection and tourist destination.'}
        ],
        'Tokyo': [
            {'name': 'Tokyo Tower', 'description': 'Communications and observation tower.'},
            {'name': 'Meiji Shrine', 'description': 'Shinto shrine dedicated to Emperor Meiji.'},
            {'name': 'Senso-ji', 'description': 'Ancient Buddhist temple.'}
        ]
    }

    return attractions_db.get(destination, [])
