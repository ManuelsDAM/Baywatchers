from apscheduler.schedulers.background import BackgroundScheduler
import time

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Producto de ejemplo y cada 10 minutos
    url = "https://fittestfreakest.com/products/while-on-earth-move-trainer"
    scheduler.add_job(lambda: track_product(url), 'interval', minutes=10)

    scheduler.start()
    print("⏱️ Scheduler iniciado")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
