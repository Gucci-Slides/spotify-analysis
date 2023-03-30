import os
import boto3
import datetime
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Connect to AWS Systems Manager Parameter Store
ssm = boto3.client('ssm')

# Retrieve Spotify API credentials from AWS SSM
SPOTIPY_CLIENT_SECRET = ssm.get_parameter(Name='API_KEY', WithDecryption=True)[
    'Parameter']['Value']
SPOTIPY_CLIENT_ID = ssm.get_parameter(Name='API_URL')['Parameter']['Value']


# Connect to the Spotify API
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def lambda_handler(event, context):

    # Define a list of playlist URIs to ingest
    playlist_uris = ['spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',
                     'spotify:playlist:37i9dQZF1DX9D5dmCM8Lo3', 'spotify:playlist:0IEOIvZvbPFmVLnTBjpEkC']

    for uri in playlist_uris:
        # Retrieve tracks for the playlist
        query = sp.playlist_tracks(uri)
        response = json.dumps(query)

        # Construct the S3 bucket key
        my_date = datetime.datetime.now()
        my_string = my_date.strftime('%Y-%m-%d')
        playlist_name = sp.playlist(uri)['name']
        key = f'data/playlist_database/playlist_json/{playlist_name}/dataload={my_string}/{playlist_name}.json'

        # Upload the JSON object to S3
        s3_client = boto3.client('s3')
        bucket_name = os.environ('BUCKET_NAME')

        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=response)

    return {
        'statusCode': 200,
        'body': json.dumps("JSON objects uploaded to S3")
    }
