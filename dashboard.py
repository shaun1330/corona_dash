from coronavirus_scraper import corona_scraper
import tkinter as tk
import datetime


class dashboard(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.count = 0
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.geometry('400x120+700+0')

        self.country_label = tk.Label(self, text='Country:')
        self.country_label.grid(row=0, column=0)

        self.corona_stats = corona_scraper()
        self.countries = self.corona_stats.get_countries()

        self.refresh_button = tk.Button(self, text=u"\U0001F5D8", command=self.refresh, font='courier 20 bold')
        self.refresh_button.grid(row=0, column=2)

        #
        self.country_selection = tk.StringVar(self)
        self.country_selection.set("World")
        self.country_dropdown = tk.OptionMenu(self, self.country_selection, *self.countries)
        self.country_dropdown.grid(row=0, column=1)

        # draw headings
        self.total_cases_label = tk.Label(self, text='Total')
        self.total_cases_label.grid(row=1, column=0)
        self.total_deaths_label = tk.Label(self, text="Deaths")
        self.total_deaths_label.grid(row=1, column=1)
        self.serious_label = tk.Label(self, text='Serious')
        self.serious_label.grid(row=1, column=2)

        # draw numbers (World by default)
        self.draw_numbers('World')
        self.country_selection.trace('w', self.country_selector)

        # start updater loop
        self.periodic_update()

    def draw_numbers(self, country):
        font = "courier 15 bold"
        new_cases = self.corona_stats.get_country_stats(country)[1]
        if new_cases != 0:
            new_cases = int(new_cases.replace(",",''))
            cases_text = self.corona_stats.get_country_stats(country)[0] + "\n(+" + str(new_cases) + ")"
        else:
            cases_text = self.corona_stats.get_country_stats(country)[0]

        self.total_cases = tk.Label(self, text=cases_text, font=font)
        self.total_cases.grid(row=2, column=0)

        new_deaths = self.corona_stats.get_country_stats(country)[3]
        if new_deaths != 0:
            new_deaths = int(new_deaths.replace(",",''))
            death_text = self.corona_stats.get_country_stats(country)[2] + "\n(+" + str(new_deaths) + ")"
        else:
            death_text = self.corona_stats.get_country_stats(country)[2]
        self.total_deaths = tk.Label(self, text=death_text, font=font)
        self.total_deaths.grid(row=2, column=1)

        self.serious = tk.Label(self, text=self.corona_stats.get_country_stats(country)[6], font=font)
        self.serious.grid(row=2, column=2)

        self.refreshed_datetime = datetime.datetime.utcnow().strftime("%d-%m-%y %H:%M:%S UTC")
        self.refreshed_datetime_label = tk.Label(self, text=self.refreshed_datetime, font='courier 10 italic')
        self.refreshed_datetime_label.grid(row=3, column=1)

    def periodic_update(self):
        self.count += 1
        if self.count == 600:
            self.refresh()
            self.count = 0
        self.after(1000, self.periodic_update)  # update every 10 minutes

    def country_selector(self, *args):
        # get new country
        selected_country = self.country_selection.get()
        # remove old numbers
        self.total_cases.grid_forget()
        self.total_deaths.grid_forget()
        self.serious.grid_forget()
        # add new numbers for that country
        self.draw_numbers(selected_country)

    def refresh(self):
        selected_country = self.country_selection.get()
        self.corona_stats = corona_scraper()
        self.countries = self.corona_stats.get_countries()
        self.total_cases.grid_forget()
        self.total_deaths.grid_forget()
        self.serious.grid_forget()
        self.draw_numbers(selected_country)


if __name__ == '__main__':
    app = dashboard()
    app.mainloop()