# 1. Grab a blank computer with Python installed
FROM python:3.10

# 2. Hugging Face requires us to create a user for security
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# 3. Create a folder called /app and move inside it
WORKDIR /app

# 4. Copy the requirements file and install the heavy AI tools
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Python code into the cloud computer
COPY --chown=user . /app

# 6. Open port 7860 (This is the specific "door" Hugging Face uses)
EXPOSE 7860

# 7. Start the engine! (With a 5-minute timeout so CLIP has time to load)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "-t", "300", "server:app"]