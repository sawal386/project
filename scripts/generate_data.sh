#!/bin/bash

source scripts/settings.sh

for sub in "medicine"
do
    for year in 2021 2022 2023 2024
    do
        for month in 1 2 3 4 5 6 7 8 9 10 11 12
        do
            python main_generate.py \
                --input_loc ${BASE_JSON_DIR} \
                --subject $sub \
                --year $year \
                --output_loc ${OUTPUT_DATA_DIR} \
                --month $month 
        done
    done
done

    
    
