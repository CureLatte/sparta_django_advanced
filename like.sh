curl -X 'POST' \
  'http://localhost:8000/api/v1/likes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "article_id": 99,
  "user_id": '$1'
}'