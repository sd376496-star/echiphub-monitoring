
from flask import Flask, Response
import requests

app = Flask(__name__)

API_URL = "https://echiphub.in/wp-admin/admin-ajax.php?action=echd_data"

@app.route("/metrics")
def metrics():
    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        result = response.json()
        data = result["data"]

        metric_lines = [
            "# HELP echiphub_total_views Total views on eChipHub",
            "# TYPE echiphub_total_views gauge",
            f"echiphub_total_views {data.get('total_views', 0)}",
            "# HELP echiphub_total_visitors Total visitors on eChipHub",
            "# TYPE echiphub_total_visitors gauge",
            f"echiphub_total_visitors {data.get('total_visitors', 0)}",
            "# HELP echiphub_today_visits Visits today on eChipHub",
            "# TYPE echiphub_today_visits gauge",
            f"echiphub_today_visits {data.get('today_visits', 0)}",
            "# HELP echiphub_today_views Views today on eChipHub",
            "# TYPE echiphub_today_views gauge",
            f"echiphub_today_views {data.get('today_views', 0)}",
            "# HELP echiphub_online_now Visitors online now on eChipHub",
            "# TYPE echiphub_online_now gauge",
            f"echiphub_online_now {data.get('online_now', 0)}",
        ]

        return Response("\n".join(metric_lines) + "\n",
                        mimetype="text/plain; version=0.0.4")
    except Exception as error:
        return Response(f"# Exporter error: {error}\n", status=500,
                        mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
