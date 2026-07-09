#!/bin/bash

BASE_URL="http://localhost:5000"

echo "Testing POST /api/timeline_post..."
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/timeline_post" \
  -d "name=Test User&email=test@test.com&content=This is a test post $(date)")

echo "POST Response: $POST_RESPONSE"

echo ""
echo "Testing GET /api/timeline_post..."
GET_RESPONSE=$(curl -s "$BASE_URL/api/timeline_post")

echo "GET Response: $GET_RESPONSE"

# 检查 GET 结果里是否包含刚才 POST 的内容
if echo "$GET_RESPONSE" | grep -q "This is a test post"; then
    echo ""
    echo "✅ Test passed! Post was successfully added and retrieved."
else
    echo ""
    echo "❌ Test failed! Post was not found in GET response."
    exit 1
fi