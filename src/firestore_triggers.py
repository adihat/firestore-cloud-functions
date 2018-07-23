from src.helpers import get_project_id, get_project_path, get_old_task_status, get_new_task_status, \
    get_project_id_on_deletion, prepare_project_reference, get_transaction_obj
from .configuration import FIRESTORE_CLIENT
from .transactions import update_task_count_in_transaction, \
    update_closed_task_count_in_transaction, update_project_status_in_transaction


def update_task_count(event, context):
    # prepare project reference
    project_ref = prepare_project_reference(event, context)

    # update the count using transaction
    transaction = get_transaction_obj()
    update_task_count_in_transaction(transaction, project_ref)

    return True


def update_closed_task_count(event, context):
    # get old task status
    old_status = get_old_task_status(event)

    # get the new task status
    new_status = get_new_task_status(event)

    # prepare project reference
    project_ref = prepare_project_reference(event, context)

    # update the count using transaction
    transaction = get_transaction_obj()
    update_closed_task_count_in_transaction(transaction, project_ref, old_status, new_status)

    return True


def update_project_on_task_deletion(event, context):
    # get old task status
    task_status = get_old_task_status(event)

    # prepare project reference
    project_ref = prepare_project_reference(event, context)

    # update the count using transaction
    transaction = FIRESTORE_CLIENT.transaction()
    update_project_status_in_transaction(transaction, project_ref, task_status)

    return True
