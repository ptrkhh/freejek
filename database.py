from supabase import create_client

SUPABASE_URL = "https://wgqajkdroolpmqtdlvlg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndncWFqa2Ryb29scG1xdGRsdmxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY5ODQ5MDIsImV4cCI6MjA0MjU2MDkwMn0.M2p9RfXyFEvgmW4-WBj2olZ8c-OopBrOV1uTcXIslf4"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

