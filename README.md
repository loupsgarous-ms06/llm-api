# llm-api
for host llm api easily

## Usage

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
   python server.py model_name/you_want_to_host
   ```

1. access to ```localhost:8080```, or ```curl localhost:8080 --data-urlencode "text=$YOUR_QUERY"```

## Limitation

- The language model you want to run must have a chat_template set to tokenizer, and the apply_chat_template method must work properly. For more detail, lease read [the document](https://huggingface.co/docs/transformers/main/chat_templating).