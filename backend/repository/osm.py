from typing import List, Tuple

import requests

from entities.latlon import LatLon


class RepositoryOsm:
    def __init__(self):
        self.osm_url_prefix = "http://router.project-osrm.org"  # TODO env

    def calculate_distance_matrix(self, locations: List[LatLon]) -> Tuple[List[List[float]], List[List[float]]]:
        prefix = "/table/v1/car/"
        suffix = "?annotations=distance,duration&fallback_coordinate=snapped&skip_waypoints=true"

        combined_coords: str = ";".join([f"{loc.lon},{loc.lat}" for loc in locations])
        url: str = f"{self.osm_url_prefix}{prefix}{combined_coords}{suffix}"
        response: requests.Response = requests.get(url)
        # Raise an exception if the API request was not successful
        response.raise_for_status()

        return ([[j for j in i] for i in response.json()["distances"]],
                [[j / 60 for j in i] for i in response.json()["durations"]])

    def generate_path(self, orig: LatLon, dest: LatLon):
        # http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.428555,52.523219?steps=true
        prefix = "/route/v1/car/"
        suffix = "?steps=true"

        combined_coords: str = f"{orig.lon},{orig.lat};{dest.lon},{dest.lat}"
        url: str = f"{self.osm_url_prefix}{prefix}{combined_coords}{suffix}"
        response: requests.Response = requests.get(url)
        # Raise an exception if the API request was not successful
        response.raise_for_status()

        response_json = response.json()
        route = response_json["routes"][0]
        leg = route["legs"][0]
        steps = leg["steps"]
        return [LatLon(lat=i["maneuver"]["location"][1], lon=i["maneuver"]["location"][0]) for i in steps]
