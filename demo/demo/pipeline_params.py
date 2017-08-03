# Params class holding the job parameters
class PipelineParams():
  def __init__(video_url, video_name, operator, logfile, job_id):
    self.video_url  = video_url
    self.video_name = video_name
    self.operator   = operator
    self.logfile    = logfile
    self.job_id     = job_id	
