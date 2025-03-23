from math import radians, cos
from typing import Tuple

import jwt

from backend.entities.latlon import LatLon


def verify_token_driver(token: str) -> Tuple[str, str, bool, str]:
    secret_key = "ABCD"  # TODO

    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    method = payload.get("app_metadata").get("provider")
    is_verified = payload.get("user_metadata").get(f"{method}_verified")
    email = payload.get("email")
    phone = payload.get("phone")
    return email, phone, is_verified, method
    # except ExpiredSignatureError:
    #     logger.warning("Token has expired")
    #     raise HTTPException(status_code=401, detail="Token has expired")
    # except InvalidTokenError:
    #     logger.warning("Token is invalid")
    #     raise HTTPException(status_code=401, detail="Invalid token")


def verify_token_rider(token: str) -> Tuple[str, str, bool, str]:
    secret_key = "ABCD"  # TODO

    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    method = payload.get("app_metadata").get("provider")
    is_verified = payload.get("user_metadata").get(f"{method}_verified")
    email = payload.get("email")
    phone = payload.get("phone")
    return email, phone, is_verified, method
    # except ExpiredSignatureError:
    #     logger.warning("Token has expired")
    #     raise HTTPException(status_code=401, detail="Token has expired")
    # except InvalidTokenError:
    #     logger.warning("Token is invalid")
    #     raise HTTPException(status_code=401, detail="Invalid token")


def minmaxlatlon(loc: LatLon, cluster_size_in_meters: int) -> Tuple[LatLon, LatLon]:
    distlat: float = cluster_size_in_meters / 111111.1  # 1 degree in meters
    minlat: float = loc.lat - distlat
    maxlat: float = loc.lat + distlat

    mindistlon: float = cluster_size_in_meters / (111111.1 * cos(radians(minlat)))
    minlon: float = loc.lon - mindistlon
    maxdistlon: float = cluster_size_in_meters / (111111.1 * cos(radians(maxlat)))
    maxlon: float = loc.lon + maxdistlon

    return LatLon(lat=minlat, lon=minlon), LatLon(lat=maxlat, lon=maxlon)
