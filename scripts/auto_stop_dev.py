import boto3

# CONFIGURATION: Set to True to simulate stops without actually shutting down resources
DRY_RUN = True

print(f"=== AWS FinOps: Non-Production Auto-Stopper ===")
print(f"Mode: {'DRY RUN (Simulation)' * DRY_RUN or 'LIVE (Actions will be executed)'}\n")

# 1. Audit and Stop EC2 Instances
print("--- Scanning EC2 Instances ---")
ec2 = boto3.resource('ec2')
ec2_to_stop = []

for instance in ec2.instances.all():
    # Only check running instances
    if instance.state['Name'] != 'running':
        continue
        
    environment = None
    do_not_stop = False
    name = "No Name"
    
    if instance.tags:
        for tag in instance.tags:
            if tag['Key'] == 'Environment':
                environment = tag['Value'].lower()
            if tag['Key'] == 'DoNotStop':
                do_not_stop = tag['Value'].lower() == 'true'
            if tag['Key'] == 'Name':
                name = tag['Value']
                
    # Criteria: Must be dev/staging/test, and NOT explicitly opted-out
    if environment in ['dev', 'staging', 'test'] and not do_not_stop:
        ec2_to_stop.append(instance.id)
        print(f"  [TARGET] EC2 ID: {instance.id} | Name: {name} | Env: {environment}")
    else:
        print(f"  [SKIP]   EC2 ID: {instance.id} | State: {instance.state['Name']} | Env: {environment or 'None'} | Opt-Out: {do_not_stop}")

if ec2_to_stop:
    if not DRY_RUN:
        print(f"\nStopping {len(ec2_to_stop)} EC2 instance(s)...")
        ec2.instances.filter(InstanceIds=ec2_to_stop).stop()
        print("EC2 stop command issued successfully.")
    else:
        print(f"\n[DRY RUN] Would have stopped {len(ec2_to_stop)} EC2 instance(s).")
else:
    print("\nNo eligible EC2 instances to stop.")

print("-" * 50)

# 2. Audit and Stop RDS Instances
print("--- Scanning RDS Instances ---")
rds_client = boto3.client('rds')
rds_to_stop = []

try:
    response = rds_client.describe_db_instances()
    for db in response.get('DBInstances', []):
        db_id = db['DBInstanceIdentifier']
        db_status = db['DBInstanceStatus']
        
        # Only check available (running) instances
        if db_status != 'available':
            print(f"  [SKIP]   RDS DB: {db_id} | Status: {db_status}")
            continue
            
        # Fetch tags for RDS instance
        tags_response = rds_client.list_tags_for_resource(ResourceName=db['DBInstanceArn'])
        tags = tags_response.get('TagList', [])
        
        environment = None
        do_not_stop = False
        
        for tag in tags:
            if tag['Key'] == 'Environment':
                environment = tag['Value'].lower()
            if tag['Key'] == 'DoNotStop':
                do_not_stop = tag['Value'].lower() == 'true'
                
        if environment in ['dev', 'staging', 'test'] and not do_not_stop:
            rds_to_stop.append(db_id)
            print(f"  [TARGET] RDS DB: {db_id} | Env: {environment}")
        else:
            print(f"  [SKIP]   RDS DB: {db_id} | Status: {db_status} | Env: {environment or 'None'} | Opt-Out: {do_not_stop}")
            
    if rds_to_stop:
        if not DRY_RUN:
            print(f"\nStopping {len(rds_to_stop)} RDS database(s)...")
            for db_id in rds_to_stop:
                rds_client.stop_db_instance(DBInstanceIdentifier=db_id)
                print(f"Stop command issued for RDS DB: {db_id}")
        else:
            print(f"\n[DRY RUN] Would have stopped {len(rds_to_stop)} RDS database(s).")
    else:
        print("\nNo eligible RDS databases to stop.")
        
except Exception as e:
    print(f"Error checking RDS instances: {e}")

print("\nFinOps Auto-Stop Audit Complete.")
