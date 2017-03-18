import uuid

JOB_PREFIX = "job_"
LOG_PREFIX = "log_"

def generate_job_id():
  return JOB_PREFIX + str(uuid.uuid4().get_hex().upper()[0:6])
