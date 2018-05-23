from kubernetes import client, config
import json
import traceback


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    try:
        req = json.loads(req)
    except:
        print 'There was an error parsing the handle req "%s": \n' %(req) + str(traceback.format_exc())
    try:
       config.load_incluster_config()
    except:
        print 'There was an error loading the Kubernetes config: \n' %(req) + str(traceback.format_exc())
    try:
        field_selector='metadata.name='+req['deploymentName']
        api_v1beta1 = client.ExtensionsV1beta1Api()
        spec = client.ExtensionsV1beta1DeploymentSpec(
            replicas=req['replicaCount'],
            template=api_v1beta1.list_namespaced_deployment(namespace="operation-dev-infra", field_selector=field_selector))
        body = client.ExtensionsV1beta1Deployment(spec=spec)
        api_v1beta1.patch_namespaced_deployment_scale(namespace='operation-dev-infra', name=req['deploymentName'], body=body)
        print '"%s" deployment replica count was set to "%s".' %(req['deploymentName'], req['replicaCount'])
    except:
        print 'There was an error changing "%s" deployment replica count to "%s" : \n' %(req['deploymentName'], req['replicaCount']) + str(traceback.format_exc())


