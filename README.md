Before starting the app. Please configure '<your-api-key>','<your-consumer-key>','<your-secret-key>' in app.py with your Google OAuth 2.0 Client IDs's Credentials.

0. Use command 'docker-compose up' to start the app once credentials has been setup.
  
1. In order to test the app, you can try to use the command 'curl http://127.0.0.1:5000/login/google -UseBasicParsing' or open the url 'http://127.0.0.1:5000/login/google' on your browser to try out the authentication process.
  For the to-do list:
  - To see the list, use 'Invoke-WebRequest -Uri http://127.0.0.1:5000/todos -Method GET -UseBasicParsing'.
  - To add a to-do item, use'Invoke-WebRequest -Uri http://127.0.0.1:5000/todos -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "task": "<Your to-do task>" }' -UseBasicParsing'.
  - To update a to-do item with completed tag, use 'Invoke-WebRequest -Uri http://127.0.0.1:5000/todos/{todo_id} -Method PUT -Body '{"completed": true}' -ContentType "application/json" -UseBasicParsing'.
  - To delete a to-do item, use 'Invoke-WebRequest -Uri http://127.0.0.1:5000/todos/{todo_id} -Method DELETE -UseBasicParsing'.
