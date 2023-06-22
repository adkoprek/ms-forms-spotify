import tkinter as tk
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WEB_DRIVER_OPTIONS = Options()
WEB_DRIVER_OPTIONS.add_argument("--window-size1920,1080")

class Window(tk.Tk):
    entry1 = None
    list1 = None
    option_menu_variable1 = None
    label1 = None
    data = []

    def __init__(self):
        super().__init__()
        self.set_up_window()
        self.set_up_content()
        self.mainloop()

    def set_up_window(self):
        self.geometry("400x800")

    def set_up_content(self):
        H1 = ("Arial", 30)
        H2 = ("Arial", 18)
        P = ("Arial", 13)

        tk.Label(self, text="MS Forms Bot", font=H1).pack(fill="x", pady=(20, 0))

        tk.Label(self, text="Enter you spotify playlist or album", font=H2).pack(fill="x", pady=(30, 0))
        self.entry1 = tk.Entry(self, font=P)
        self.entry1.pack(fill="x", padx=20)
        self.list1 = tk.Listbox(self, font=P, height=18)
        self.list1.pack(fill="x", padx=20, pady=(10, 0))
        tk.Button(self, text="Check Titles From Spotify", command=self.get_spotify_data, font=P).pack(pady=(10, 0), anchor=tk.CENTER)

        tk.Label(self, text="Choose your Browser", font=H2).pack(fill="x", pady=(30, 0))
        options = ["Firefox", "Chrome", "Edge", "Safari"]
        self.option_menu_variable1 = tk.StringVar(self)
        self.option_menu_variable1.set(options[0])
        tk.OptionMenu(self, self.option_menu_variable1, *options).pack(pady=(10, 0), anchor=tk.CENTER)
        tk.Button(self, text="Run", command=self.run, font=("Arial", 13)).pack(pady=(10, 0), anchor=tk.CENTER)
        self.label1 = tk.Label(self, font=P, fg="#ff0000")
        self.label1.pack(fill="x", pady=(10, 0))

    def get_spotify_data(self):
        URL = self.entry1.get()
        self.label1.config(text="")
        self.list1.delete(0, tk.END)
        self.data = []

        try:
           html_data = requests.get(URL)

        except:
            self.label1.config(text="Your URL is in a false format or doesn't exists")
            return -1

        bs_obj = BeautifulSoup(html_data.content, "html.parser")

        if "album" in URL:
            songs_data = bs_obj.findAll("span", class_="ListRowTitle__LineClamp-sc-1xe2if1-0 jjpOuK")
            artists_raw = bs_obj.findAll("span", class_="ListRowDetails__LineClamp-sc-sozu4l-0 hoTVKD")
            songs = [span.get_text() for span in songs_data]
            artists = [span.get_text() for span in artists_raw]
            for element in zip(songs, artists):
                self.data.append(element[0] + ", " + element[1])
                self.update_list(element[0] + ", " + element[1])
                self.update()


        elif "playlist" in URL:
            tracks = bs_obj.findAll("meta", attrs={'name': 'music:song'})
            for track in tracks:
                track_bs_obj = BeautifulSoup(requests.get(track.attrs['content']).content, "html.parser")
                title = track_bs_obj.find("meta", attrs={"name": "twitter:title"}).attrs["content"]
                autor = track_bs_obj.find("div", class_="Type__TypeElement-sc-goli3j-0 bkjCej t5WPFlGTY6GCd9UOFfLu").contents[0]
                self.data.append(title + ", " + str(autor))
                self.update_list(title + ", " + str(autor))
                self.update()


        else:
            self.label1.config(text="Your URL is not supported")
            return -1

        return 1

    def update_list(self, item):
        web_driver = None

        self.list1.insert(tk.END, item)

    def run(self):
        self.label1.config(text="")

        if not self.data:
            if not self.get_spotify_data():
                return

        try:
            if self.option_menu_variable1.get() == "Firefox":
                web_driver = webdriver.Firefox(options=WEB_DRIVER_OPTIONS)

            elif self.option_menu_variable1.get() == "Chrome":
                web_driver = webdriver.Chrome(options=WEB_DRIVER_OPTIONS)

            elif self.option_menu_variable1.get() == "Edge":
                web_driver = webdriver.Edge(options=WEB_DRIVER_OPTIONS)

            elif self.option_menu_variable1.get() == "Safari":
                web_driver = webdriver.Safari(options=WEB_DRIVER_OPTIONS)

            else:
                return -1

        except:
            self.label1.config(text="Your browser chosen browser cannot be found")
            return -1

        web_driver.get("https://forms.office.com/Pages/ResponsePage.aspx?id=-zoCyUIGEEGnTzadpOGehY6-j3zBNDhIie5s4gFi7bN"
                       "UNzhQRjBXRFRUUzdMOFYyNjRaS01ONTNKRy4u&origin=QRCode")

        try:
            button = WebDriverWait(web_driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div/div[2]/div/button")))
            button.click()
            c = 0

            for element in self.data:
                input = web_driver.find_element(By.XPATH,
                                            "/html/body/div/div/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2"
                                            "]/div/span/input")
                input.send_keys(element)

                button = WebDriverWait(web_driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/div[1]/div/div/div[3]/div/div/div[2]/div[2]/div/button")))
                button.click()

                button = WebDriverWait(web_driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/div[1]/div/div/div[3]/div/div/div[2]/div[2]/div[2]/a")))
                button.click()
                c += 1
                if c > 20:
                    break

        except:
            self.label1.config(text="There was an error while executing")
            return -1


if __name__ == "__main__":
    app = Window()
