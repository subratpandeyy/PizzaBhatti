# Pizza Website

A web application for placing pizza orders, built using Flask, HTML/CSS, WTForms, and MongoDB via PyMongo.

## Features

* Browse available pizzas
* Place custom orders with a form
* Form validation using WTForms
* Orders stored in MongoDB
* Admin view for managing orders

## Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS
* **Database:** MongoDB (PyMongo)
* **Forms:** WTForms

## Project Structure

```
pizza-website/
│
├── src/
│   ├── static/             # CSS, images
│   ├── templates/          # HTML templates
│   ├── app.py              # Main Flask application
│   ├── forms.py            # WTForms definitions
│   ├── config.py           # Configuration (e.g., MongoDB URI)
│   └── requirements.txt    # Python dependencies
│
└── README.md
```

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/subratpandeyy/PizzaBhatti.git
   cd pizza-website/src
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MongoDB**

   * Set your MongoDB URI in `config.py` or within the app directly.

4. **Run the app**

   ```bash
   flask run
   ```
