# test_api.py

import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Amadeus API client with logging enabled for debugging
amadeus = Client(
    client_id=os.getenv('AMADEUS_CLIENT_ID'),
    client_secret=os.getenv('AMADEUS_CLIENT_SECRET'),
    log_level='debug'  # Set log level to debug
)

def test_get_hotels():
    city_code = 'PAR'  # IATA code for Paris
    check_in = '2024-12-01'
    check_out = '2024-12-05'
    try:
        # Step 1: Get hotel IDs for the city
        hotel_list_response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)
        hotel_ids = [hotel['hotelId'] for hotel in hotel_list_response.data]
        if not hotel_ids:
            print("No hotels found in the specified city.")
            return

        # Step 2: Get hotel offers using hotel IDs
        response = amadeus.shopping.hotel_offers_search.get(
            hotelIds=','.join(hotel_ids[:10]),  # Limit to first 10 hotel IDs
            checkInDate=check_in,
            checkOutDate=check_out,
            adults=2,
            roomQuantity=1,
            paymentPolicy='NONE',
            includeClosed=False,
            bestRateOnly=True,
            sort='PRICE'
        )
        hotels = response.data
        if hotels:
            print(f"Fetched offers for {len(hotels)} hotels in city code {city_code}.\n")
            for hotel in hotels[:3]:
                hotel_name = hotel['hotel']['name']
                address = hotel['hotel']['address'].get('lines', [])
                city = hotel['hotel']['address'].get('cityName', '')
                print(f"Hotel Name: {hotel_name}")
                print(f"Address: {', '.join(address)}, {city}\n")
        else:
            print("No hotel offers found.")
    except ResponseError as error:
        print(f"Amadeus API ResponseError in get_hotels: {error}")
        if error.response and error.response.body:
            error_details = error.response.result
            print("Error Details:")
            print(error_details)
    except Exception as e:
        print(f"Unexpected error in get_hotels: {e}")

def test_get_attractions():
    try:
        response = amadeus.reference_data.locations.points_of_interest.get(
            latitude=48.8566,
            longitude=2.3522,
            radius=2,
            page_limit=10,
            categories='SIGHTSEEING'
        )
        attractions = response.data
        if attractions:
            print(f"Fetched {len(attractions)} attractions.\n")
            for attraction in attractions[:3]:
                attraction_name = attraction.get('name', 'No Name')
                print(f"Attraction Name: {attraction_name}\n")
            else:
                print("No attractions found.")
    except ResponseError as error:
        print(f"Amadeus API ResponseError in get_attractions: {error}")
        if error.response and error.response.body:
            error_details = error.response.result
            print("Error Details:")
            print(error_details)
    except Exception as e:
        print(f"Unexpected error in get_attractions: {e}")

if __name__ == "__main__":
    print("Testing Hotel Offers Search:\n")
    test_get_hotels()
    print("\nTesting Points of Interest:\n")
    test_get_attractions()
