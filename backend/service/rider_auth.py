import logging
from typing import Literal, Tuple

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from backend.entities.rider import Rider
from backend.repository import Repository


class ServiceRiderAuth:
    def __init__(self, repository: Repository):
        self.repository = repository

    def rider_email_sign_up(self, email: str, password: str, session: Session = None) -> None:
        if not session:
            logging.warn("Session was not provided")
        try:
            self.repository.rider.get_by_email(email, session)
        except NoResultFound:
            logging.info(f"Rider {email} signing up")
        else:
            raise FileExistsError(f"Rider {email} already exists")

        response = self.repository.supabase.auth.sign_in_with_otp({
            'email': email,
            'type': "email",
            'options': {
                # 'email_redirect_to': 'https://example.com/welcome',
            },
        })
        print("THE RESPONSE", response)
        self.repository.rider.insert_one(Rider(
            auth_id=response.user.id,
            email=email,
            password=password,  # TODO do not plaintext
        ), session=session)

    # def rider_email_sign_in(self, email: str, password: str, session: Session = None) -> Tuple[str, str]:
    #     if not session:
    #         logging.warn("Session was not provided")
    #     rider: Rider = self.repository.rider.get_by_email(email, session)
    #     data = self.repository.supabase.auth.sign_in_with_password({
    #         'email': email,
    #         'password': password,
    #     })
    #     # {'user': {'id': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6', 'app_metadata': {'provider': 'email', 'providers': ['email']}, 'user_metadata': {'email': 'ptrkhh@outlook.com', 'email_verified': False, 'phone_verified': False, 'sub': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6'}, 'aud': 'authenticated', 'confirmation_sent_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 362936, tzinfo=datetime.timezone.utc), 'recovery_sent_at': datetime.datetime(2024, 12, 24, 13, 8, 41, 555390, tzinfo=datetime.timezone.utc), 'email_change_sent_at': None, 'new_email': None, 'new_phone': None, 'invited_at': None, 'action_link': None, 'email': 'ptrkhh@outlook.com', 'phone': '', 'created_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 353621, tzinfo=datetime.timezone.utc), 'confirmed_at': datetime.datetime(2024, 12, 24, 12, 40, 15, 93668, tzinfo=datetime.timezone.utc), 'email_confirmed_at': datetime.datetime(2024, 12, 24, 12, 40, 15, 93668, tzinfo=datetime.timezone.utc), 'phone_confirmed_at': None, 'last_sign_in_at': datetime.datetime(2025, 1, 25, 13, 1, 56, 490295, tzinfo=datetime.timezone.utc), 'role': 'authenticated', 'updated_at': datetime.datetime(2025, 1, 25, 13, 1, 56, 514820, tzinfo=datetime.timezone.utc), 'identities': [{'id': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6', 'identity_id': '436594b2-caa0-4dbc-a7bf-659d2552d736', 'user_id': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6', 'identity_data': {'email': 'ptrkhh@outlook.com', 'email_verified': False, 'phone_verified': False, 'sub': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6'}, 'provider': 'email', 'created_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 359931, tzinfo=datetime.timezone.utc), 'last_sign_in_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 359880, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 359931, tzinfo=datetime.timezone.utc)}], 'is_anonymous': False, 'factors': None}, 'session': {'provider_token': None, 'provider_refresh_token': None, 'access_token': 'eyJhbGciOiJIUzI1NiIsImtpZCI6IkJ2bk9oZ1hMaS9Sd2R4b3QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3dncWFqa2Ryb29scG1xdGRsdmxnLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI2ZDYyZDk1Mi1kOGM4LTRlYTktYWQ0NS1jMTdmYzhkZjJhYzYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM3ODEzNzE2LCJpYXQiOjE3Mzc4MTAxMTYsImVtYWlsIjoicHRya2hoQG91dGxvb2suY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6InB0cmtoaEBvdXRsb29rLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI2ZDYyZDk1Mi1kOGM4LTRlYTktYWQ0NS1jMTdmYzhkZjJhYzYifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczNzgxMDExNn1dLCJzZXNzaW9uX2lkIjoiYjhkZDk2NjMtNmRmNy00N2M4LTljMGItMDY5MGEyNzk4NDE0IiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.3GVrRVkVi-tIorKHyoBfOwYpRmh2k7R95zVpQbroGzY', 'refresh_token': 'uxAyVdbbW4L6LZvLcUY4qg', 'expires_in': 3600, 'expires_at': 1737813716, 'token_type': 'bearer', 'user': {'id': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6', 'app_metadata': {'provider': 'email', 'providers': ['email']}, 'user_metadata': {'email': 'ptrkhh@outlook.com', 'email_verified': False, 'phone_verified': False, 'sub': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6'}, 'aud': 'authenticated', 'confirmation_sent_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 362936, tzinfo=datetime.timezone.utc), 'recovery_sent_at': datetime.datetime(2024, 12, 24, 13, 8, 41, 555390, tzinfo=datetime.timezone.utc), 'email_change_sent_at': None, 'new_email': None, 'new_phone': None, 'invited_at': None, 'action_link': None, 'email': 'ptrkhh@outlook.com', 'phone': '', 'created_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 353621, tzinfo=datetime.timezone.utc), 'confirmed_at': datetime.datetime(2024, 12, 24, 12, 40, 15, 93668, tzinfo=datetime.timezone.utc), 'email_confirmed_at': datetime.datetime(2024, 12, 24, 12, 40, 15, 93668, tzinfo=datetime.timezone.utc), 'phone_confirmed_at': None, 'last_sign_in_at': datetime.datetime(2025, 1, 25, 13, 1, 56, 490295, tzinfo=datetime.timezone.utc), 'role': 'authenticated', 'updated_at': datetime.datetime(2025, 1, 25, 13, 1, 56, 514820, tzinfo=datetime.timezone.utc), 'identities': [{'id': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6', 'identity_id': '436594b2-caa0-4dbc-a7bf-659d2552d736', 'user_id': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6', 'identity_data': {'email': 'ptrkhh@outlook.com', 'email_verified': False, 'phone_verified': False, 'sub': '6d62d952-d8c8-4ea9-ad45-c17fc8df2ac6'}, 'provider': 'email', 'created_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 359931, tzinfo=datetime.timezone.utc), 'last_sign_in_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 359880, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 12, 24, 12, 39, 57, 359931, tzinfo=datetime.timezone.utc)}], 'is_anonymous': False, 'factors': None}}}
    #     # TODO INSERT AUTH ID
    #     return data.session.access_token, data.session.refresh_token

    def rider_email_otp_request(self, email: str, session: Session = None) -> None:
        self._rider_otp_request(email, "email", session)

    def rider_phone_otp_request(self, phone: str, session: Session = None) -> None:
        # TODO convert to E164
        self._rider_otp_request(phone, "phone", session)

    def _rider_otp_request(self, email_or_phone: str, type: Literal["email", "phone"], session: Session = None) -> None:
        if type == "phone":
            raise NotImplementedError("Phone OTP has not been implemented yet")
        if not session:
            logging.warn("Session was not provided")

        response = self.repository.supabase.auth.sign_in_with_otp({
            type: email_or_phone,
            'type': type,
            'options': {
                # set this to false if you do not want the user to be automatically signed up
                'should_create_user': False,
                # 'email_redirect_to': 'https://example.com/welcome',
            },
        })
        return response

    def rider_phone_otp_verify(self, phone: str, otp: str, session: Session = None):
        # TODO convert to E164
        return self._rider_otp_verify(phone, otp, "sms", session)

    def rider_email_otp_verify(self, email: str, otp: str, session: Session = None):
        return self._rider_otp_verify(email, otp, "email", session)

    def _rider_otp_verify(self, email: str, otp: str, type: str, session: Session = None):
        if not session:
            logging.warn("Session was not provided")
        response = self.repository.supabase.auth.verify_otp({
            'email': email,
            'token': otp,
            'type': type,
        })
        # TODO INSERT AUTH ID
        return response.session.access_token, response.session.refresh_token
