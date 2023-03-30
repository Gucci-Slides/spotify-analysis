# Spotify Playlist Analysis with AWS Lambda and S3
This project provides a solution for ingesting Spotify playlist data using AWS Lambda and storing the data in S3. The solution includes two lambda functions: one for ingesting data from Spotify, and one for converting the data to CSV format and storing it in S3.

![image](https://user-images.githubusercontent.com/23535221/227681636-ddd5712a-f60d-4cec-9986-1da40585835c.png)



## Dependencies and Installations
This project requires the following dependencies:

- `boto3`
- `spotipy`

To install these dependencies, you can use pip:

```
pip install boto3 spotipy
```
## Workflow
1. **EventBridge Trigger** is scheduled every week to invoke **spotify_data_ingestion.py**
2. **Data Ingestion Lambda** is invokes and queries Spotify API for the playlist URIs. A JSON object is returned.
3. **Data Ingestion Lambda** sends the JSON object to S3. 
4. **Data Transformation Lambda** converts JSON object into CSV and puts the new object back into S3.

## Lambda Functions
### Spotify Data Ingestion
The first lambda function, **spotify_data_ingestion.py** , connects to the Spotify API using `spotipy` and retrieves playlist data for a specific playlist. The function then uploads the JSON data to an S3 bucket.

### JSON to CSV Conversion
The second lambda function, json_to_csv.py, retrieves the JSON data from S3 and converts it to CSV format. The function then uploads the CSV data to an S3 bucket.

## S3 Key Structure
The S3 key structure for the JSON and CSV files follows a specific pattern to allow for easy organization and retrieval of the data. The key is composed of multiple subdirectories separated by forward slashes. Here's an example:

```
data/playlist_database/playlist_json/rap_caviar/dataload=2023-03-24/rap_caviar.json
```

In this example, the S3 key consists of the following subdirectories:

- `data`: The top-level directory for the project
- `playlist_database`: A subdirectory for playlist data
- `playlist_json`: A subdirectory for JSON data
- `rap_caviar`: The name of the playlist
- `dataload=2023-03-24`: The date when the data was ingested
- `rap_caviar.json`: The name of the JSON file

This structure allows you to easily identify the playlist and the date when the data was ingested. The CSV file structure follows a similar pattern, with the playlist_csv subdirectory replacing playlist_json.

Overall, this structure allows for easy organization and retrieval of playlist data in S3, which is important when dealing with large amounts of data.

## Setting Up and Testing the Lambda Functions
To set up the lambda functions, follow these steps:
1. Clone the repository to your local machine using the following command:
```
git clone https://github.com/your-username/spotify-lambda-s3.git
```

2. Install the dependencies using pip:
```
pip install boto3 spotipy
```

3. Open spotify_data_ingestion.py and replace my-s3-bucket with the name of your S3 bucket.

4. Open json_to_csv.py and replace my-s3-bucket with the name of your S3 bucket.

5. Zip both files into separate packages and upload them to AWS Lambda.

6. In AWS Lambda, create a new trigger for the spotify_data_ingestion function to run on a schedule, such as daily.

7. Test the spotify_data_ingestion function by manually invoking it and checking if the JSON data is uploaded to your S3 bucket.

8. Test the json_to_csv function by manually invoking it and checking if the CSV data is uploaded to your S3 bucket.

9. Schedule the json_to_csv function to run on a regular interval, such as hourly, to ensure that new data is converted to CSV format and uploaded to your S3 bucket.

That's it! You should now have a fully functional solution for ingesting and analyzing Spotify playlist data using AWS Lambda and S3.

## Event Test Payloads

### Example Test Event Payload for spotify_data_ingestion
```
{
  "key": "data/playlist_database/playlist_json/rap_caviar/dataload=2023-03-24/rap_caviar.json"
}
```
### Example Test Event Payload for json_to_csv
```
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "my-s3-bucket"
        },
        "object": {
          "key": "data/playlist_database/playlist_json/rap_caviar/dataload=2023-03-24/rap_caviar.json"
        }
      }
    }
  ]
}
```

These test event payloads can be used to manually test the lambda functions in the AWS Lambda console. Simply copy and paste the payload into the console and click "Test" to test the function.


## Troubleshooting Tips and Common Errors
### S3 Bucket Permissions
Make sure that the IAM role associated with your lambda function has the necessary permissions to access your S3 bucket. If you encounter errors related to S3 permissions, check your IAM role settings and make sure that the role has the necessary permissions.

## Lambda Function Configuration
Double-check that your lambda function configuration is correct, including the function code, function handler, and function trigger. If any of these settings are incorrect, the function may fail to execute or may not execute as intended.

## Spotipy API Credentials
Make sure that you have entered your Spotipy API credentials correctly in the spotify_data_ingestion.py file. If your API credentials are incorrect or invalid, the function will fail to connect to the Spotipy API and will not be able to retrieve playlist data.

## Invalid JSON Data
If you encounter errors related to invalid JSON data, make sure that the JSON data being uploaded to your S3 bucket is valid and properly formatted. Invalid JSON data may cause the json_to_csv function to fail or produce incorrect results.

## Incorrect S3 Key Structure
Make sure that the S3 key structure for your JSON and CSV data follows the correct pattern, as described in the README file. If the key structure is incorrect, the lambda functions may not be able to access or write to the correct S3 objects.

## AWS Lambda and S3 Region Mismatch
Make sure that your AWS Lambda and S3 bucket are located in the same region. If the lambda function and S3 bucket are located in different regions, the function may fail to access or write to the S3 bucket.

These are just a few common errors that you may encounter when setting up and using the lambda functions. If you encounter other errors or issues, refer to the AWS Lambda and S3 documentation, or consult the AWS support team for assistance.

