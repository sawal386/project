#!/bin/bash

source scripts/settings.sh

for sub in "medicine"
do
    for year in 2024
    do
        python main_generate.py \
            --input_loc ${BASE_JSON_DIR} \
            --subject $sub \
            --year $year \
            --output_loc ${OUTPUT_DATA_DIR}
    done
done

    
    
