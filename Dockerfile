#base image get light linux(Slim)
FROM python:3.9-slim

# 2. setup folder.
WORKDIR /app

# 3. paste for requirements.
COPY requirements.txt .

# 4. install library for pip.
RUN pip install --no-cache-dir -r requirements.txt

# 5. copy source.
COPY . .

# 6. open port 8501.
EXPOSE 8501

# 7. order for implement
# (0.0.0.0 allowing external access)
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]