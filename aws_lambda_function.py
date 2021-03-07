import json

def sqsmsg(event, context):
    try:
        # decode from sqs
        print('The original source is '+str(event))
        event = event['Records']
        event = event[0]
        event = event['body']
        #print(event)
        event = json.loads(event)
    except KeyError:
        print('unable to regionize the msg in sqs')