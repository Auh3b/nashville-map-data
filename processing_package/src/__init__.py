import sys
from argparse import ArgumentParser
from processing import main


parser = ArgumentParser()

if __name__ == "__main__":
    parser.add_argument('input_path', type=str, help='The path to the file.')
    parser.add_argument('mapbox_token', type=str,
                        help='Mapbox token for geocoding processing')
    parser.add_argument('--output_path', type=str,
                        help='The location where the processed file should be exported to. If no path is given, the output will be exported to the same destination as the file path.')
    parser.add_argument('--input_format', choices=['xlsx', 'json', 'csv'], type=str,
                        help='The format of the input file. However the script will try to interpolate the format.')
    parser.add_argument('--output_format',  choices=['json', 'csv'], type=str,
                        help='The file format of the output file. If none is given, the format will default to JSON')

    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    mapbox_token = args.mapbox_token
    input_format = args.input_format
    output_format = args.output_format

    if (not bool(input_path)):
        print("Input path not found. Please provided the file path to the input.")
        sys.exit()
    if (not bool(mapbox_token)):
        print(
            "Mapbox token not found. Please provided Mapbox token for spatial processing.")
        sys.exit()

    main(input=input_path, mapbox_token=mapbox_token, output=output_path,
         input_format=input_format, output_format=output_format)
