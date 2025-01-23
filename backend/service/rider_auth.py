import logging

from gotrue import AuthResponse
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from backend.entities.rider import Rider
from backend.repository import Repository


class ServiceRiderAuth:
    def __init__(self, repository: Repository):
        self.repository = repository

    def rider_email_sign_up(self, email: str, password: str, session: Session = None):
        if not session:
            logging.warn("Session was not provided")
        try:
            self.repository.rider.get_by_id(email, session)
        except NoResultFound as e:
            logging.info(f"Rider {email} signing up")
        else:
            raise FileExistsError(f"Rider {email} already exists")

        # TODO check if supabase auth already exists
        if True:
            data: AuthResponse = self.repository.supabase_client.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    # 'email_redirect_to': 'https://example.com/welcome',
                },
            })
        else:
            pass
            # supabase auth login
        self.repository.rider.insert_one(Rider(
            email=email,
            password=password,  # TODO do not plaintext
        ), session=session)
        return data.session.access_token, data.session.refresh_token

    def rider_email_sign_in(self, email: str, password: str, session: Session = None):
        if not session:
            logging.warn("Session was not provided")
        rider: Rider = self.repository.rider.get_by_id(email, session)
        data = self.repository.supabase.auth.sign_in_with_password({
            'email': email,
            'password': password,
        })
        return data

    def rider_email_otp_request(self, email: str, session: Session = None):
        self._rider_otp_request(email, "email", session)

    def rider_phone_otp_request(self, phone: str, session: Session = None):
        # TODO convert to E164
        self._rider_otp_request(phone, "phone", session)

    def _rider_otp_request(self, email_or_phone: str, type: Literal["email", "phone"], session: Session = None):
        if not session:
            logging.warn("Session was not provided")
        response = self.repository.supabase.auth.sign_in_with_otp({
            type: email_or_phone,
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
        return response
