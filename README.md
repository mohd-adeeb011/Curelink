# Curelink

## Different Approaches
- RAG
- Fine Tuning
- Prompting

### Why Finetuning and RAG was not approached.
* Since RAG is built on top of documents—in our case, it would be the previous chat history—using the previous chats as context won't help, as the query will be different each time.
* Fine-tuning could be a pragmatic approach, given that there's a lot of data with sufficient examples. However, the provided data only had 1.8 million tokens and 23 examples.
* While it’s not the most efficient solution, given the limited data, prompting can do the job of imitating human responses.
