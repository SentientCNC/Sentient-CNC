from google.cloud import datastore
import datetime


class data_handler():
    """
    Object designed to handle storage of incoming sensor data.
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
            data_snapshot = self.client.key(self.sensor_node,
                                            datetime.datetime)
        else:
            data_snapshot = self.client.key(self.sensor_node,
                                            timestamp)

        entry = datastore.Entity(data_snapshot)
        entry.update(sensor_data)

        # Push the data entry to the cloud
        self.client.put(entry)

        # Check to make sure entry was added to DataStore
        with self.client.transaction():
            entry_exists = self.client.get(data_snapshot)

            if not entry_exists:
                raise ValueError(
                    'Entry {} was not pushed'.format(data_snapshot))

            entry['transacted'] = True
            self.client.put(entry)


def delete_task(client, task_id):
    '''
    deletes a task entity, using the task entity's key
    '''
    key = client.key('Task', task_id)
    client.delete(key)


def list_tasks(client):
    query = client.query(kind='Task')
    query.order = ['created']

    return list(query.fetch())
