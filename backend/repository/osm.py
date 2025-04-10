from typing import List, Tuple

import requests

from entities.latlon import LatLon


class RepositoryOsm:
    def __init__(self):
        self.osm_url_prefix = "http://router.project-osrm.org/table/v1/car/"  # TODO env
        self.osm_url_suffix = "?annotations=distance,duration&fallback_coordinate=snapped&skip_waypoints=true"  # TODO env

    def calculate_distance_matrix(self, locations: List[LatLon]) -> Tuple[List[List[float]], List[List[float]]]:
        combined_coords: str = ";".join([f"{loc.lon},{loc.lat}" for loc in locations])
        url: str = f"{self.osm_url_prefix}{combined_coords}{self.osm_url_suffix}"
        response: requests.Response = requests.get(url)
        # Raise an exception if the API request was not successful
        response.raise_for_status()

        return ([[j for j in i] for i in response.json()["distances"]],
                [[j / 60 for j in i] for i in response.json()["durations"]])
