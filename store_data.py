from oauth2client.client import GoogleCredentials
from google.cloud import datastore
import datetime
import numpy as np
import os
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
    "/Users/joshua/Documents/Sentient-CNC/SentientCNC-3c8c6f014588.json"
sys.exit()

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
        self.client = datastore.Client(project_id)
        self.device = self.client.key(sensor_node)
        self.access = GoogleCredentials.get_application_default()

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
            timestamp = datetime.datetime.now()

        data_snapshot = self.client.key(self.sensor_node, timestamp)

        print('data key generated:', data_snapshot)

        entry = datastore.Entity(data_snapshot)
        entry.update(sensor_data)
        entry.update({'created': timestamp})

        # Push the data entry to the cloud
        self.client.put(entry, credentials=self.access)
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


if __name__ == "__main__":

    curr_time = datetime.datetime.now()
    data_package = {'camera': np.arange(30000).reshape((100, 100, 3)),
                    'mic': np.arange(100).reshape((1, 100)),
                    'created': curr_time,
                    'label': 'Running'}

    print('Executing test run....\n\n\tCurrent time: {}'
          .format(curr_time))

    data = data_handler()

    data.write(data_package, curr_time)
