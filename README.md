# Early Adopters Database

A web dashboard for managing email records with chart-based analytics, built with **Flask** and **SQLite Cloud**.

## Features

* Chart analytics (by day and by hour)
* Responsive table with search, pagination, and sorting
* Delete emails
* Export data to CSV
* Fully integrated with SQLite Cloud
* No heavy ORM dependencies (native sqlitecloud only)

## Technology Stack

### Backend

* **Flask 3.0.0** – Web framework
* **flask-cors 4.0.0** – CORS support
* **python-dotenv 1.0.0** – `.env` configuration
* **sqlitecloud 1.0.37** – Native SQLite Cloud driver

### Frontend

* **Bootstrap 5.3.2** – CSS framework (CDN)
* **Chart.js 4.4.0** – Charts (CDN)

## Setup

### Prerequisites

* Python 3.8+
* An account on [SQLite Cloud](https://sqlitecloud.io)
* A database created in SQLite Cloud

### 1. Clone the repository

```powershell
git clone <repo-url>
cd early-adopters-db
```

### 2. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file at the project root:

```env
CONNECTION_STRING=sqlitecloud://api-key@host:8860/dbname?apikey=your_api_key
```

**How to obtain the connection string:**

1. Go to your SQLite Cloud dashboard
2. Select your database
3. Copy the connection string (usually starts with `sqlitecloud://`)
4. Paste it inside `.env`

### 5. Run the application

```powershell
cd source
python main.py
```

Application available at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## Project Structure

```
early-adopters-db/
├── source/
│   ├── main.py              # Flask application with API routes
│   ├── database.py          # Email class + sqlitecloud connection
│   └── templates/
│       └── index.html       # Bootstrap UI + Chart.js graphs
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables example
├── test_connection.py       # Database connection test
├── README.md                # This file
└── venv/                    # Virtual environment
```

## API Endpoints

### GET `/`

Serves the main HTML page.

### GET `/api/emails`

Returns a list of all registered emails.

**Response:**

```json
[
  {
    "email": "user@example.com",
    "time": "12/07/2025 14:30:45"
  },
  {
    "email": "another@example.com",
    "time": "12/07/2025 14:25:10"
  }
]
```

### POST `/api/emails`

Adds a new email.

**Request:**

```json
{
  "email": "new@example.com"
}
```

**Response:**

```json
{
  "message": "Email added successfully",
  "email": "new@example.com",
  "time": "12/07/2025 14:30:45"
}
```

### DELETE `/api/emails`

Deletes an email.

**Request:**

```json
{
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "message": "Email deleted successfully"
}
```

### GET `/api/emails/stats`

Returns registration statistics.

**Response:**

```json
{
  "total": 42,
  "byDay": [
    {"date": "2025-12-07", "count": 15},
    {"date": "2025-12-08", "count": 27}
  ],
  "byHour": [
    {"hour": "00", "count": 0},
    {"hour": "01", "count": 1},
    {"hour": "14", "count": 8},
    ...
    {"hour": "23", "count": 2}
  ]
}
```

## How It Works

### Database (SQLite Cloud)

The `Email` class in `database.py` provides a simple interface for interacting with SQLite Cloud:

```python
# Create a new email
new_email = Email.create("user@example.com")

# List all emails
emails = Email.select()

# Delete an email
Email.delete("user@example.com")

# Get statistics
stats = Email.get_stats()
```

### Frontend

`index.html` implements:

* Table with search, sorting, and pagination
* Line and bar charts built with Chart.js
* Action buttons (copy, delete)
* CSV export

All data is loaded dynamically via REST API.

## Troubleshooting

### Error: "CONNECTION_STRING environment variable must be set"

* Ensure `.env` exists in the project root
* Ensure `CONNECTION_STRING` is properly set
* Use `.env.example` as reference

### Error: "ModuleNotFoundError: No module named 'sqlitecloud'"

```powershell
pip install sqlitecloud
```

### Error: "Connection refused" or timeout

* Check whether the connection string is correct
* Verify network conditions (firewall, VPN, etc.)
* Ensure the API key is valid
* Ensure the database exists in SQLite Cloud

### Empty table on dashboard

* Make sure you're connected to the right database
* Ensure the `emails` table was created (automatic)
* Check application logs

## Development

### Run in debug mode

```powershell
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
cd source
python main.py
```

### Test database connection

```powershell
python test_connection.py
```

### Run tests (if available)

```powershell
pytest tests/
```

## Environment Variables

| Variable            | Required | Example                                         |
| ------------------- | -------- | ----------------------------------------------- |
| `CONNECTION_STRING` | Yes      | `sqlitecloud://api-key@host:8860/db?apikey=key` |
| `FLASK_ENV`         | No       | `development` or `production`                   |
| `FLASK_DEBUG`       | No       | `1` or `0`                                      |

## Successfully Deployed?

If everything is running:

1. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Add some emails
3. Watch the charts update
4. Test search, pagination, and export

---

Se quiser, posso gerar também a versão em inglês com layout de README.md mais profissional.
