from firebase_admin import firestore

from .configuration import FIRESTORE_CLIENT


@firestore.transactional
def update_task_count_in_transaction(transaction, project_ref):
    doc_ref = FIRESTORE_CLIENT.document(project_ref)
    snapshot = doc_ref.get(transaction=transaction)
    transaction.update(doc_ref, {
        u'taskCount': snapshot.get(u'taskCount') + 1
    })


@firestore.transactional
def update_closed_task_count_in_transaction(transaction, project_ref, old_status, new_status):
    doc_ref = FIRESTORE_CLIENT.document(project_ref)

    if old_status == 'open' and new_status == 'closed':
        snapshot = doc_ref.get(transaction=transaction)
        transaction.update(doc_ref, {
            u'closedTaskCount': snapshot.get(u'closedTaskCount') + 1
        })
    elif old_status == 'closed' and new_status == 'open':
        snapshot = doc_ref.get(transaction=transaction)
        transaction.update(doc_ref, {
            u'closedTaskCount': snapshot.get(u'closedTaskCount') - 1
        })
    else:
        print('didnt match any condition')


@firestore.transactional
def update_project_status_in_transaction(transaction, project_ref, task_status):
    doc_ref = FIRESTORE_CLIENT.document(project_ref)

    # get the document
    project = doc_ref.get().to_dict()

    # decrement task count
    if project['taskCount'] > 0:
        snapshot = doc_ref.get(transaction=transaction)
        transaction.update(doc_ref, {
            u'taskCount': snapshot.get(u'taskCount') - 1
        })

    # decrement closed task count
    if task_status == 'closed':
        if project['closedTaskCount'] > 0:
            snapshot = doc_ref.get(transaction=transaction)
            transaction.update(doc_ref, {
                u'closedTaskCount': snapshot.get(u'closedTaskCount') - 1
            })
