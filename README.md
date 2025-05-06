# c4k
A Fast Efficient Check-in/Check-out System for C4K

## Information
The project has an admin, backend, and frontend component. The admin site is built using **streamlit** and the backend is built using **FastAPI**. The frontend is built using **Next.js**, **React**, and **Tailwind CSS**. The database used is **SQLite**. The frontend, backend, and admin code are in separate folder in the root directory of the project. This project uses `uv` python package manager for the **admin** and **backend**.

## Running the Project

1. Clone the repository:
    ```bash
    git clone https://github.com/pradeepravi26/c4k.git
    ```

2. Navigate to the project directory:
    ```bash
    cd c4k
    ```

3. Install and run **admin**:
    ```bash
    cd admin
    uv venv
    source .venv/bin/activate # for MacOS/Linux
    .venv\Scripts\activate # for Windows
    uv pip install -r pyproject.toml
    streamlit run main.py
    ```

4. Install and run **backend**:
    ```bash
    cd backend
    uv venv
    source .venv/bin/activate # for MacOS/Linux
    .venv\Scripts\activate # for Windows
    uv pip install -r pyproject.toml
    fastapi run main.py
    ```

5. Install and run **frontend**:
    ```bash
    cd frontend
    npm install
    npm run start
    ```

6. Open the following URLs in your browser:
    - Admin: [http://localhost:8501](http://localhost:8501)
    - Frontend: [http://localhost:3000](http://localhost:3000)

**Note**:
- Change the `CORS` settings in the `backend/main.py` file to allow requests from the frontend URL.
- The scripts folder contains a script to generate random data for the database. The data is generated using the `Faker` library. The data is generated in the `data` folder. The data is in CSV format. The data can be imported into the database using the admin site.
- The `c4k.db` file is the SQLite database file. The database currently has fake data for testing purposes. To clear the database, delete the `c4k.db` file and run either the `orm.py` file in the `admin` or `backend` folder. This will create a new database file with the same schema as the old one, but without any data.

## Project Structure
```
.
├── Caddyfile
├── README.md
├── admin
│   ├── README.md
│   ├── __init__.py
│   ├── forms
│   │   ├── check_in.py
│   │   └── check_out.py
│   ├── home.py
│   ├── main.py
│   ├── member_visit
│   │   ├── live_member_visits.py
│   │   └── manage_member_visits.py
│   ├── orm.py
│   ├── pyproject.toml
│   ├── user
│   │   ├── manage_users.py
│   │   └── upload_users.py
│   └── uv.lock
├── backend
│   ├── README.md
│   ├── main.py
│   ├── orm.py
│   ├── pyproject.toml
│   ├── schema.py
│   └── uv.lock
├── c4k.db
├── frontend
│   ├── README.md
│   ├── components.json
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── public
│   │   ├── file.svg
│   │   ├── globe.svg
│   │   ├── next.svg
│   │   ├── vercel.svg
│   │   └── window.svg
│   ├── src
│   │   ├── app
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── guest
│   │   │   │   ├── check-in
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── check-out
│   │   │   │   │   ├── [id]
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── search
│   │   │   │   │       └── page.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── student
│   │   │   │   ├── check-in
│   │   │   │   │   ├── [id]
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── search
│   │   │   │   │       └── page.tsx
│   │   │   │   ├── check-out
│   │   │   │   │   ├── [id]
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── search
│   │   │   │   │       └── page.tsx
│   │   │   │   └── page.tsx
│   │   │   └── volunteer
│   │   │       ├── check-in
│   │   │       │   ├── [id]
│   │   │       │   │   └── page.tsx
│   │   │       │   └── search
│   │   │       │       └── page.tsx
│   │   │       ├── check-out
│   │   │       │   ├── [id]
│   │   │       │   │   └── page.tsx
│   │   │       │   └── search
│   │   │       │       └── page.tsx
│   │   │       └── page.tsx
│   │   ├── components
│   │   │   ├── time-picker.tsx
│   │   │   └── ui
│   │   │       ├── alert.tsx
│   │   │       ├── button.tsx
│   │   │       ├── calendar.tsx
│   │   │       ├── card.tsx
│   │   │       ├── dialog.tsx
│   │   │       ├── input.tsx
│   │   │       ├── label.tsx
│   │   │       └── select.tsx
│   │   └── lib
│   │       └── utils.ts
│   └── tsconfig.json
└── scripts
    ├── README.md
    ├── data
    │   ├── students.csv
    │   └── volunteers.csv
    ├── main.py
    ├── pyproject.toml
    └── uv.lock
```