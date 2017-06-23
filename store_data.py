from google.cloud import datastore
from google.cloud import storage
import datetime

# import numpy as np
# import pickle
# import os
# import cv2
# import sys

# # Establish cloud credientials
# home_path = os.path.expanduser('~')
# auth_path = "/Documents/Sentient-CNC/SentientCNC-3c8c6f014588.json"
# auth_file_path = home_path + auth_path

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_file_path


# # Imports the Google Cloud client library
# from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()

# The name for the new bucket
bucket_name = 'my-new-bucket'

# Creates the new bucket
bucket = storage_client.create_bucket(bucket_name)

print('Bucket {} created.'.format(bucket.name))


class data_handler():
    """
    Object designed to handle storage of incoming sensor data.

    How to use:
        Initialize the handler object, then use the .write function
        to push the sensor data to the cloud storage. Sensor data should
        be packaged as a dictionary of values.

    Args:
    project_id: string
        Project ID per Google Cloud's project ID (see Cloud Console)
    sensor_node: string
        Identifier for sensor gateway. This is used as a primary key for
        storing data entries (so data can be viewed per device)
    """

    def __init__(self,
                 project_id='sentientcnc-1',
                 sensor_node='CNCmill_001'):

        # Creates an authorized service object to make authenticated
        # requests to Google Cloud API using the API's client libraries.
        self.sensor_node = sensor_node
        self.client = datastore.Client(project_id)

    def write(self, sensor_data, timestamp=None):
        """
        writes the sensor data to the cloud storage

        Args:
        sensor_data: dict
            dictionary of sensor nodes as keys and data as parameters
        timestamp: string
            timestamp of when the data was recorded
        """

        # Create key for timestamp
        if not timestamp:
            timestamp = str(datetime.datetime.now())

        data_snapshot = self.client.key(self.sensor_node, timestamp)

        # Create the database entity (equivalent to a row entry in a table)
        entry = datastore.Entity(data_snapshot)
        entry.update(sensor_data)
        entry.update({'created': timestamp})

        # Push the data entry to the cloud
        self.client.put(entry)
        print('data pushed to cloud. Entry', entry)

        # Check to make sure entry was added to DataStore
        with self.client.transaction():
            entry_exists = self.client.get(data_snapshot)

            if not entry_exists:
                raise ValueError(
                    'Entry {} was not pushed'.format(data_snapshot))

            entry['transacted'] = True
            self.client.put(entry)

    def list_entries(self):
        query = self.client.query(kind=self.sensor_node)
        query.order = ['created']

        return list(query.fetch())


def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))


# if __name__ == "__main__":

#     # Get current time for data key storage and 'created' parameter
#     curr_time = str(datetime.datetime.now())

#     # Psuedo sensor data dictionary
#     # Collected values of all sensors at a given time instance
#     data_package = {'created': curr_time,
#                     'mic': [2, 3, 3, 3],
#                     'label': 'Running'}

#     print('Executing test run....\n\n\tCurrent time: {}'
#           .format(curr_time), '\ndata type:', type(curr_time))

#     # Can't write image object to NoSQL database...
#     ##################################################
#     # data = data_handler()
#     # data.write(sensor_data=data_package, timestamp=curr_time)
#     ##########################################################
