This repository describes on how to run the full pipeline. Step 3 is the most time consuming. You need to run it only once to generate the data of interest. 

1. Clone the repository 

   git clone 
2. cd into the directory 
    
    cd project 

3. The first step is to tokenize the data and store it as parquet file. Open scripts/settings.sh and check if the directories are correct. Also go over generate_data.sh. 
    
    bash scripts/generate_data.sh 

The source data for this is the raw json file containing the information about all the articles. I am assuming the file is name as "{year}.json". If possible, follow this convention. Otherwise, you will have to make modifications in main_generate.py. The outputs are automatically saved in the path "inference_data/{subject}/{year}_{month}.parquet". Additionally, there is also an accompanying text file "inference_data/{subject}/meta_{year}_{month}.csv". This is meant to a metadata file. As of now it contains information about the sentence and source article id. 

Note that this takes sometime to complete.

4. Now that we have created the inference data, we will run the actual inference. Before this check the script run_inference.sh in the folder scripts. Make sure the paths are correct. Next run,

    bash scripts/run_inference.sh 

This script will run the main_analysis.py. The inputs to this are the parquet files containing the distribution. In the current version, the file can be accessed via "project/data/distribution/distribution.parquet". The other input file is location to the folder containing inference data distribution obtained from step 3. The program will automatically loop through the files in the folder and use the relevant parquet files to estimate alpha. The final output is saved to output/{subject_name}_{year}.csv

 

