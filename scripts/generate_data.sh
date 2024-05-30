#!/bin/bash

source scripts/settings.sh

for sub in "education"
do
    for year in 2021
    do
        python main_generate.py \
            --input_loc ${BASE_JSON_DIR} \
            --subject $sub \
            --year $year \
            --output_loc ${OUTPUT_DATA_DIR}
    done
done

    
    
