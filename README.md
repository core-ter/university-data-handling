# Data Handling

> Python data handling pipeline with Oracle SQL integration, Faker data generation, and interactive Pandas statistics.

This project demonstrates a comprehensive data management system implemented in Python. It generates realistic test data, manages relationships between entities (Person, Department, Project), and handles data persistence across multiple formats including CSV, JSON, Excel, and Oracle Database.

## ✨ Features

- **Realistic Data Generation**: Uses `Faker` to generate thousands of records with meaningful relationships.
- **Multi-Format Support**:
  - **CSV**: Robust handling with custom delimiters and headers.
  - **JSON**: Hierarchical data storage with date serialization.
  - **Excel (XLSX)**: Native Excel support using `openpyxl`.
  - **Oracle SQL**: Full database integration with automatic table creation and relationship mapping.
- **Extended Data Model**:
  - **Person**: Core entity.
  - **Department**: 1:N relationship with Person (includes Job Titles & Salaries).
  - **Project**: N:M relationship with Person (includes Budgets, Deadlines & Status).
- **Interactive Analytics**:
  - Generates a professional HTML report (`stats.html`).
  - Features interactive dropdowns for department filtering.
  - Visualizes budget metrics and employee distributions.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Oracle Instant Client (for SQL features)
- University Network/VPN (for specific DB connection)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/data-handling.git
   cd data-handling
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: If `requirements.txt` is missing, install: `faker openpyxl oracledb pandas python-dotenv`)*

3. Configure Environment (Optional):
   Create a `.env` file in the root directory:
   ```env
   DB_HOST=codd.inf.unideb.hu
   DB_PORT=1521
   DB_SERVICE=ora21cp.inf.unideb.hu
   DB_USER=your_username
   DB_PASS=your_password
   ```

### Usage

Run the main verification script:

```bash
python src/main.py
```

This will:
1. Generate 1000+ records.
2. Export data to `output/` (CSV, JSON, XLSX).
3. Upload data to Oracle DB (if configured).
4. Generate the interactive `stats.html` report.

## 📂 Project Structure

```
src/
├── data/
│   ├── basic/          # Base templates
│   └── solution/       # Implementation
│       ├── handler/    # CSV, JSON, XLSX, SQL handlers
│       ├── generator.py
│       ├── model.py
│       └── extra_pandas.py
└── main.py             # Entry point
```

## 📊 Statistics Demo

The project generates an interactive HTML dashboard allowing you to explore department data and project metrics in real-time.

