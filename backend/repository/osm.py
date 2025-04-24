from typing import List, Tuple, Optional

import requests

from entities.latlon import LatLon
from entities.web_api import Poi


class RepositoryOsm:
    def calculate_distance_matrix(self, locations: List[LatLon]) -> Tuple[List[List[float]], List[List[float]]]:
        prefix = "http://router.project-osrm.org/table/v1/car/"
        suffix = "?annotations=distance,duration&fallback_coordinate=snapped&skip_waypoints=true"

        combined_coords: str = ";".join([f"{loc.lon},{loc.lat}" for loc in locations])
        url: str = f"{prefix}{combined_coords}{suffix}"
        response: requests.Response = requests.get(url)
        # Raise an exception if the API request was not successful
        response.raise_for_status()

        return ([[j for j in i] for i in response.json()["distances"]],
                [[j / 60 for j in i] for i in response.json()["durations"]])

    def generate_path(self, orig: LatLon, dest: LatLon):
        prefix = "http://router.project-osrm.org/route/v1/car/"
        suffix = "?steps=true"

        combined_coords: str = f"{orig.lon},{orig.lat};{dest.lon},{dest.lat}"
        url: str = f"{prefix}{combined_coords}{suffix}"
        response: requests.Response = requests.get(url)
        # Raise an exception if the API request was not successful
        response.raise_for_status()

        response_json = response.json()
        return [
            LatLon(lat=i["maneuver"]["location"][1], lon=i["maneuver"]["location"][0])
            for i in response_json["routes"][0]["legs"][0]["steps"]
        ]

    def search_poi(self, orig: LatLon, q: str, limit: Optional[int] = 10):
        q = f"&q={q}" if q else ""
        url: str = f"https://photon.komoot.io/api/?lon={orig.lon}&lat={orig.lat}&limit={limit}{q}"
        response: requests.Response = requests.get(url)
        # Raise an exception if the API request was not successful
        response.raise_for_status()

        response_json = response.json()
        return [
            Poi(
                location=LatLon(lat=i["geometry"]["coordinates"][1], lon=i["geometry"]["coordinates"][0]),
                name=i["properties"]["name"],
                street=i["properties"]["street"],
                postal_code=i["properties"]["postcode"],
            )
            for i in response_json["features"]
        ]
