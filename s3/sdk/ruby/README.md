# Ruby SDK Example

This is a small Ruby starter example for S3.

## Example
```ruby
require 'aws-sdk-s3'

s3 = Aws::S3::Resource.new(region: 'us-east-1')
puts "Ruby S3 client ready"
```

## Basic setup
Install the gem first.

```bash
gem install aws-sdk-s3
```

## Beginner note
This is a simple way to start using the AWS SDK from Ruby.
