

<!-- ```markdown -->
# 🌍 International Shipping API

## 📖 Project Overview
International Shipping API adalah backend service berbasis Django REST Framework yang menyediakan fitur:
- Listing negara & kategori pengiriman
- Pencarian destinasi (subdistrict)
- Perhitungan ongkir internasional + domestik (integrasi dengan API Komship)

💡 **Base URL (contoh)**: `http://localhost:8000/`

---

## 🚀 Features
- **Country Listing** → Mendapatkan daftar negara tujuan
- **Category Listing** → Mendapatkan daftar kategori pengiriman (bisa filter per negara)
- **Destination Search** → Pencarian destinasi berdasarkan keyword
- **Shipping Cost Calculator** → Menghitung ongkir total internasional + domestik

---

## Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd project_directory
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```sh
   KOMSHIP_API_KEY=your_api_key_here
   ```
5. Apply migrations and run the development server:
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

## API Endpoints

### Product Endpoints

#### Get all countries
**Endpoint:** `GET /countries/`

- **Parameters:**
   ```sh
    | Parameter | Type   | Required | Description                  |
    | --------- | ------ | -------- | ---------------------------- |
    | search    | string | No       | Cari berdasarkan nama negara |
   ```

---

#### Get Categories
**Endpoint:** `GET /categories/`

- **Parameters:**
   ```sh
    | Parameter | Type   | Required | Description                  |
    | --------- | ------ | -------- | ---------------------------- |
    | search    | string | No       | Cari berdasarkan nama negara |
   ```

---

#### Get All Categories
**Endpoint:** `GET /category_list`

- **Parameters:**
   ```sh
    |Parameter   | Type   | Required | Description                           |
    | ----------- | ------ | -------- | ------------------------------------- |
    | country\_id | int    | No       | Filter kategori berdasarkan ID negara |
    | search      | string | No       | Cari berdasarkan nama kategori        |
   ```

---

#### Search Destination
**Endpoint:** `GET /destinations/`

- **Parameters:**
   ```sh
    | Parameter | Type   | Required | Description                 |
    | --------- | ------ | -------- | --------------------------- |
    | keyword   | string | Yes      | Kata kunci pencarian lokasi |
   ```

---

#### Calculate Shipping
**Endpoint:** `GET /calculate/`  

- **Parameters:**
   ```sh
    | Parameter                    | Type  | Required | Description                      |
    | ---------------------------- | ----- | -------- | -------------------------------- |
    | country\_id                  | int   | Yes      | ID negara asal barang            |
    | category\_id                 | int   | Yes      | ID kategori barang               |
    | weight                       | float | Yes      | Berat barang (kg)                |
    | destination\_subdistrict\_id | int   | Yes      | ID subdistrict tujuan pengiriman |
   ```

---

# 🚀 Django PostgreSQL Migration Workflow

**1. Install PostgreSQL driver:**
```bash
pip install psycopg2-binary
```

**2. Dump existing data from SQLite:**
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
```

**3. (Optional) Ensure `data.json` is UTF-8 encoded:**
- If you get a `UnicodeDecodeError` later:
  - Open `data.json` in VS Code.
  - Click the encoding at the bottom bar (or `File > Save with Encoding > UTF-8`).
  - Save the file again as **UTF-8**.

**4. Create PostgreSQL database and user.**

**5. Update `settings.py` to use PostgreSQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**6. Run database migrations:**
```bash
python manage.py migrate
```

**7. Load dumped data into PostgreSQL:**
```bash
python manage.py loaddata data.json
```

**8. Test your application thoroughly.**

---
