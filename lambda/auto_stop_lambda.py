import boto3

def lambda_handler(event, context):
    print("=== AWS FinOps: Serverless Lambda Non-Production Auto-Stopper ===")
    
    ec2 = boto3.resource('ec2')
    ec2_to_stop = []

    for instance in ec2.instances.all():
        if instance.state['Name'] != 'running':
            continue
            
        environment = None
        do_not_stop = False
        
        if instance.tags:
            for tag in instance.tags:
                if tag['Key'] == 'Environment':
                    environment = tag['Value'].lower()
                if tag['Key'] == 'DoNotStop':
                    do_not_stop = tag['Value'].lower() == 'true'
                    
        if environment in ['dev', 'staging', 'test'] and not do_not_stop:
            ec2_to_stop.append(instance.id)

    if ec2_to_stop:
        ec2.instances.filter(InstanceIds=ec2_to_stop).stop()
        print(f"Successfully issued stop command for {len(ec2_to_stop)} EC2 instance(s).")
    else:
        print("No eligible EC2 instances to stop.")
        
    return {
        'statusCode': 200,
        'body': f'FinOps Lambda execution complete. Stopped {len(ec2_to_stop)} instances.'
    }
