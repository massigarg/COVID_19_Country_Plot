import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
import os

today = datetime.today().strftime("%d-%m-%Y")

# #Total Deaths
if not os.path.isfile(f"./total_deaths_{today}.csv"):
    urllib.request.urlretrieve("https://covid.ourworldindata.org/data/ecdc/total_deaths.csv",
                               f"total_deaths_{today}.csv")
df_total_deaths = pd.read_csv(f"total_deaths_{today}.csv", parse_dates=["date"])
df_total_deaths["date"] = pd.to_datetime(df_total_deaths["date"]).dt.strftime("%d-%m-%y")
df_total_deaths = df_total_deaths.fillna(0)

# #Total Confirmed Cases
if not os.path.isfile(f"./total_cases_{today}.csv"):
    urllib.request.urlretrieve("https://covid.ourworldindata.org/data/ecdc/total_cases.csv", f"total_cases_{today}.csv")
df_total_cases = pd.read_csv(f"total_cases_{today}.csv", parse_dates=["date"])
df_total_cases["date"] = pd.to_datetime(df_total_cases["date"]).dt.strftime("%d-%m-%y")
df_total_cases = df_total_cases.fillna(0)

# #New Confirmed Cases
if not os.path.isfile(f"./new_cases_{today}.csv"):
    urllib.request.urlretrieve("https://covid.ourworldindata.org/data/ecdc/new_cases.csv", f"new_cases_{today}.csv")
df_new_cases = pd.read_csv(f"new_cases_{today}.csv", parse_dates=["date"])
df_new_cases["date"] = pd.to_datetime(df_new_cases["date"]).dt.strftime("%d-%m-%y")
df_new_cases = df_new_cases.fillna(0)

def get_days():
    return df_total_deaths["date"]


def get_countries():
    countries = list(df_total_deaths.columns.values)
    return countries


def daily_death_increase():
    daily_increase = []
    for i in range(len(df_total_deaths[country])):
        if i == 0:
            daily_increase.append(df_total_deaths[country][i])
        else:
            daily_increase.append(df_total_deaths[country][i] - df_total_deaths[country][i - 1])
    return daily_increase


def top_coutries():
    df_top_10 = df_total_deaths.drop(labels=["date", "World"], axis=1)
    df_top_10.sort_values(by=len(df_top_10.idxmax(1))-1, axis=1, ascending=False, inplace=True)
    return list(df_top_10.columns)


def top_deaths():
    df_top_10 = df_total_deaths.drop(labels=["date", "World"], axis=1)
    df_top_10.sort_values(by=len(df_top_10.idxmax(1)) - 1, axis=1, ascending=False, inplace=True)
    return list(df_top_10.iloc[-1][1:])


def plot_figure():
    global country
    country=input("Choose a country: ")
    if country not in get_countries():
        return
    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(2, 2)

    # DEATHS PLOT
    ax1 = plt.subplot(gs[0, 0])
    ax1.set_title(f"Deats Trend for {country} @{today}")

    # Daily Increase Plot
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Daily Deaths Increase", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")

    ax1.bar(df_total_deaths["date"], daily_death_increase(), color="blue")

    ax1.set_xticklabels(df_total_deaths["date"], rotation="vertical")

    ax1 = ax1.twinx()

    # Total Deaths Plot
    ax1.set_ylabel("Total Deats", color="red")
    ax1.tick_params(axis='y', labelcolor="red")

    ax1.plot(df_total_deaths["date"], df_total_deaths[country], color="red", lw=2)

    ax1.set_xticklabels(df_total_deaths["date"], rotation="vertical")
    plt.xticks(np.arange(0, len(df_total_deaths["date"]), 3))

    # CASES PLOT
    ax2 = plt.subplot(gs[0, 1])
    ax2.set_title(f"Cases Trend for {country} @{today}")

    # New Cases
    ax2.set_xlabel("Days")
    ax2.set_ylabel("New Cases", color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")

    ax2.bar(get_days(), df_new_cases[country], color="blue")

    ax2.set_xticklabels(df_total_deaths["date"], rotation="vertical")

    ax2 = ax2.twinx()

    # Total Confirmed Cases
    ax2.set_ylabel("Total Confirmed Cases", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    ax2.plot(get_days(), df_total_cases[country], color="red", lw=2)

    ax2.set_xticklabels(df_total_deaths["date"], rotation="vertical")
    plt.xticks(np.arange(0, len(df_total_deaths["date"]), 3))

    # TOP 10
    ax3 = plt.subplot(gs[1, :])
    ax3.set_title("Top 10 Countries")
    ax3.set_ylabel("Total Deaths")

    ax3.bar(top_coutries()[:11], top_deaths()[:11], color="green")

    fig.tight_layout()

    plt.show()

plot_figure()
