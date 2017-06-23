from google.cloud import datastore
from google.cloud import storage
import datetime
import os
import cv2


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
