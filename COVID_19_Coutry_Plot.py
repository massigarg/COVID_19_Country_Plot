import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
import seaborn as sns
import os

today = datetime.today().strftime("%d-%m-%Y")

# #Total Deaths
if not os.path.isfile(f"./total_deaths_{today}.csv"):
    urllib.request.urlretrieve("https://covid.ourworldindata.org/data/ecdc/total_deaths.csv",f"total_deaths_{today}.csv")

df_total_deaths = pd.read_csv(f"total_deaths_{today}.csv", parse_dates=["date"])
df_total_deaths["date"] = pd.to_datetime(df_total_deaths["date"]).dt.strftime("%b-%d")
df_total_deaths=df_total_deaths.fillna(method="bfill")[1:]

# #Total Confirmed Cases
if not os.path.isfile(f"./total_cases_{today}.csv"):
    urllib.request.urlretrieve("https://covid.ourworldindata.org/data/ecdc/total_cases.csv", f"total_cases_{today}.csv")

df_total_cases = pd.read_csv(f"total_cases_{today}.csv", parse_dates=["date"])
df_total_cases["date"] = pd.to_datetime(df_total_cases["date"]).dt.strftime("%b-%d")
df_total_cases.set_index("date")
df_total_cases = df_total_cases.fillna(method="bfill")[1:]

# #New Confirmed Cases
if not os.path.isfile(f"./new_cases_{today}.csv"):
    urllib.request.urlretrieve("https://covid.ourworldindata.org/data/ecdc/new_cases.csv", f"new_cases_{today}.csv")

df_new_cases = pd.read_csv(f"new_cases_{today}.csv", parse_dates=["date"])
df_new_cases["date"] = pd.to_datetime(df_new_cases["date"]).dt.strftime("%d-%m-%y")
df_new_cases.set_index("date")
df_new_cases = df_new_cases.fillna(method="bfill")[1:]

def get_days():
    return df_total_deaths["date"]

def get_countries():
    countries = list(df_total_deaths.columns.values)
    return countries


def daily_death_increase():
    daily_increase = []
    for i in range(len(df_total_deaths[country])):
        if i == 0:
            daily_increase.append(df_total_deaths[country].iloc[i])
        else:
            daily_increase.append(df_total_deaths[country].iloc[i] - df_total_deaths[country].iloc[i - 1])
    return daily_increase



def top_coutries():
    top_countries = df_total_deaths.drop(labels=["date", "World"], axis=1)
    top_countries.sort_values(by=len(top_countries.idxmax(1)), axis=1, ascending=False, inplace=True)
    return list(top_countries.columns)


def top_deaths():
    top_deaths = df_total_deaths.drop(labels=["date", "World"], axis=1)
    top_deaths.sort_values(by=len(top_deaths.idxmax(1)), axis=1, ascending=False, inplace=True)
    return list(top_deaths.iloc[-1])


def plot_figure():
    global country
    country="World"
    country=input("Choose a country: ")
    if country not in get_countries():
        return

    fig = plt.figure(figsize=(16, 9))
    fig.suptitle(f"Trends for {country} @{today}", fontsize=12, fontweight='bold', y=1)
    gs = fig.add_gridspec(2, 2)
    sns.set_style("whitegrid")

    # DEATHS PLOT
    ax1 = plt.subplot(gs[0, 0])
    ax1.set_title("Deaths Trend")

    # Daily Increase Plot
    ax1.set_ylabel("Daily Deaths Increase", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")

    sns.barplot(x=df_total_deaths["date"], y=daily_death_increase(), color="blue", ax=ax1)
    ax1.grid(False)

    ax1.set_xticklabels(labels=list(df_total_deaths["date"])[::5], rotation=45)
    plt.xticks(np.arange(0, len(df_total_deaths["date"]), 5))

    ax2 = ax1.twinx()

    # Total Deaths Plot
    ax2.set_ylabel("Total Deats", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    sns.lineplot(data=df_total_deaths[country], linewidth=2.5 , color="red",ax=ax2)

    ax1.set_xlabel("Date")

    # CASES PLOT
    ax3 = plt.subplot(gs[0, 1])
    ax3.set_title("Cases Trend")

    # New Cases
    ax3.tick_params(axis="y", labelcolor="blue")

    sns.barplot(x=get_days(), y=df_new_cases[country], color="blue", ax=ax3)
    ax3.grid(False)

    ax3.set_ylabel("New Cases", color="blue")

    ax3.set_xticklabels(labels=list(df_total_deaths["date"])[::5], rotation=45)
    plt.xticks(np.arange(0, len(df_total_deaths["date"]), 5))

    ax4 = ax3.twinx()

    # Total Confirmed Cases
    ax4.set_ylabel("Total Confirmed Cases", color="red")
    ax4.tick_params(axis='y', labelcolor="red")

    sns.lineplot(data=df_total_cases[country],linewidth=2.5, color="red", ax=ax4)

    ax3.set_xlabel("Date")

    # TOP 10
    ax5 = plt.subplot(gs[1, :])
    ax5.set_title("Top 10 Countries")
    ax5.set_ylabel("Total Deaths")

    sns.barplot(x=top_coutries()[:11], y=top_deaths()[:11], palette="rocket", ax=ax5)

    fig.tight_layout()

    plt.show()

plot_figure()


