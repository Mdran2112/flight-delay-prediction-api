wrk -t12 -c400 -d45s -H "X-API-KEY: MYAPIKEY" \
                     -H "Content-Type: application/json" \
                     -s post.lua \
                     http://localhost:5050/prediction-server/predictions
