
# curl -X PUT -H "Content-Type: application/json" \
#      -d "{\"id\":\"B2\",\"formula\":\"6\"}" localhost:3000/cells/B2

curl -X PUT -H "Content-Type: application/json" \
     -d "{\"id\":\"B3\",\"formula\":\"6\"}" localhost:3000/cells/B3

curl -X PUT -H "Content-Type: application/json" \
     -d "{\"id\":\"B4\",\"formula\":\"8\"}" localhost:3000/cells/B4

curl -X DELETE localhost:3000/cells/B4

# curl -X PUT -H "Content-Type: application/json" \
#      -d "{\"id\":\"D4\",\"formula\":\"(B4 + B2) *B3\"}" localhost:3000/cells/D4

# curl -X GET localhost:3000/cells/D4

# curl -s -X GET -d "{\"id\":\"B2\",\"formula\":\"6\"}" \
#     -H "Content-Type: application/json" -w "%{http_code}" localhost:3000/cells/B2

curl -X GET localhost:3000/cells