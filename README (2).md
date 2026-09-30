# AI-Powered Customer Support Ticket Classification and Automation System

An end-to-end application that automatically classifies incoming customer support
tickets into categories, suggests a starting reply, and flags low-confidence
predictions for human review.

![Demo Screenshot](docs/screenshot-demo.png)
<!-- Replace with your actual screenshot, e.g. the one showing REFUND/DELIVERY tickets -->

---

## Problem Statement

Support teams spend significant time manually reading and routing incoming tickets
before any actual resolution work begins. This project automates that first step —
classifying a ticket's category and suggesting a reply — while keeping a human in
the loop for cases the model is unsure about.

---

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌────────────────┐      ┌─────────┐
│   React     │ ───► │ Spring Boot  │ ───► │  Python ML      │      │  MySQL  │
│  (Frontend) │ ◄─── │  (Backend)   │ ◄─── │  Service (API)  │      │         │
└─────────────┘      └──────┬───────┘      └────────────────┘      └────▲────┘
                             │                                          │
                             └──────────────────────────────────────────┘
                                     saves ticket + prediction
```

1. User submits a ticket through the React form
2. Spring Boot receives it, saves the raw ticket to MySQL
3. Spring Boot calls the Python ML service to classify the ticket
4. The ML service returns a category, confidence score, and a suggested reply
5. Spring Boot updates the ticket record in MySQL with these results
6. React displays the classified ticket, flagging it if confidence is low

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Axios |
| Backend | Java, Spring Boot, Spring Data JPA |
| Database | MySQL |
| Machine Learning | Python, scikit-learn |
| NLP | TF-IDF (unigrams + bigrams) |
| ML Models | Linear SVM (calibrated), Logistic Regression (benchmark) |
| Communication | REST APIs (JSON) |

---

## Dataset

[Bitext Customer Support LLM Dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset)
— ~26,872 labeled customer support tickets across 11 categories (ACCOUNT, CANCEL,
CONTACT, DELIVERY, FEEDBACK, INVOICE, ORDER, PAYMENT, REFUND, SHIPPING,
SUBSCRIPTION).

---

## Model Development

Two models were trained and compared on TF-IDF features (unigrams + bigrams,
20,000 max features):

| Model | Validation Macro-F1 |
|---|---|
| Linear SVM | **[fill in your printed score]** |
| Logistic Regression | **[fill in your printed score]** |

Linear SVM was selected as the final model. On the held-out test set, it achieved
near-perfect accuracy across all 11 categories.

**A note on the near-100% accuracy:** the Bitext dataset is synthetic and
template-generated, meaning tickets within a category reuse similar vocabulary.
This makes the classification task easier than real-world, organically-written
tickets would be. The near-perfect score reflects the dataset's low linguistic
diversity rather than a claim that the model would perform this well on live,
unfiltered customer messages.

### Confidence Calibration

`LinearSVC` does not natively output probability scores — only a distance from
its decision boundary. An initial approach used a softmax transformation over
these decision scores, but this consistently *understated* the model's actual
confidence (e.g., a correct prediction showing ~39% confidence). This was fixed
by wrapping the model in scikit-learn's `CalibratedClassifierCV`, which learns
genuine probability estimates via cross-validation. This did not change the
model's predictions — only made its reported confidence trustworthy enough to
be used for the low-confidence review flag described below.

---

## Features

- **Automatic ticket classification** into 11 categories
- **Suggested reply generation** — a category-appropriate template response,
  meant as a starting point for a human agent to review and personalize
- **Low-confidence flagging** — tickets predicted with under 60% confidence are
  visually flagged for manual review, rather than auto-routed
- **Full CRUD** — create, list, and delete tickets

---

## Screenshots

<!-- Add 2-3 screenshots here: the submission form, a classified ticket, and the
     low-confidence warning badge -->

![Classified tickets](docs/screenshot-classified.png)
![alt text](image.png) 

---

## Running Locally

**1. ML Service (Python)**
```bash
cd ml-service
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cd src
uvicorn app:app --reload --port 8000
```

**2. Backend (Spring Boot)**
```bash
cd backend
# update src/main/resources/application.properties with your MySQL credentials
.\mvnw.cmd spring-boot:run
```

**3. Frontend (React)**
```bash
cd frontend
npm install
npm start
```

Then open `http://localhost:3000`.

---

## What I'd Improve Next

- Replace fixed per-category reply templates with a retrieval-based approach
  (return the closest-matching historical ticket's reply, for more variety)
- Test the model against non-synthetic, organically-written support tickets
- Add authentication and role-based access (admin vs. support agent)
- Add basic analytics (ticket volume per category, model accuracy over time)


precision    recall  f1-score   support

     ACCOUNT       1.00      1.00      1.00       817
      CANCEL       1.00      1.00      1.00       142
     CONTACT       1.00      1.00      1.00       300
    DELIVERY       1.00      1.00      1.00       249
    FEEDBACK       1.00      1.00      1.00       300
     INVOICE       1.00      0.99      1.00       274
       ORDER       0.99      0.99      0.99       475
     PAYMENT       1.00      0.99      0.99       300
      REFUND       1.00      0.99      1.00       394
    SHIPPING       0.99      1.00      1.00       295
SUBSCRIPTION       1.00      1.00      1.00       150

    accuracy                           1.00      3696
   macro avg       1.00      1.00      1.00      3696
weighted avg       1.00      1.00      1.00      3696

---

## Author

**[Rama Surendra]** 
