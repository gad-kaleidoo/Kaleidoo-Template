import utils
import config

def get_scheduler(scheduler_id, org_id):
    url = f"{config.SCHEDULER_URL}/{scheduler_id}/{org_id}"
    return utils.get(url)

# Additional generic function examples
def delete_scheduler(scheduler_id, org_id):
    url = f"{config.SCHEDULER_URL}/{scheduler_id}/{org_id}"
    return utils.delete(url)

def create_scheduler(scheduler_id, org_id, data):
    url = f"{config.SCHEDULER_URL}/{scheduler_id}/{org_id}"
    return utils.post(url, data)

def update_scheduler(scheduler_id, org_id, data):
    url = f"{config.SCHEDULER_URL}/{scheduler_id}/{org_id}"
    return utils.put(url, data)
