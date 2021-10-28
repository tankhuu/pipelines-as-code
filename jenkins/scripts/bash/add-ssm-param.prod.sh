
#!/bin/bash
NAME=$1
VALUE=$2
TYPE=$3

/usr/local/bin/aws --profile prod ssm put-parameter --overwrite --cli-input-json "{\"Name\":\"$NAME\",\"Value\":\"$VALUE\",\"Type\":\"$TYPE\"}"