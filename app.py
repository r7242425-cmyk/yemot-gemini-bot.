import os
from flask import Flask, request
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None


@app.route("/")
def home():
  if not api_key:
    return "השרת עובד, אך חסר מפתח GEMINI_API_KEY בהגדרות!"
  return "השרת של נתנאל עובד ב-Render עם Gemini וימות המשיח!"


@app.route("/ivr", methods=["GET", "POST"])
def ivr_bot():
  if not client:
    return "id_list_message=t-שגיאת מערכת, לא הוגדר מפתח."

  user_text = (
      request.args.get("text", "")
      or request.form.get("text", "")
      or request.args.get("voice_text", "")
  )

  if not user_text:
    return "id_list_message=t-שלום, לא נקלט טקסט להעברה."

  try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=user_text,
    )
    bot_reply = response.text.strip().replace("\n", " ")
    return f"id_list_message=t-{bot_reply}"
  except Exception as e:
    return f"id_list_message=t-שגיאה בפנייה לג'מיני: {str(e)}"


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
