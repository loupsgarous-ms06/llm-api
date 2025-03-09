# llm-api
for host llm api easily

## usage

1. Place the necessary files.
   - .default(mandatory, sample available)
     - frontpage of faq
   - .prompt(mandatory, sample available)
     - initial system prompt.
   - .document
     - initial document of reference for models.
   - .icon
     - favicon

1. Install some libraries the model want.

1. Run
   ```sh
   python server.py model_name_any_you_want_host
   ```

1. access to ```localhost:8080```, or　```curl localhost:8080 --data-urlencode "text=$YOUR_QUERY"```
