# Week 4 · NLP, Transformers & Large Language Models

**Mon 26 – Fri 30 Oct 2026**

| Notebook | What it covers |
|---|---|
| [01_nlp_vectorization_restaurant_reviews.ipynb](01_nlp_vectorization_restaurant_reviews.ipynb) | NLP basics (tokenisation, normalisation, stop words and the negation trap, stemming vs lemmatisation, n-grams) · Bag of Words, TF-IDF · Word2Vec (CBOW vs skip-gram), GloVe · vectors vs embeddings with model examples · attention, transformers and BERT (contextual embeddings) · sentence embeddings and semantic search · how LLMs are trained, in brief |
| [02_prompt_engineering_llms.ipynb](02_prompt_engineering_llms.ipynb) | Running an LLM locally with Ollama · anatomy of a prompt · zero-shot, few-shot · structured JSON output with validation · chain of thought, self-consistency · tree of thought · guardrails (prompt injection, PII, output checks) · LLM-as-a-judge · RAG basics · deploying locally as a service |

Both use the same dataset: 1,000 restaurant reviews labelled liked / not liked (loaded from the web, nothing to download by hand).

## Setup

```bash
uv add pandas numpy scikit-learn matplotlib nltk gensim sentence-transformers transformers torch openai pydantic jupyter
```

**Notebook 2 needs an LLM.** The easiest is a local one with [Ollama](https://ollama.com/download):

```bash
ollama pull llama3.2:3b      # ~2 GB; the Ollama server runs on http://localhost:11434
```

To use a cloud model instead, set `LLM_BASE_URL`, `LLM_MODEL` and `OPENAI_API_KEY` as environment variables before starting Jupyter (see Part 1 of the notebook). Never put API keys in a notebook.

Notebook 1 is saved with all its outputs. In Notebook 2, the cells marked **🤖 calls the LLM** are saved without outputs: run them yourself, because answers vary between models and runs.
