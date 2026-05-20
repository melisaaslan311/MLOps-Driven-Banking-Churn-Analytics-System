"""
Dag: Directed Acyclic Graph(Yönlü Dongusuz Graph)
Airflow kullanmadan önce, her gün bilgisayarın başına geçip sırasıyla extract.py, sonra transform.py, en son da load.py dosyalarını elinle çalıştırman gerekirdi.
Airflow bunu senin yerine otomatiğe bağlar.
Sıralama (Dependency): extract >> transform >> load satırı sayesinde, veri çekilmeden temizlik başlamaz, temizlik bitmeden veritabanına yükleme yapılmaz.
Zamanlama (Scheduling): schedule_interval="@daily" sayesinde bu işlem her gece sen uyurken otomatik çalışır.
Hata Yönetimi: Eğer extract aşamasında internet kesilirse, Airflow transform aşamasına geçmez ve sana "Burada bir hata oldu!" diye haber verir.
"""

"""
Neden Sadece Python Script Kullanmıyoruz da Airflow Kullanıyoruz?
Diyelim ki sadece main.py yazdın ve çalıştırdın. Şu sorunlarla karşılaşırsın:
Hata İzleme: Eğer transform aşamasında hata olursa, kodun nerede kaldığını arayüzden göremezsin. Airflow'da hata veren task kırmızı yanar.
Yeniden Deneme (Retry): Veri çekerken internet giderse Airflow otomatik olarak 5 dakika sonra tekrar dener. Düz Python script'inde bunu elle kodlaman gerekir.
Geriye Dönük Çalıştırma (Backfill): Diyelim ki sistem 3 gün bozuk kaldı. Airflow'a "Geçmiş 3 günün verisini de işle" diyebilirsin.
    
"""
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="bank_churn_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python etl/extract.py"
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="python etl/transform.py"
    )

    load = BashOperator(
        task_id="load",
        bash_command="python etl/load.py"
    )

    extract >> transform >> load
"""