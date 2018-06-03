from kubernetes import client, config
import json
import requests

def handle(event):
    """handle a request to the function
    Args:
        event (str): CloudEvent
    """
    try:
        event=json.loads(event)
        deploymentName=event['data']['body']['deploymentName']
        replicaCount=int(event['data']['body']['replicaCount'])
        kubeEventId=event['eventID']
        kubeEventTime=event['eventTime']
    except:
        return '{"statusCode": 500, "headers": {"Content-Type": "text/plain; charset=utf-8"}, "body": "There was an error parsing the event"}'
    try:
        config.load_incluster_config()
    except:
        return '{"statusCode": 500, "headers": {"Content-Type": "text/plain; charset=utf-8"}, "body": "There was an error loading Kubernetes config"}'
    try:
        field_selector = 'metadata.name='+deploymentName
        api_v1beta1 = client.ExtensionsV1beta1Api()
        spec = client.ExtensionsV1beta1DeploymentSpec(
            replicas=replicaCount,
            template=api_v1beta1.list_namespaced_deployment(namespace="test-infra", field_selector=field_selector))
        body = client.ExtensionsV1beta1Deployment(spec=spec)
        api_v1beta1.patch_namespaced_deployment_scale(namespace='test-infra', name=deploymentName, body=body)
    except:
        return '{"statusCode": 500, "headers": {"Content-Type": "text/plain; charset=utf-8"}, "body": "There was an error changing deployment replica count"}'
    try:
        body = {
            "replicaCount": replicaCount,
            "deploymentName": deploymentName,
            "kubeEventId": kubeEventId,
            "kubeEventTime": kubeEventTime
        }
        r = requests.post(
            'http://event-gateway:4000/aws-lambda/update-dynamodb-kubernetes-deployment-replica-count-table',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(body))
        if r.status_code > 299:
            raise Exception
    except:
        return '{"statusCode": 500, "headers": {"Content-Type": "text/plain; charset=utf-8"}, "body": "There was an error Updating DynamoDB"}'
    return '{"statusCode": 200, "headers": {"Content-Type": "text/plain; charset=utf-8"}, "body": "%s deployment replica count was changed to %d successfully"}' %(deploymentName, replicaCount)



