# Gunakan image Python 3.11
FROM python:3.11

# Tetapkan direktori kerja dalam container
WORKDIR /code

# Salin file requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Instal dependensi tanpa menyimpan cache
RUN pip install --no-cache-dir -r /code/requirements.txt

# Salin seluruh isi proyek ke dalam container
COPY . /code/

# Tetapkan variabel lingkungan dengan format yang benar
ENV PORT=8003

# Buka port yang digunakan
EXPOSE ${PORT}

# Jalankan aplikasi menggunakan app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8003", "app:app"]