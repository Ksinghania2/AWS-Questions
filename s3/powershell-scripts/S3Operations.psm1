<#
Simple PowerShell helper for basic S3 work.
This module is meant for beginners who want to try S3 commands from PowerShell.
#>

function New-S3Bucket {
    param(
        [Parameter(Mandatory=$true)]
        [string]$BucketName,
        [string]$Region = 'us-east-1'
    )

    # Create a bucket in the default region unless another region is given.
    if ($Region -eq 'us-east-1') {
        aws s3api create-bucket --bucket $BucketName
    }
    else {
        aws s3api create-bucket --bucket $BucketName --create-bucket-configuration "LocationConstraint=$Region"
    }
}

function Get-S3Objects {
    param(
        [Parameter(Mandatory=$true)]
        [string]$BucketName
    )

    # List the objects inside the bucket.
    aws s3api list-objects-v2 --bucket $BucketName
}

# Beginner example:
# Import-Module ./s3/powershell-scripts/S3Operations.psm1
# New-S3Bucket -BucketName 'my-test-bucket'
# Get-S3Objects -BucketName 'my-test-bucket'

Export-ModuleMember -Function New-S3Bucket, Get-S3Objects
