
# 🚀 Docker PostgreSQL + Airflow ETL Pipeline - NASA APOD

This repository demonstrates an end-to-end **ETL pipeline** using **Docker**, **PostgreSQL**, and **Apache Airflow** to extract data from **NASA's Astronomy Picture of the Day (APOD)** API, transform it, and load it into a PostgreSQL database.

---

## 📌 Project Structure

```
.
├── docker-compose.yml     # Sets up PostgreSQL, Airflow, and supporting services
├── dags/
│   └── nasa_apod_postgres.py  # DAG definition for ETL process
└── README.md
```

---

## ⚙️ What This Project Does

- **Extract**: Fetches data from the NASA APOD API (`https://api.nasa.gov/planetary/apod`)
- **Transform**: Formats and structures the API response
- **Load**: Inserts the data into a PostgreSQL table inside a Docker container
- **Schedule**: Runs daily using Apache Airflow

---

## 🐳 Docker Setup

Make sure you have Docker and Docker Compose installed.

### ✅ Run All Services

```bash
docker-compose up -d
```

This spins up:
- PostgreSQL (`localhost:5432`)
- Airflow Webserver (`localhost:8080`)
- Airflow Scheduler, DAG Processor, Triggerer, and API

---

## 🧠 Airflow DAG

The DAG (`nasa_apod_postgres.py`) does the following:

1. Creates the `apod_data` table if it doesn't exist
2. Sends a GET request to the NASA APOD API
3. Parses the JSON response
4. Inserts the data into PostgreSQL using Airflow’s `PostgresHook`

---

## 🧪 Access and Verify PostgreSQL Data

### Via Terminal (WSL):
```bash
docker exec -it <postgres_container_name> psql -U postgres -d postgres
```

Example query:
```sql
SELECT * FROM apod_data;
```

### Via DBeaver:
- **Host**: `127.0.0.1`
- **Port**: `5432`
- **User**: `postgres`
- **Password**: `postgres`
- **Database**: `postgres`

---

## 🖥️ Access Airflow UI

Visit: [http://localhost:8080](http://localhost:8080)  
Default credentials (if set):
- **User**: `airflow`
- **Password**: `airflow`

Trigger the `nasa_apod_postgres` DAG manually or wait for the next scheduled run.

---

## 🔐 Configuration Tips

- Make sure to set up a connection in Airflow named `postgres_default` with correct Postgres credentials.
- Replace the `DEMO_KEY` in the API call with your actual NASA API key. You can store it in:
  - Airflow Variables, or
  - `.env` file if you configure environment loading

---

## 📈 Sample Output

The `apod_data` table will look like this:

| id | title | explanation | url | date | media_type |
|----|-------|-------------|-----|------|------------|

---

## 📎 Useful Commands

Check running containers:
```bash
docker ps
```

Shut down services:
```bash
docker-compose down
```

---

## 💡 Troubleshooting

- If DBeaver shows `Connection Refused`:
  - Ensure Docker is running
  - Confirm that Postgres container is active (`docker ps`)
- If `psql` command not found in WSL:
  ```bash
  sudo apt install postgresql-client
  ```

---

## 📚 Resources

- [NASA APOD API](https://api.nasa.gov/)
- [Airflow Docs](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## 👨‍💻 Author

**Arun Shukla**  
Passionate about automation, cloud, and data engineering 🚀  
GitHub: [@anshu1016](https://github.com/anshu1016)

---
