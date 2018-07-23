from src.configuration import FIRESTORE_CLIENT


def get_project_id(event):
    return event.get('value', {}).get('fields', {}).get('project', {}).get('stringValue', '')


def get_project_id_on_deletion(event):
    return event.get('oldvalue', {}).get('fields', {}).get('project', {}).get('stringValue', '')


def get_project_path(context, project_id):
    resource_string = context.resource
    return '/'.join(resource_string.split('/')[5:7] + ['projects', project_id])


def get_old_task_status(event):
    return event.get('oldValue', {}).get('fields', {}).get('status', {}).get('stringValue', '')


def get_new_task_status(event):
    return event.get('value', {}).get('fields', {}).get('status', {}).get('stringValue', '')


def get_transaction_obj():
    return FIRESTORE_CLIENT.transaction()


def prepare_project_reference(event, context):
    project_id = get_project_id(event)
    if not project_id:
        print('no project id')
        return True
    project_ref = get_project_path(context, project_id)
    return project_ref
