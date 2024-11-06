from amadeus import Client, ResponseError
import os
from dotenv import load_dotenv

load_dotenv()

amadeus = Client(
    client_id=os.getenv('AMADEUS_CLIENT_ID'),
    client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
)

try:
    # A simple API call to test authentication
    response = amadeus.reference_data.urls.checkin_links.get(airlineCode='BA')
    print("Authentication successful. Your API credentials are valid.")
except ResponseError as error:
    print(f"Authentication failed: {error}")
