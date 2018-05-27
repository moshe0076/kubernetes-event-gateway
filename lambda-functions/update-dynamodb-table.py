import boto3
import os
import traceback
import json

def updateDynamoDBTable(**kwargs):
    """
    This function will update the kubernetes-service-pod-count-table
    It will set the number of pods in a service

    :type serviceName: string
    :param serviceName: The name of the Kubernetes service.

    :type numberOfPods: int
    :param numberOfPods: Number of pods

    """

    try:
        dynamodb = boto3.resource('dynamodb')
    except:
        print 'There was an error connecting to DynamoDB APIs in' + str(traceback.format_exc())

    try:
        table = dynamodb.Table('kubernetes-service-pod-count')
    except:
        print 'There was an error connecting to DynamoDB table "kubernetes-service-pod-count"' + str(traceback.format_exc())
    try:
        table.update_item(
            Key={
                'service-name': kwargs['serviceName'],
            },
            UpdateExpression='SET pod_count = :val1',
            ExpressionAttributeValues={
                ':val1': kwargs['numberOfPods']
            }
        )
        print 'The number of service "%s" pods was updated to "%d"\n' %(kwargs['serviceName'], kwargs['numberOfPods'])
    except:
       print 'There was an error Updating number of service "%s" pods to "%d": \n' %(kwargs['serviceName'], kwargs['numberOfPods']) + str(traceback.format_exc())

def main(event, context, **kwargs):
    """
    main function

    """
    serviceName=event['data']['body']['serviceName']
    numberOfPods=int(event['data']['body']['numberOfPods'])
    updateDynamoDBTable(serviceName=serviceName, numberOfPods=numberOfPods)
