"""
Get a snapshot of the county by county COVID-19 stats for Florida
"""
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json
import pandas as pd
import os

counties = ["GILCHRIST", "PUTNAM", "TAYLOR", "OKALOOSA", "CALHOUN", "PALM BEACH", "ST. LUCIE", "PASCO", "GADSDEN", "LEON", "JEFFERSON", "MADISON", "LIBERTY", "HAMILTON", "BAY", "COLUMBIA", "BAKER", "HOLMES", "MARTIN", "HILLSBOROUGH", "MANATEE", "CLAY", "HARDEE", "MARION", "VOLUSIA", "DIXIE", "LAKE", "LEVY", "SUMTER", "SEMINOLE", "ORANGE", "CITRUS", "HERNANDO", "PINELLAS", "SUWANNEE", "DUVAL", "LAFAYETTE", "GULF", "UNION", "BRADFORD", "WAKULLA", "BREVARD", "POLK", "OSCEOLA", "HIGHLANDS", "LEE", "COLLIER", "DADE", "MONROE", "SANTA ROSA", "WALTON", "JACKSON", "WASHINGTON", "NASSAU", "GLADES", "CHARLOTTE", "SARASOTA", "DESOTO", "FLAGLER", "HENDRY", "INDIAN RIVER", "BROWARD", "ESCAMBIA", "OKEECHOBEE", "FRANKLIN", "ALACHUA", "ST. JOHNS", "Unknown"]

counties.sort()

if __name__ == '__main__':
    files = []
    dates = []
    for fname in os.listdir('data/'):
        if fname[0:4] != '2020':
            continue
        files.append(fname)
        dates.append(fname[:11])

    files.sort()
    dates.sort()
    # pandas.read_csv

    frames = []

    for fname in files:
        pdf = pd.read_csv('data/' + fname, index_col="COUNTYNAME")
        frames.append(pdf)

    metric_names = ["Positives", "Deaths"]
    metric_indexes = ["TPositive", "Deaths"]

    for j in range(len(metric_names)):
        print("Generating " + metric_names[j])
        metric_name = metric_names[j]
        metric_index = metric_indexes[j]

        xs = range(len(frames))

        fig = plt.figure(figsize=(20,45.5))

        rows = int(len(counties) / 4) + 1

        for i in range(len(counties)):

            plt.subplot(rows, 4, i+1)

            data = []
            for df in frames:
                data.append(df.loc[counties[i]][metric_index])

            plt.plot(xs, data, color='#CfCfff')
            plt.xticks(xs,dates,rotation=45)
            plt.title('Daily C19 '+metric_name+' in '+counties[i]+' County FL')
            plt.tight_layout()

        ts = datetime.datetime.now().strftime("%Y-%m-%d")

        plt.suptitle("COVID-19 " + metric_name + " for Florida's Counties on "+ts, fontsize=24)
        plt.figtext(0.5, 0.02, "Chart prepared by Charles McGuinness @socialseercom using data from covidtracking.com", ha="center",
                    fontsize=16)
        fig.subplots_adjust(top=0.95, bottom=0.05)

        plt.savefig('images/' + ts + '-county-'+metric_name+'.png', dpi=150)
