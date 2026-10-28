# Week 4 projects: an LLM app, one per person

Each person builds **one small LLM app** end to end. Your project is listed below. Present it on **Tuesday 3 November** (Tuesday of Week 5).

## What every project must have

| # | Requirement | What "done" looks like |
|---|---|---|
| 1 | **Prompt engineering** | At least **3 techniques** (from zero-shot, few-shot, role/system prompt, chain of thought), written as separate prompt functions |
| 2 | **Structured output + Pydantic** | The LLM returns JSON that is validated with a Pydantic model, with one retry on a `ValidationError` |
| 3 | **Accuracy comparison** | A labelled set of **at least 20 examples** you check by hand; a table of field-level accuracy per prompting technique; say which one you chose and why |
| 4 | **LLM as a judge** | A rubric-based judge that scores the app's free-text output (1–5 + reason, validated with Pydantic); check it against your own scores on 10 examples and report the agreement |
| 5 | **FastAPI backend** | At least `GET /health` and one `POST` endpoint for the main feature, with Pydantic request/response models and sensible status codes (422 / 400 / 503) |
| 6 | **Streamlit frontend** | A page that calls your FastAPI backend (never the LLM directly) and shows the structured result and the judge's score |
| 7 | **Docker** | A `Dockerfile` for the backend and the frontend, and a `docker-compose.yml` so `docker compose up --build` starts the whole app |
| 8 | **Secrets and repo** | Azure OpenAI settings in `.env` (never committed), a `.env.example`, and a README with how to run it and your accuracy table |

Use [Notebook 3](03_prompt_engineering_simple.ipynb) for the prompting, Pydantic, accuracy and judge code, and the
[Streamlit + FastAPI + MLflow demo](https://github.com/samuelts96/streamlit-fastapi-mlflow) as the template for the
FastAPI / Streamlit / Docker Compose layout (you don't need MLflow).

**Suggested layout**

```
backend/     FastAPI app: prompts.py, schemas.py (Pydantic), judge.py, main.py, Dockerfile
frontend/    Streamlit app.py, Dockerfile
notebooks/   prompt comparison + judge calibration
data/        labelled examples (CSV/JSON)
docker-compose.yml
.env.example
README.md
```

Only use public or made-up data. **Never put real personal data into a prompt.**

---

## The projects

### Akinlolu Oyetakin · Job advert analyser
Paste a job advert; the app extracts `job_title`, `seniority` (junior / mid / senior), `required_skills` (list), `nice_to_have_skills`, `salary_min` / `salary_max` (or null) and `remote` (remote / hybrid / onsite), then writes 3 CV bullet suggestions that match the advert.
**Judge:** scores the CV bullets on relevance to the advert, specificity and honesty (no invented experience).
**Data:** job adverts from a public dataset (e.g. LinkedIn Job Postings on Kaggle) or copied from job boards.

### Dr. Janki Pal · Patient feedback triage (synthetic data)
Paste a piece of hospital patient feedback; the app extracts `department`, `issue_type` (clinical care / waiting time / staff attitude / facilities / communication / praise), `urgency` (low / medium / high) and `sentiment`, then drafts a reply from the patient experience team.
**Judge:** scores the reply on empathy, addressing every concern raised and making no clinical promises.
**Data:** write 20+ realistic synthetic feedback messages yourself. No real patient data.

### Saraswathi Lakshman · Recipe and allergen assistant
Paste a recipe; the app extracts `ingredients` (name + quantity), `allergens` (from the 14 major allergens), `diet` (vegan / vegetarian / none), `prep_minutes` and `difficulty`, then suggests one substitution that removes the main allergen.
**Judge:** scores the substitution on whether it actually removes the allergen and keeps the dish workable.
**Data:** recipes from a public dataset (e.g. Food.com Recipes on Kaggle) or recipe websites.

### Tejaswini Pandiri · Customer support ticket router
Paste a support email; the app extracts `category` (billing / technical / delivery / account / other), `priority` (low / medium / high), `product` and `customer_wants` (refund / fix / information / cancel), then drafts a first reply.
**Judge:** scores the reply on answering the actual question, tone and making no promises outside policy.
**Data:** a public dataset (e.g. Customer Support Ticket Dataset on Kaggle) or 20+ tickets you write.

### Egbierele Uku · Receipt and invoice extractor
Paste the text of a receipt or invoice; the app extracts `vendor`, `date` (ISO format), `currency`, `line_items` (description, quantity, price), `total` and `vat`, and Pydantic checks that the line items add up to the total. It then writes a one-line expense description.
**Judge:** scores whether the expense description is accurate and complete for the receipt.
**Data:** 20+ receipts/invoices typed as text (made up or from your own receipts with personal details removed).

### Mojeed Adekunbi Rafiu · News article summariser and classifier
Paste a news article; the app extracts `topic` (business / politics / sport / tech / entertainment), `people`, `organisations`, `locations` and `sentiment`, and writes a 3-bullet summary.
**Judge:** scores the summary on faithfulness (nothing that isn't in the article), coverage of the main points and brevity.
**Data:** BBC News articles (public BBC News classification dataset on Kaggle / Hugging Face).

### Helena Lawrence · Product review insights
Paste a product review; the app extracts each `aspect` mentioned (quality / price / delivery / packaging / customer service) with its own sentiment, an overall `rating_guess` (1–5) and `would_recommend`, then writes a one-sentence summary for the product team.
**Judge:** scores the summary on accuracy to the review and usefulness to the product team.
**Data:** Amazon Fine Food Reviews (Kaggle), which already has star ratings to compare `rating_guess` against.

### Syed Taha Hussaini · Meeting notes action-item extractor
Paste meeting notes or a transcript; the app extracts `decisions` (list), `action_items` (task, owner, due date or null), `open_questions` and `next_meeting` (or null), then writes the follow-up email.
**Judge:** scores the email on including every action item with its owner, clarity and no invented deadlines.
**Data:** 20+ sets of meeting notes you write (different lengths and styles, some with missing owners or dates).

### Toni Miran Borders · Travel request planner
Type a free-text trip request ("4 days in Lisbon in May, £800, love food and museums"); the app extracts `destination`, `days`, `month`, `budget` + `currency`, `travellers`, `interests` and `constraints`, then writes a day-by-day plan.
**Judge:** scores the plan on respecting every constraint (days, budget, interests) and being realistic.
**Data:** 20+ trip requests you write, including vague and contradictory ones.

---

## Presentation (Tuesday 3 November, 10 minutes)

1. Live demo: `docker compose up --build`, then the Streamlit app.
2. Your prompting techniques and the accuracy table: which won and why.
3. Your judge: rubric, agreement with your own scores, and one case where it got it wrong.
4. What you would improve next.

Push to GitHub and add the repo link as a comment on your Week 4 Trello card.
