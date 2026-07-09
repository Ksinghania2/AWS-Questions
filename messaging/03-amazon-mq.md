# Amazon MQ

Managed message broker for ActiveMQ and RabbitMQ.

## CLI
```bash
aws mq create-broker --broker-name my-broker --engine-type ACTIVEMQ --engine-version 5.x --host-instance-type mq.t3.micro --users '{"Username":"admin","Password":"MyPass123!"}'
aws mq describe-broker --broker-id broker-xxx
aws mq list-brokers
```

## Q&A
**Q1: What is Amazon MQ?** A: Managed ActiveMQ/RabbitMQ. **Q2: When to use instead of SQS/SNS?** A: When migrating existing apps that use standard protocols (AMQP, MQTT, STOMP). **Q3: Protocols?** A: AMQP, MQTT, STOMP, OpenWire. **Q4: Single vs standby?** A: Standby for HA. **Q5: Storage?** A: EFS for persistent messages.
