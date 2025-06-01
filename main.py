import login
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if __name__ == "__main__":
    app = login.ModernLogin()
    app.mainloop()