#!/bin/bash

until curl -s http://localhost:5601/api/status > /dev/null; do
    echo "Waiting for Kibana to start..."
    sleep 10
done

sleep 20

curl -X POST "http://localhost:5601/api/kibana/settings" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "changes": {
      "dateFormat:tz": "UTC"
    }
  }'

echo "Timezone has been set."
