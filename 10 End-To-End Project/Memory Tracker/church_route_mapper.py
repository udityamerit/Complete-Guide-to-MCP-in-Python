"""
Church Route Mapper using Google Maps API
Maps the optimal route between multiple churches to visit
"""

import googlemaps
from datetime import datetime
import json

# List of churches to visit (add your churches here)
CHURCHES_TO_VISIT = [
    "St. Paul's Cathedral, London",
    "Westminster Abbey, London",
    "St. Pancras Church, London",
    "Christ Church, London"
]

# Initialize Google Maps client
# Get your API key from: https://developers.google.com/maps/documentation/distance-matrix/get-api-key
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"

def get_distance_matrix(locations, api_key):
    """
    Get distance and duration between all pairs of locations
    """
    gmaps = googlemaps.Client(key=api_key)
    
    try:
        result = gmaps.distance_matrix(
            origins=locations,
            destinations=locations,
            mode="driving",
            units="metric"
        )
        return result
    except Exception as e:
        print(f"Error getting distance matrix: {e}")
        return None

def get_directions(origin, destination, api_key):
    """
    Get turn-by-turn directions between two locations
    """
    gmaps = googlemaps.Client(key=api_key)
    
    try:
        result = gmaps.directions(
            origin=origin,
            destination=destination,
            mode="driving"
        )
        return result
    except Exception as e:
        print(f"Error getting directions: {e}")
        return None

def calculate_total_distance(locations, api_key):
    """
    Calculate total distance for visiting all churches in order
    """
    gmaps = googlemaps.Client(key=api_key)
    total_distance = 0
    total_duration = 0
    
    for i in range(len(locations) - 1):
        try:
            result = gmaps.distance_matrix(
                origins=locations[i],
                destinations=locations[i + 1],
                mode="driving"
            )
            
            if result['rows']:
                distance = result['rows'][0]['elements'][0]['distance']['value']  # meters
                duration = result['rows'][0]['elements'][0]['duration']['value']   # seconds
                
                total_distance += distance
                total_duration += duration
                
                print(f"\n{locations[i]} → {locations[i + 1]}")
                print(f"Distance: {distance / 1000:.2f} km")
                print(f"Duration: {duration / 60:.0f} minutes")
        except Exception as e:
            print(f"Error: {e}")
    
    return total_distance, total_duration

def generate_route_summary(churches):
    """
    Generate a summary of the route
    """
    print("\n" + "="*60)
    print("CHURCH ROUTE MAPPER")
    print("="*60)
    print(f"\nChurches to visit ({len(churches)}):")
    for i, church in enumerate(churches, 1):
        print(f"{i}. {church}")
    print("\n" + "="*60)

def main():
    """
    Main function to run the church route mapper
    """
    if GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
        print("ERROR: Please set your Google Maps API key in the script")
        print("Get one at: https://developers.google.com/maps/documentation/distance-matrix/get-api-key")
        return
    
    generate_route_summary(CHURCHES_TO_VISIT)
    
    # Calculate total distance and time
    print("\nCalculating route details...")
    total_distance, total_duration = calculate_total_distance(CHURCHES_TO_VISIT, GOOGLE_MAPS_API_KEY)
    
    print("\n" + "="*60)
    print("ROUTE SUMMARY")
    print("="*60)
    print(f"Total Distance: {total_distance / 1000:.2f} km")
    print(f"Total Duration: {total_duration / 3600:.1f} hours ({total_duration / 60:.0f} minutes)")
    print("="*60)
    
    # Optional: Get detailed directions for first leg
    if len(CHURCHES_TO_VISIT) > 1:
        print(f"\nGetting detailed directions from {CHURCHES_TO_VISIT[0]} to {CHURCHES_TO_VISIT[1]}...")
        directions = get_directions(CHURCHES_TO_VISIT[0], CHURCHES_TO_VISIT[1], GOOGLE_MAPS_API_KEY)
        
        if directions:
            for step in directions[0]['legs'][0]['steps'][:5]:  # Show first 5 steps
                print(f"- {step['html_instructions']}")

if __name__ == "__main__":
    main()
