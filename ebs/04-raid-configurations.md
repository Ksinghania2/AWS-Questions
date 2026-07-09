# RAID Configurations on EBS

## RAID Options
| RAID | Description | Use Case |
|------|-------------|----------|
| **RAID 0** | Striping (combine volumes) | Max performance, no redundancy |
| **RAID 1** | Mirroring (duplicate data) | Fault tolerance, higher cost |

## CLI (OS-level configuration)
```bash
# Create RAID 0 with mdadm (on EC2 instance)
sudo mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/xvdf /dev/xvdg
sudo mkfs.ext4 /dev/md0
sudo mount /dev/md0 /mnt/raid

# Create RAID 1
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/xvdf /dev/xvdg
```

## Important Notes
- **RAID 0**: Better performance, but if one volume fails, all data is lost
- **RAID 1**: Redundancy, but half the usable capacity
- **RAID is OS-level**, not AWS-managed
- **Do NOT use RAID 5/6** on EBS (not recommended by AWS)

## Q&A
**Q1: What RAID level is best for performance?** A: RAID 0 (striping).
**Q2: What RAID level provides fault tolerance?** A: RAID 1 (mirroring).
**Q3: Is RAID managed by AWS or the OS?** A: OS-level (configured on the instance).
**Q4: Why is RAID 5/6 not recommended on EBS?** A: EBS already provides durability; RAID 5/6 adds complexity without benefit.
**Q5: What tool is used to create RAID on Linux?** A: mdadm.
