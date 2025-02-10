import ollama

# generate a response combining the prompt and data we retrieved in step 2
# note: this function still doesn't have context storage
def chat (model: str, prompt: str, system: str):
  # the function to return the message as a data flow
  def stream_generator():
    # make the prompt
    stream = ollama.chat(
      model=model,
      messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
      ],
      # as a stream
      stream=True
    )
    # and the answer
    for ans in stream:
      yield ans["message"]["content"] + "\n"
  # return the function
  return stream_generator()

# https://ollama.com/blog/embedding-models