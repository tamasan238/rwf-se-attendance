echo "Please wait..."
chromium-browser > /dev/null 2>&1
sleep 30s
sudo ntpdate (removed for publication)
cd /home/pi/se-attendance
python3 record.py
