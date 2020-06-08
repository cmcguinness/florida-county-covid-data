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
    total_pos_up = 0
    total_death_up = 0
    total_pos_down = 0
    total_death_down = 0
    non_zero_was_zero_pos = 0
    non_zero_was_zero_death = 0
    zero_was_non_zero_pos = 0
    zero_was_non_zero_death = 0

    files = []
    dates = []
    for fname in os.listdir('data/'):
        if fname[0:4] != '2020':
            continue
        files.append(fname)
        dates.append(fname[:11])

    files.sort()
    dates.sort()
    dates = np.array(dates)
    # Weed out dates from the array so that the plot isn't so dense
    sparseness = 2
    for i in range(sparseness - 1):
        dates[len(dates) - (i + 2)::-sparseness] = ""

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
            last_data = frames[0].loc[counties[i]][metric_index]

            for df in frames:
                new_data = df.loc[counties[i]][metric_index]
                data.append(max(0,new_data - last_data))
                last_data = new_data

            linedata = data[1:]

            cumulative = 0

            for k in range(1,8):
                cumulative += data[k]
                linedata[k-1] = cumulative / k

            for k in range(8, len(data)):
                cumulative -= data[k-7]
                cumulative += data[k]
                linedata[k-1] = cumulative / 7

            plt.bar(xs[1:], data[1:], color='#CfCfff')
            plt.plot(xs[1:], linedata, color='r')

            if linedata[-1] > 1+linedata[-8]:
                if metric_names[j] == "Deaths":
                    total_death_up += 1
                else:
                    total_pos_up += 1

            if linedata[-1]+1 < linedata[-8]:
                if metric_names[j] == "Deaths":
                    total_death_down += 1
                else:
                    total_pos_down += 1


            if linedata[-1] > 1 and linedata[-8] < 1:
                if metric_names[j] == "Deaths":
                    non_zero_was_zero_death += 1
                else:
                    non_zero_was_zero_pos += 1

            if linedata[-1] < 1 and linedata[-8] > 1:
                if metric_names[j] == "Deaths":
                    zero_was_non_zero_death += 1
                else:
                    zero_was_non_zero_pos += 1

            bottom, top = plt.ylim()  # return the current ylim
            bottom = max(0, bottom)
            top = max(8,top)
            plt.ylim(bottom,top)
            plt.xticks(xs[1:],dates[1:],rotation=45)
            plt.title('Daily C19 '+metric_name+' in '+counties[i]+' County FL')
            plt.tight_layout()

        ts = datetime.datetime.now().strftime("%Y-%m-%d")

        plt.suptitle("COVID-19 " + metric_name + " for Florida's Counties on "+ts, fontsize=24)
        plt.figtext(0.5, 0.04, "Blue Bars = Daily Change, Red Line = 7 day trailing average (mean)", ha="center",
                    fontsize=16)
        plt.figtext(0.5, 0.03, "Not All Counties using same Y Scale !", ha="center",
                    fontsize=16)
        plt.figtext(0.5, 0.02, "Chart prepared by Charles McGuinness @socialseercom using data from State of Florida DOH", ha="center",
                    fontsize=16)
        fig.subplots_adjust(top=0.95, bottom=0.05)

        plt.savefig('images/' + ts + '-county-'+metric_name+'.png', dpi=150)

    print('# counties with increase in positives', total_pos_up)
    print('# counties with increase in deaths', total_death_up)
    print('# counties with decrease in positives', total_pos_down)
    print('# counties with decrease in deaths', total_death_down)
    print('# counties > 1 positive but < 1 a week ago', non_zero_was_zero_pos)
    print('# counties > 1 death but < 1 a week ago', non_zero_was_zero_death)
    print('# counties < 1 positive but > 1 a week ago', zero_was_non_zero_pos)
    print('# counties < 1 death but > 1 a week ago', zero_was_non_zero_death)
