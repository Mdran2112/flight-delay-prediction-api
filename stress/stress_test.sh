wrk -t20 -c100 -d45s -H "X-API-KEY: MYAPIKEY" \
                     -H "Content-Type: application/json" \
                     -s post.lua \
                     http://localhost:5050/prediction-server/predictions
