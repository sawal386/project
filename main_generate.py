## This file is used generating the data


from helper import convert_raw_json
import json
from argparse import ArgumentParser

def parse_args():

    parser = ArgumentParser()
    parser.add_argument("--input_loc", required=True,
                        help="path to the folder containing the raw json files")
    parser.add_argument("--subject", required=True,
                        help="subject of interest")
    parser.add_argument("--year", required=True, type=int,
                        help="the year in which the article was published")
    parser.add_argument("--month", default=None, type=int,
                        help="the month in which the article was published")
    parser.add_argument("--output_loc", required=True,
                        help="the path to the folder where the output is saved")

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()
    #base_json = "/Users/sawal/Documents/stanford_ms_icme/courses/spring_24/cs224c/project/data"
    #subject = "medicine"
    #year = 2024
    #month = 1
    output_folder = "{}/{}".format(args.output_loc, args.subject)
    if args.month is None:
        name = "{}_{}".format(args.year, "all")
    else:
        name = "{}_{}".format(args.year, args.month)

    print("Generating data for subject: {}, year: {}, month:{}".format(args.subject,
                                                                    args.year, args.month))

    json_path = "{}/{}.json".format(args.input_loc, args.year)
    with open(json_path, "r") as f:
        raw_json = json.load(f)

    all_collection = convert_raw_json(raw_json)
    subj_collection = all_collection.get_articles_subject(args.subject)
    subj_time_collection = subj_collection.get_articles_time(args.year, args.month)
    subj_time_collection.assign_subject(args.subject)
    print("Final Size:", subj_time_collection.get_size())
    subj_time_collection.export_parquet(output_folder, name)








