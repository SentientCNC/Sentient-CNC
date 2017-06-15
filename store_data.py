from google.cloud import datastore
import datetime


class data_writer():

    def __init__(self, project_id='sentientcnc-1'):
        self.project = datastore.Client(project_id)
        pass


def create_client(project_id):
    '''
    Creates an authorized service object to make authenticated
    requests to Google Cloud API using the API's client libraries
    input: Google Cloud project ID
    output: client object
    '''

    return datastore.Client(project_id)


def add_task(client, description):
    key = client.key('Task')

    task = datastore.Entity(key, exclude_from_indexes=['description'])

    task.update({
        'created': datetime.datetime.utcnow(),
        'description': description,
        'done': False
    })

    client.put(task)

    return task.key


def mark_done(client, task_id):
    with client.transaction():
        key = client.key('Task', task_id)
        task = client.get(key)

        if not task:
            raise ValueError(
                'Task {} does not exist'.format(task_id))

        task['done'] = True

        client.put(task)


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


