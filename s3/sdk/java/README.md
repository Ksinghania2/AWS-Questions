# Java SDK Example

This is a simple Java starter example for S3.

## Example
```java
import software.amazon.awssdk.services.s3.S3Client;

public class S3Starter {
    public static void main(String[] args) {
        S3Client s3 = S3Client.create();
        System.out.println("S3 client ready");
    }
}
```

## Basic setup
Add the AWS SDK for Java dependency to your project.

```xml
<dependency>
  <groupId>software.amazon.awssdk</groupId>
  <artifactId>s3</artifactId>
  <version>2.25.40</version>
</dependency>
```
