import boto3
import os
import traceback
import json
import sys

def updateDynamoDBTable(**kwargs):
    """
    This function will update the kubernetes-deployment-replica-count DynambDB table
    it will update the number of replicas in a deployment field
    it will update the event ID which triggered the replica count change field
    and it will update the event time which triggered the replica count change field

    :type deploymentName: string
    :param deploymentName: The name of the Kubernetes deployment

    :type replicaCount: int
    :param replicaCount: Number of replicas

    :type kubeEventId: string
    :param kubeEventId: ID of the event which triggerd the replica count change

    :type kubeEventTime: string
    :param kubeEventTime: Time of the event which triggerd the replica count change

    """

    try:
        dynamodb = boto3.resource('dynamodb')
    except:
        print 'There was an error connecting to DynamoDB APIs in' + str(traceback.format_exc())
        sys.exit(1)
    try:
        table = dynamodb.Table('kubernetes-deployment-replica-count')
    except:
        print 'There was an error connecting to DynamoDB table "kubernetes-deployment-replica-count"' + str(traceback.format_exc())
        sys.exit(1)
    try:
        table.update_item(
            Key={
                'deployment_name': kwargs['deploymentName'],
            },
            UpdateExpression='SET replica_count = :replica_count, kube_event_id= :kube_event_id, kube_event_time= :kube_event_time',
            ExpressionAttributeValues={
                ':replica_count': kwargs['replicaCount'],
                ':kube_event_id': kwargs['kubeEventId'],
                ':kube_event_time': kwargs['kubeEventTime'],
            }
        )
        print 'The number of deployment "%s" replicas was updated to "%d"\n' %(kwargs['deploymentName'], kwargs['replicaCount'])
    except:
       print 'There was an error Updating number of deployment "%s" replicas to "%d": \n' %(kwargs['deploymentName'], kwargs['replicaCount']) + str(traceback.format_exc())
       sys.exit(1)

def main(event, context, **kwargs):
    """
    main function

    """
    print event
    deploymentName=event['data']['body']['deploymentName']
    replicaCount=int(event['data']['body']['replicaCount'])
    kubeEventId=event['data']['body']['kubeEventId']
    kubeEventTime=event['data']['body']['kubeEventTime']
    updateDynamoDBTable(deploymentName=deploymentName, replicaCount=replicaCount, kubeEventId=kubeEventId, kubeEventTime=kubeEventTime)


