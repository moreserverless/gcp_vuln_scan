from diagrams import Cluster, Diagram 
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.devtools import Scheduler

with Diagram("Vulnerability Scan Notification", show=False):

    # Scheduler >> Cloud Function >> Pub/Sub >> Cloud Function

    with Cluster("GCP Project"):

        schedule_scan = Scheduler("Cloud Scheduler") >> Functions("Read Vulnerabilities") 
        publish_results = schedule_scan >> PubSub("Pub/Sub")
        email_results = publish_results >> Functions("Notification Service")