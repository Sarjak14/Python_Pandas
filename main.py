import pandas as pd
import matplotlib.pyplot as py
import tkinter as tk
from tkinter import ttk


class covid_data_analysis:
    def __init__(this, link, title):
        this.title = title
        this.link = link
        this.data = pd.read_csv(this.link)
        if "Confirmed" in this.data.columns:
            this.total_cases = this.data["Confirmed"].sum()
            this.total_deaths = this.data["Deaths"].sum()
            this.total_recovered = this.data["Recovered"].sum()
            this.total_active = this.data["Active"].sum()
        elif "TotalCases" in this.data.columns:
            this.total_cases = this.data["TotalCases"].sum()
            this.total_deaths = this.data["TotalDeaths"].sum()
            this.total_recovered = this.data["TotalRecovered"].sum()
            this.total_active = this.data["ActiveCases"].sum()
        else:
            print("Error: Column names do not match expected values.")
        this.total_life_affairs = [
            this.total_recovered,
            this.total_deaths,
            this.total_active,
        ]
        global root
        global cl
        root = tk.Tk()
        root.geometry("1500x1500")
        root.title(this.title)
        style = ttk.Style(root)
        style.configure("TButton", font=("calibri", 20, "bold"), borderwidth="4")
        pie = ttk.Button(
            root, text="Pie Chart", command=lambda: this.show_pie_chart()
        )
        pie.pack(pady=10)
        options_list=(this.data.columns.append(pd.Index(['All'])))
        variable = tk.StringVar(root)
        variable.set('Select required Columns')
        temp=ttk.Label(root,text="please select that you want to view and click View Data")
        temp.pack(pady=10)
        cl=ttk.OptionMenu(root,variable, *options_list)
        cl.pack(pady=10)
        vd = ttk.Button(root, text="View Data", command=lambda: this.print_data(variable))
        vd.pack(pady=10)
        dd = ttk.Button(root, text="Info", command=lambda: [this.description()])
        dd.pack(pady=10)
        dp = ttk.Button(root, text="Describe", command=lambda: this.calculate_info())
        dp.pack(pady=10)
        clr = ttk.Button(
            root,
            text="Clear",
            command=lambda: covid_data_analysis(this.link, this.title),
        )
        clr.pack(pady=10)
        root.mainloop()

    def show_pie_chart(this):
        py.pie(
            this.total_life_affairs,
            labels=["Total Recovered", "Total Dead", "Total Active"],
            colors=["green", "red", "yellow"],
        )
        py.title("Health Condition of the Infected")
        py.show()

    def print_data(this,variable):
        global root
        global data_display
        id=variable.get()
        print(id)
        data_display = tk.Text(root, height=50, width=200)
        if id=='All':
         try:
            data_display.delete("START", "END")
         except:
            data_display.insert("0.0", this.data.head(100).to_string())
            data_display.pack()
        else:
            data_display.insert("0.0", this.data[id])    
            data_display.pack()


    def description(this):
        global root
        global data_display
        try:
            data_display.delete("START", "END")
        except:
            data_display = tk.Text(root, height=50, width=200)
            data_display.insert("0.0", this.data.describe().to_string())
            data_display.pack()

    def calculate_info(this):
        global root
        global info_display
        hd, hr, ha = 0, 0, 0
        highest_death, highest_active, highest_recovered = None, None, None
        if "Confirmed" in this.data.columns:
            this.total_cases = this.data["Confirmed"].sum()
            this.total_deaths = this.data["Deaths"].sum()
            this.total_recovered = this.data["Recovered"].sum()
            this.total_active = this.data["Active"].sum()
            for i in range(len(this.data)):
                if this.data.loc[i, "Deaths"] > hd:
                    hd = this.data.loc[i, "Deaths"]
                    highest_death = this.data.loc[i]
                if this.data.loc[i, "Active"] > ha:
                    ha = this.data.loc[i, "Active"]
                    highest_active = this.data.loc[i]
                if this.data.loc[i, "Recovered"] > hr:
                    hr = this.data.loc[i, "Recovered"]
                    highest_recovered = this.data.loc[i]
        elif "TotalCases" in this.data.columns:
            this.total_cases = this.data["TotalCases"].sum()
            this.total_deaths = this.data["TotalDeaths"].sum()
            this.total_recovered = this.data["TotalRecovered"].sum()
            this.total_active = this.data["ActiveCases"].sum()
            for i in range(len(this.data)):
                if this.data.loc[i, "TotalDeaths"] > hd:
                    hd = this.data.loc[i, "TotalDeaths"]
                    highest_death = this.data.loc[i]
                if this.data.loc[i, "ActiveCases"] > ha:
                    ha = this.data.loc[i, "ActiveCases"]
                    highest_active = this.data.loc[i]
                if this.data.loc[i, "TotalRecovered"] > hr:
                    hr = this.data.loc[i, "TotalRecovered"]
                    highest_recovered = this.data.loc[i]

        death_rate = (this.total_deaths / this.total_cases) * 100
        recovery_rate = (this.total_recovered / this.total_cases) * 100
        info_paragraph = (
            f"The total number of confirmed cases is {this.total_cases}.\n "
            f"The total number of deaths is {this.total_deaths}.\n "
            f"The total number of recovered cases is {this.total_recovered}.\n "
            f"The total number of active cases is {this.total_active}.\n"
            f"The death rate is {death_rate:.2f}%.\n"
            f"The recovery rate is {recovery_rate:.2f}%.\n"
            f"\nThe Data with highest Death Is :\n"
            f"{highest_death}\n"
            f"The Data with highest Active Is :\n"
            f"{highest_active}\n"
            f"The Data with highest Recovered Is :\n"
            f"{highest_recovered}\n"
        )
        if "Date" in this.data.columns:
            print(this.title)
            info_paragraph += (
                f"Maximum people died {highest_death['Deaths']} in date {highest_death['Date']}\n"
                f"Maximum people active {highest_active['Active']} in date {highest_active['Date']}\n"
                f"Maximum people REcovered {highest_recovered['Recovered']} in date {highest_recovered['Date']}\n"
            )
            print(info_paragraph)
        try:
            info_display.delete("1.0", "end")
        except:
            info_display = tk.Text(root, height=50, width=200)
            info_display.insert("1.0", info_paragraph)
            info_display.pack()


def covid_data_analysis_call():
    a = covid_data_analysis("country_wise_latest.csv", "Country_Wise_latest")


def day_wise_data_analysis_call():
    b = covid_data_analysis("day_wise.csv", "Day_wise_latest")


def clean_complete_analysis_call():
    c = covid_data_analysis("covid_19_clean_complete.csv", "Covid_19_clean_Complete")


def full_grouped_analysic_call():
    d = covid_data_analysis("full_grouped.csv", "Full_Grouped")


def worldometer_data_call():
    e = covid_data_analysis("worldometer_data.csv", "Worldometer_Data")


pd.set_option("display.max_rows", None)
main = tk.Tk()
main.title("Sarjak_Covid_Data_Analysis_Tool")
main.geometry("380x380")
style = ttk.Style(main)
style.configure("TButton", font=("calibri", 20, "bold"), borderwidth="4")
Prompt_text = tk.ttk.Label(
    main, text="Select the data for view:\n", font=["calibri", 14]
)
Prompt_text.pack()
contents = ttk.Button(
    main, text="Covid Data", command=lambda: covid_data_analysis_call()
)
contents.pack(pady=10)
contents = ttk.Button(
    main, text="Day_Wise", command=lambda: day_wise_data_analysis_call()
)
contents.pack(pady=10)
contents = ttk.Button(
    main, text="Clean Analysis", command=lambda: clean_complete_analysis_call()
)
contents.pack(pady=10)
contents = ttk.Button(
    main, text="Full Grouped", command=lambda: full_grouped_analysic_call()
)
contents.pack(pady=10)
contents = ttk.Button(
    main, text="Worldometer", command=lambda: worldometer_data_call()
)
contents.pack(pady=10)
main.mainloop()
