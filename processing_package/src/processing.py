import requests
import os
from pandas import read_csv, read_json, read_excel, DataFrame
from geojson import FeatureCollection
import sys
import uuid


def mapboxGeocode(params: dict = {}):
    baseUrl = "https://api.mapbox.com/search/geocode/v6/forward"
    req = requests.get(baseUrl, params=params)
    return req.json()


def getGeocodeCoordinates(result: FeatureCollection):
    return ",".join(([str(x) for x in result['features'][0]["geometry"]["coordinates"]]))


def getAddressCoordinates(address, MAPBOX_TOKEN):
    mapbox_query = {
        "q": address,
        "access_token": MAPBOX_TOKEN,
        "country": 'US'
    }
    geocode_results = mapboxGeocode(mapbox_query)
    string_coordinates = getGeocodeCoordinates(geocode_results)
    return string_coordinates


def processAddresses(df: DataFrame, mapbox_token):
    df['coordinates'] = df["address"].apply(
        lambda x: getAddressCoordinates(x, mapbox_token))
    df['longitude'] = df["coordinates"].apply(lambda x: float(x.split(",")[0]))
    df['latitude'] = df["coordinates"].apply(lambda x: float(x.split(",")[1]))
    return df


def generateUniqueId():
    return str(uuid.uuid4())


def getImportFileType(file: str):
    root, ext = os.path.splitext(file)
    return ext[1:]


def getDataframeReader(ext: str):
    readerDict = {
        'xlsx': read_excel,
        'csv': read_csv,
        'json': read_json
    }
    return readerDict[ext]


def fileToDataframe(input: str, ext: str) -> DataFrame:
    try:
        reader = getDataframeReader(ext)
        return reader(input)
    except:
        print("Input file not in right format. Allowed formats are xlsx, csv, json")
        sys.exit()


def exportDataFrameToFile(df: DataFrame, ext: str, output: str):
    if (ext == 'csv'):
        output_path = output + ".csv"
        df.to_csv(output_path)
        print(f"Output export to {output_path}")
        return
    if (ext == 'json'):
        output_path = output + ".json"
        df.to_json(output_path, orient='records')
        print(f"Output export to {output_path}")
        return


def process_columns(df: DataFrame):
    columns = df.columns
    new_cols = [str(x).lower().replace(" ", "_") for x in columns]
    df.columns = new_cols
    return df


def main(input: str, mapbox_token: str, output: str = "", input_format="", output_format=""):
    ext = input_format

    print("input: ", input)
    print("output: ", output)
    print("input format: ", input_format)
    print("output format: ", output_format)

    if (not ext):
        ext = getImportFileType(input)

    df = fileToDataframe(input, ext)
    df = process_columns(df)
    df = processAddresses(df, mapbox_token)

    output_path = os.path.splitext(output)[0]

    if (not output_path):
        output_path = os.path.splitext(input)[0]

    out_ext = output_format
    if (not out_ext):
        out_ext = ext

    exportDataFrameToFile(df, out_ext, output_path)
