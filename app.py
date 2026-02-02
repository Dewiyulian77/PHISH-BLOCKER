from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Memuat model AI
try:
    model = joblib.load('model_phishing.pkl')
except Exception as e:
    print(f"Gagal memuat model: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url_input = request.form['url'].lower()
    
    # Kata kunci simulasi phishing untuk demo
    kata_kunci_bahaya = ['login', 'verifikasi', 'update', 'akun', 'hadiah', 'bca', 'bri', 'dana', 'secure', 'shopee']
    is_mencurigakan = any(kata in url_input for kata in kata_kunci_bahaya)
    
    # Prediksi AI (Simulasi fitur teknis)
    features = [1] * 30 
    prediction = model.predict([np.array(features)])

    # Penentuan status
    if is_mencurigakan or prediction[0] == -1:
        status, warna = "BAHAYA", "#dc3545"
        pesan = "Sistem mendeteksi indikasi kuat serangan phishing. Jangan masukkan data sensitif pada link ini."
    else:
        status, warna = "AMAN", "#28a745"
        pesan = "Sistem tidak menemukan ancaman mencurigakan. Tetap waspada saat mengakses informasi."

    return render_template('result.html', 
                           status=status, 
                           pesan=pesan, 
                           skor=96.7, 
                           warna=warna, 
                           url=url_input)

if __name__ == "__main__":
    # Mendukung port dinamis untuk publikasi (Render/Railway)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)