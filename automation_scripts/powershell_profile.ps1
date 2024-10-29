# Add this to your powershell $profile to automate running the flask server.
function synclist {
    # Start the Flask app in a background job
	Write-Host "Running Script..."
    $flaskJob = Start-Job -ScriptBlock {
        cd PATH/TO/PROJECT_ROOT
        python -u "c:\Users\User\projects\Canvas2DoIst\app.py"
    }

    Start-Sleep -Seconds 1

	Write-Host "Accessing Assignments..."
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/sync-assignments" -UseBasicP
    Write-Host "Response Status Code: $($response.StatusCode)"

    # Stop the Flask job
    Stop-Job -Job $flaskJob
    Remove-Job -Job $flaskJob
	
    Write-Host "Done"
}