from google.cloud import datastore
from google.cloud import storage
import datetime
<<<<<<< HEAD
import os
import cv2
||||||| merged common ancestors
import numpy as np
import pickle
import os
import cv2
import sys
import string

# Establish cloud credientials
home_path = os.path.expanduser('~')
auth_path = "/Documents/Sentient-CNC/SentientCNC-3c8c6f014588.json"
auth_file_path = string.join(home_path, auth_path)

credentials = app_engine.Credentials()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_file_path
=======

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
>>>>>>> 3e9d3071593b3fb4432a77401fbcce8453fa080c


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
    sensor_name: string
        Identifier for sensor gateway. This is used as a primary key for
        storing data entries (so data can be viewed per device)
    """

    def __init__(self,
                 project='sentientcnc-1',
                 sensor_name='cncmill-001'):

        # Creates an authorized service object to make authenticated
        # requests to Google Cloud API using the API's client libraries.
<<<<<<< HEAD
        self.sensor_name = sensor_name
        self.datastore = datastore.Client(project)
        self.storage = storage.Client(project)
        self.directory = os.path.dirname(os.path.abspath('__file__'))

    def _save_image(self, sensor_data, timestamp):
        """
        Internal method for saving the image file.

        NOTE: IMAGE KEY MUST BE 'image'!!

        Removes the image object from the sensor data and writes
        the image to a .jpg file in a $HOME/<sensor_name>-image/
        as well as on the cloud in an identically named bucket.

        Args:
        sensor_data: dict
            dictionary of sensor nodes as keys and data as parameter
        timestamp: string
            timestamp of when the data was recorded

        Returns:
        img_path: string
            name of the file where image was saved
        """

        # Write image
        image = sensor_data.pop('image', None)

        if image is not None:

            # Writing Locally
            ###########################################
            img_file = timestamp + ".jpg"
            img_folder = '/'.join([self.directory, self.sensor_name, 'images'])
            img_path = '/'.join([img_folder, img_file])

            if not os.path.isdir(img_folder):
                os.makedirs(img_folder)

            cv2.imwrite(img_path, image)

            # Writing in the Cloud
            ############################################
            img_bucket = self.storage.lookup_bucket(self.sensor_name)

            if not img_bucket:
                img_bucket = self.storage.create_bucket(self.sensor_name)
                assert isinstance(img_bucket, storage.bucket.Bucket)

            img_blob = img_bucket.blob(timestamp)
            img_blob.upload_from_filename(img_path)

            return img_path

        else:
            return 'NaN'
||||||| merged common ancestors
        self.sensor_node = sensor_node
        self.client = datastore.Client(project_id)
        self.access = GoogleCredentials.get_application_default()
=======
        self.sensor_node = sensor_node
        self.client = datastore.Client(project_id)
>>>>>>> 3e9d3071593b3fb4432a77401fbcce8453fa080c

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

        # Create Keys
        cloud_key = self.datastore.key(self.sensor_name, timestamp)

        # Create the database entity (equivalent to a row entry in a table)
        entry = datastore.Entity(cloud_key)

        # Save the sensor image
        img_filename = self._save_image(sensor_data, timestamp)

        # Metadata for database
        metadata = {'created': timestamp,
                    'file_path': img_filename}

        # Update cloud database with the rest of the data
        entry.update(sensor_data)
        entry.update(metadata)

        # Push the data entry to the cloud
        self.datastore.put(entry)

        # Check to make sure entry was added to DataStore
        with self.datastore.transaction():
            entry_exists = self.datastore.get(cloud_key)

            if not entry_exists:
                raise ValueError(
                    'Entry {} was not pushed'.format(cloud_key))

            entry['transacted'] = True

    def list_entries(self):
        query = self.datastore.query(kind=self.sensor_name)
        query.order = ['created']

        return list(query.fetch())


<<<<<<< HEAD
if __name__ == "__main__":

    # image snapshot
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    capture.release()
    cv2.destroyAllWindows()

    # Psuedo sensor data dictionary
    # Collected values of all sensors at a given time instance
    data_package = {'image': frame,
                    'mic': [2, 3, 3, 3],
                    'label': 'Running'}

    #  Writing image
    ##################################################
    data = data_handler()
    data.write(sensor_data=data_package)
    ##################################################
||||||| merged common ancestors
def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))


if __name__ == "__main__":

    # Get storage bucket for image files
    storage = storage.Client(credentials=credentials)  # Need to sort out credentials
    try:
        print('retrieving bucked: Active\n')
        bucket = storage.lookup_bucket('active')
        assert isinstance(bucket, Bucket) # not sure if this works... 
    except exceptions.NotFound:
        print('Active bucket does not exit. Creating bucket...\n\n')
        bucket = storage.create_bucket('active')

    sys.exit()

    # Get current time for data key storage and 'created' parameter
    curr_time = str(datetime.datetime.now())

    # image snapshot
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    capture.release()
    cv2.destroyAllWindows()

    # Trying to convert the cv2 frame object into something useable...
    frame_list = np.array(frame)
    frame_list = frame_list.tolist()
    frame_pickle = pickle.dumps(frame)

    # info
    print('frame captured. converted to list. shape:', len(frame_list))
    print()
    print('frame size:', sys.getsizeof(frame))
    print('frame list size:', sys.getsizeof(frame_list))
    print('frame pickle size:', sys.getsizeof(frame_pickle))
    print()
    print('frame pickle:', frame_pickle[0:3])

    # Psuedo sensor data dictionary
    # Collected values of all sensors at a given time instance
    data_package = {'created': curr_time,
                    'mic': [2, 3, 3, 3],
                    'label': 'Running'}

    print('Executing test run....\n\n\tCurrent time: {}'
          .format(curr_time), '\ndata type:', type(curr_time))

    # Can't write image object to NoSQL database...
    ##################################################
    # data = data_handler()
    # data.write(sensor_data=data_package, timestamp=curr_time)
    ##########################################################
=======
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
>>>>>>> 3e9d3071593b3fb4432a77401fbcce8453fa080c
