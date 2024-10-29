function synclist {
    # Start Flask app in the background
    cd PATH/TO/APP_ROOT
    nohup python3 /path/to/your/app.py > flask_output.log 2>&1 &
    echo "Starting Script..."

    flask_pid=$!

    sleep 5

    echo "Syncing Assignments..."
    response=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/sync-assignments)

    # Check if the response code is 200 (OK)
    if [ "$response" -eq 200 ]; then
        echo "Sync successful..."
    else
        echo "Error: Sync failed with status code $response."
    fi

    # Kill the Flask app
    kill $flask_pid

    # Print Done when finished
    echo "Done"
}