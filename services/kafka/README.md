docker exec -it kafka-broker-1 bash
kafka-topics --bootstrap-server kafka-broker-1:9092 --create --topic test
kafka-console-producer --bootstrap-server kafka-broker-1:9092 --topic test
kafka-console-consumer --bootstrap-server kafka-broker-1:9092 --topic test

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data "{\"schema\":\"{\\\"type\\\":\\\"record\\\",\\\"name\\\":\\\"example\\\",\\\"fields\\\":[{\\\"name\\\":\\\"name\\\",\\\"type\\\":\\\"string\\\"},{\\\"name\\\":\\\"age\\\",\\\"type\\\":\\\"int\\\"}]}\"}" http://localhost:8081/subjects/my-avro-topic-value/versions

kafka-avro-console-producer \
    --broker-list kafka-broker-1:19092 --topic my-avro-topic \
    --property value.schema='{"type":"record","name":"example","fields":[{"name":"name","type":"string"},{"name":"age","type":"int"}]}'

kafka-avro-console-consumer --topic my-avro-topic \
    --bootstrap-server kafka-broker-1:9092 --from-beginning \
    --property schema.registry.url=http://localhost:8081
