import boto3
import os
import traceback
import json
import urllib2

def close(session_attributes, fulfillment_state, message):
    """
    Returns a response to the Lex Bot as stated in the documentation
    https://docs.aws.amazon.com/lex/latest/dg/lambda-input-response-format.html

    :param session_attributes: Application-specific session attributes that the client sends in the request.

    :param fulfillment_state: Fulfilled or Failed

    :param message: Message to convey to the user.

    :return: response: response in format required by AWS Lex
    """
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response


def initKuberneteDeploymentReplicaCountChange(event, **kwargs):
    """
    This function will init the deployment replica count change

    ::type deploymentName: string
    :param deploymentName: The name of the Kubernetes deployment

    :type replicaCount: int
    :param replicaCount: Number of replicas
    """
    try:
        body = {
            "replicaCount": kwargs['replicaCount'],
            "deploymentName": kwargs['deploymentName']
        }
        body=json.dumps(body)
        url="https://event-gateway-events-test-dev.moshen-app.net/test-infra/set-pod-replica"
        req = urllib2.Request(url, body, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        return close(
            event["sessionAttributes"],
            'Fulfilled',
            {
              'contentType': 'PlainText',
                'content': response
            }
        )
    except:
         print 'There was an error changing replica count' + str(traceback.format_exc())
         return close(
            event["sessionAttributes"],
            'Failed',
            {
                'contentType': 'PlainText',
                'content': 'There was an error changing replica count'
            }
        )



def main(event, context, **kwargs):
    """
    main function

    """
    deploymentName=event['currentIntent']['slots']['deploymentName']
    replicaCount=event['currentIntent']['slots']['replicaCount']
    return initKuberneteDeploymentReplicaCountChange(
        event,
        deploymentName=deploymentName,
        replicaCount=replicaCount
    )
