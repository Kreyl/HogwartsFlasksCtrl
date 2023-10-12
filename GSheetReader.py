import gspread
from google.oauth2.service_account import Credentials


class GSheetRdr:
    url = ""

    def __init__(self):
        self.sheet1 = None

    def Connect(self):
        # If you would like to restrict your program from updating any data,
        # you can specify spreadsheets.readonly and drive.readonly in the scope.
        # scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        scope = ['https://www.googleapis.com/auth/spreadsheets.readonly',
                 'https://www.googleapis.com/auth/drive.readonly']
        # Build a Credentials object with our JSON file
        creds = Credentials.from_service_account_file("TableReader.json", scopes=scope)
        client = gspread.authorize(creds)
        # Get sheet
        google_sh = client.open_by_url(self.url)
        self.sheet1 = google_sh.get_worksheet(0)

    def GetCellInt(self, cellstr):
        txt = self.sheet1.acell(cellstr).value
        if txt:
            try:
                v = int(txt)
                return v
            except ValueError:
                pass
        return None

