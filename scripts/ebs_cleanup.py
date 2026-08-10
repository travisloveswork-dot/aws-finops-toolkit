import boto3

# CONFIGURATION: Set to True to simulate deletions without actually removing volumes
DRY_RUN = True

print("=== AWS FinOps: Unattached EBS Volume Cleaner ===")
print(f"Mode: {'DRY RUN (Simulation)' * DRY_RUN or 'LIVE (Deletion active)'}\n")

ec2 = boto3.client('ec2')

try:
    # Scan for unattached volumes (status = 'available')
    response = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    
    volumes = response.get('Volumes', [])
    
    if not volumes:
        print("No unattached EBS volumes found in this region.")
    else:
        print(f"Found {len(volumes)} unattached (idle) EBS volume(s):")
        volume_ids_to_delete = []
        
        for vol in volumes:
            vol_id = vol['VolumeId']
            size_gb = vol['Size']
            vol_type = vol['VolumeType']
            create_time = str(vol['CreationTime'])
            
            print(f"  -> Volume ID: {vol_id} | Size: {size_gb}GB | Type: {vol_type} | Created: {create_time}")
            volume_ids_to_delete.append(vol_id)
            
        if volume_ids_to_delete:
            if not DRY_RUN:
                print(f"\nDeleting {len(volume_ids_to_delete)} unattached volume(s)...")
                for vol_id in volume_ids_to_delete:
                    ec2.delete_volume(VolumeId=vol_id)
                    print(f"Deleted volume: {vol_id}")
            else:
                print(f"\n[DRY RUN] Would have deleted {len(volume_ids_to_delete)} unattached EBS volume(s).")
                
except Exception as e:
    print(f"Error scanning EBS volumes: {e}")

print("\nEBS Cleanup Audit Complete.")
