# gcd
# 📂 Cloud Storage + Cloud Run + Pub/Sub Integration

This project sets up a system where uploading a file to a Google Cloud Storage bucket triggers a **Cloud Run** service. The service extracts metadata (file name, size, format) and publishes it to a **Pub/Sub** topic.

---

## 🚀 Architecture Overview

1. **Cloud Storage Bucket**  
   - Acts as the trigger source when a file is uploaded.
  
2. **Cloud Run Service**  
   - Runs a Python Flask app that receives the upload notification.
   - Extracts file details and sends them to a Pub/Sub topic.

3. **Pub/Sub Topic**  
   - Collects and stores messages about uploaded files.

---

## 📁 Project Structure

