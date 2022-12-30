import os
import queue
import threading
import time
from random import randint
from time import sleep


import pandas as pd
import plotille

art1 = '''
    ____             _             _                __  __    _         _____ __      
   / __ )___  ____ _(_)___  ____  (_)___  ____ _   / /_/ /_  (_)____   / __(_) /__  _ 
  / __  / _ \/ __ `/ / __ \/ __ \/ / __ \/ __ `/  / __/ __ \/ / ___/  / /_/ / / _ \(_)
 / /_/ /  __/ /_/ / / / / / / / / / / / / /_/ /  / /_/ / / / (__  )  / __/ / /  __/   
/_____/\___/\__, /_/_/ /_/_/ /_/_/_/ /_/\__, /   \__/_/ /_/_/____/  /_/ /_/_/\___(_)  
           /____/                      /____/                                         
'''

art2 = '''
    __  ___      __                                           ____              __  __    _         _____ __      
   / / / (_)____/ /_____  ____ __________ _____ ___  _____   / __/___  _____   / /_/ /_  (_)____   / __(_) /__  _ 
  / /_/ / / ___/ __/ __ \/ __ `/ ___/ __ `/ __ `__ \/ ___/  / /_/ __ \/ ___/  / __/ __ \/ / ___/  / /_/ / / _ \(_)
 / __  / (__  ) /_/ /_/ / /_/ / /  / /_/ / / / / / (__  )  / __/ /_/ / /     / /_/ / / / (__  )  / __/ / /  __/   
/_/ /_/_/____/\__/\____/\__, /_/   \__,_/_/ /_/ /_/____/  /_/  \____/_/      \__/_/ /_/_/____/  /_/ /_/_/\___(_)  
                       /____/                                                                                     
'''


art3 = '''
                                                       
,---.     |                       ,   .                
|    ,---.|    .   .,-.-.,---.    |\  |,---.,-.-.,---.o
|    |   ||    |   || | ||   |    | \ |,---|| | ||---' 
`---'`---'`---'`---'` ' '`   '    `  `'`---^` ' '`---'o
                                                       
'''

art4 = '''
                                                                                                                            
,---.                                       |         |             ,---.              |    |    o         ,---.o|          
`---..   .,-.-.,-.-.,---.,---.,   .    ,---.|--- ,---.|--- ,---.    |__. ,---.,---.    |--- |---..,---.    |__. .|    ,---.o
    ||   || | || | |,---||    |   |    `---.|    ,---||    `---.    |    |   ||        |    |   ||`---.    |    ||    |---' 
`---'`---'` ' '` ' '`---^`    `---|    `---'`---'`---^`---'`---'    `    `---'`        `---'`   '``---'    `    ``---'`---'o
                              `---'                                                                                         
'''

def process_csv(q, output_file):
    # Process CSV files until the queue is empty
    while not q.empty():
        # Get the next CSV file to process
        file_path = q.get()

        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)
        sleep(randint(1,19))
        # Print summary statistics for the DataFrame
        print(art1)
        print('-'*45)
        print(file_path)
        print('-'*45)
        print(art4)
        print('-'*45)
        print(df.describe())
        print('-'*45)
        print(art2)
        # Create a histogram for each column in the DataFrame
        for column in df.columns:
            fig = plotille.Figure()
            fig.histogram(df[column])
            print('-'*45)
            print(art3)
            print(column + ' from this file:' + file_path)
            print('-'*45)
            print('-'*45)
            print(fig.show())
            print('-'*45)
            print('-'*45)
        # Append the summary statistics and histograms to the output file
        with open(output_file, 'a') as f:
            f.write(str(df.describe()))
            for column in df.columns:
                print('-'*45)
                print('-'*45)
                fig = plotille.Figure()
                fig.histogram(df[column])
                f.write(fig.show())
                print('-'*45)
                print('-'*45)

        # Mark the task as done
        q.task_done()

def main():
    # Create a queue to store the CSV file paths
    q = queue.Queue()
    filename = str(input('Input the path to your directory of csv files. End with "/"'))
    # Add the CSV file paths to the queue
    for file_name in os.listdir(filename):
        if file_name.endswith('.csv'):
            q.put(filename + file_name)

    # Create a list of worker threads
    threads = []
    for i in range(4):
        t = threading.Thread(target=process_csv, args=(q, 'output.txt'))
        t.start()
        threads.append(t)

    # Wait for all tasks to be completed
    q.join()

if __name__ == '__main__':
    main()
