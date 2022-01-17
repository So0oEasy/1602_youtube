

from flask import Flask, render_template, request, redirect, send_file
from csv_export import  save_to_csv
from apscheduler.schedulers.background import BackgroundScheduler
import ps1010
import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()

def get_tags():

    youtube_df = ps1010.get_link()
    df_result =ps1010.get_hash_tag(youtube_df)
    save_to_csv(df_result)
    now = datetime.datetime.now()
    print(":: LOOP ::")
    print(now)


if __name__ == "__main__":
    scheduler.start()
    
    #매 30분마다 시작
    scheduler.add_job(get_tags,'interval', minute=30, id='test_1')
    app.run(use_reloader=False,debug=True)

# @app.route("/")
# def home():

#     return render_template("index_1.html")


# @app.route("/search", methods=["GET"])
# def search():

#     text = request.args.get("work")

#     if text:
#         text = text.lower()
#         fromDB = db.get(text)
#         if fromDB:
#             jobs = fromDB
#         else:
#             jobs = get_jobs(text)
#             db[text] = jobs

#     else:
#         return redirect("/")

#     return render_template(
#         "index_2.html", text=text, searchText=text, resultNum=len(jobs), jobs=jobs
#     )


# @app.route("/export")
# def export():

#     # try ~ expect ------> try 도중 에러나면 expect문 실행
#     try:
#         text = request.args.get("work")

#         if not text:
#             raise Exception()  # 에러 발생시 expect문 실행

#         text = text.lower()
#         jobs = db.get(text)

#         if not jobs:
#             raise Exception()

#         save_to_file(jobs, text)
#         return send_file("downloadjobs.csv")
#     except:
#         return redirect("/")
