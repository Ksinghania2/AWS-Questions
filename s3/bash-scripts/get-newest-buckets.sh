#!/usr/bin/env bash

################################################################################
# GET NEWEST S3 BUCKETS SCRIPT
#
# Purpose:
#   This script retrieves the newest/most recently created S3 buckets.
#   Useful for listing and managing buckets by creation date.
#
# Prerequisites:
#   - AWS CLI installed and configured with valid AWS credentials
#   - Permissions: s3:ListAllMyBuckets
#
# Usage:
#   ./get-newest-buckets [count]
#
# Examples:
#   ./get-newest-buckets         (shows last 10 buckets)
#   ./get-newest-buckets 5       (shows last 5 buckets)
#   ./get-newest-buckets 20      (shows last 20 buckets)
#
# Output:
#   - Bucket Name
#   - Creation Date
#   - Formatted in reverse chronological order (newest first)
#
# Use Cases:
#   - Find recently created test buckets
#   - Verify bucket creation
#   - Cleanup old buckets
#   - Audit bucket history
################################################################################

echo " === Getting Newest S3 Buckets ==="

# STEP 1: Get count parameter (default: 10)
COUNT=${1:-10}

# STEP 2: Display query details
echo "🔍 Retrieving newest $COUNT buckets..."
echo ""

# STEP 3: Retrieve newest buckets
# list-buckets: Lists all buckets in account
# --query: JMESPath expression to filter/format output
#   sort_by(..., &CreationDate): Sort by CreationDate
#   reverse(@): Reverse order (newest first)
#   [-COUNT:]: Get last COUNT items
# --output table: Format as ASCII table
echo "| Bucket Name                              | Creation Date           |"
echo "|------------------------------------------|-------------------------|"

aws s3api list-buckets \
  --query "reverse(sort_by(Buckets, &CreationDate))[-$COUNT:].{Name:Name, Created:CreationDate}" \
  --output table

# STEP 4: Verify command success
if [ $? -eq 0 ]; then
  echo ""
  echo "✅ SUCCESS: Retrieved bucket list"
else
  echo ""
  echo "❌ FAILURE: Could not retrieve buckets"
  exit 1
fi

exit 0
