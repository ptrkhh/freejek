import asyncio

from supabase import create_client, Client

url: str = "https://wgqajkdroolpmqtdlvlg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndncWFqa2Ryb29scG1xdGRsdmxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY5ODQ5MDIsImV4cCI6MjA0MjU2MDkwMn0.M2p9RfXyFEvgmW4-WBj2olZ8c-OopBrOV1uTcXIslf4"
supabase: Client = create_client(url, key)


def sign_up():
    data = supabase.auth.sign_up({
        'email': 'ptrkhh@outlook.com',
        'password': 'example-password',
        'options': {
            'email_redirect_to': 'https://example.com/welcome',
        },
    })
    return data

def sign_in():
    data = supabase.auth.sign_in_with_password({
        'email': 'ptrkhh@outlook.com',
        'password': 'example-password',
    })
    return data

def sign_in_magic():
    response = supabase.auth.sign_in_with_otp({
      'email': 'ptrkhh@gmail.com',
      'options': {
        # set this to false if you do not want the user to be automatically signed up
        'should_create_user': False,
        'email_redirect_to': 'https://example.com/welcome',
      },
    })
    return response

def sign_in_otp():
    response = supabase.auth.sign_in_with_otp({
        'email': 'ptrkhh@outlook.com',
        'options': {
            # set this to false if you do not want the user to be automatically signed up
            'should_create_user': False,
        },
    })
    return response

def verify_otp():
    response = supabase.auth.verify_otp({
        'email': "ptrkhh@outlook.com",
        'token': '353451',
        'type': 'email',
    })
    return response

res = verify_otp()
print("THE RES", res)
print("lagi")