import logging
import os
import io
import asyncio
import wave
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv
from pydub import AudioSegment

# -----------------------------
# تحميل المتغيرات من .env
# -----------------------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# التحقق من وجود المفاتيح
if not TELEGRAM_BOT_TOKEN:
    logging.error("❌ TELEGRAM_BOT_TOKEN is not set.")
    raise ValueError("❌ تأكد من وضع TELEGRAM_BOT_TOKEN في ملف .env")

if not GEMINI_API_KEY:
    logging.error("❌ GEMINI_API_KEY is not set.")
    raise ValueError("❌ تأكد من وضع GEMINI_API_KEY في ملف .env")

# -----------------------------
# إعداد Logging
# -----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------
# إعداد Gemini
# -----------------------------
genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel("gemini-1.5-flash")
tts_model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-tts")
image_model = genai.GenerativeModel(model_name="gemini-2.0-flash-preview-image-generation")
transcription_model = genai.GenerativeModel("gemini-1.5-pro-latest")

# -----------------------------
# برومبت البوت الاحترافي
# -----------------------------
PROFESSIONAL_PROMPT = """
أنت الآن تعمل كبوت مساعد ذكي للغاية، متعدد المجالات، وودي، يمكنه التحدث بالعربية بطلاقة.
هدفك هو مساعدة المستخدمين بأفضل طريقة ممكنة، مع تقديم إجابات دقيقة وواضحة.
"""

# -----------------------------
# دوال البوت
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إضافة البرومبت الاحترافي كجزء من تاريخ المحادثة
    context.user_data['chat_history'] = [{"role": "user", "parts": [{"text": PROFESSIONAL_PROMPT}]}]
    await update.message.reply_text(
        "👋 أهلاً بك! أنا بوت يعمل بالذكاء الاصطناعي (Gemini).\n"
        "أرسل لي أي رسالة نصية أو صوتية وسأرد عليك.\n"
        "يمكنك أيضًا استخدام الأمر /image لإنشاء صور أو /clear لمسح المحادثة."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ أوامر البوت:\n"
        "/start - بدء البوت\n"
        "/help - عرض الأوامر\n"
        "/image [وصف الصورة] - لإنشاء صورة بالذكاء الاصطناعي\n"
        "/clear - لمسح سجل المحادثة"
    )

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['chat_history'] = []
    await update.message.reply_text("✅ تم مسح سجل المحادثة.")

# -----------------------------
# تحويل النص إلى صوت WAV
# -----------------------------
async def convert_text_to_wav(text: str) -> io.BytesIO:
    try:
        generation_config = genai.types.GenerationConfig(
            speech_config=genai.types.SpeechConfig(
                voice_config=genai.types.VoiceConfig(
                    prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            )
        )
        response = await asyncio.to_thread(
            tts_model.generate_content,
            contents=[{"parts": [{"text": text}]}],
            generation_config=generation_config
        )
        if not response.candidates:
            logger.error("❌ Gemini TTS returned no candidates")
            return None
        
        audio_part = next((p for p in response.candidates[0].content.parts if "inlineData" in p), None)
        if not audio_part:
            logger.error("❌ Gemini TTS returned no audio data")
            return None

        audio_data = base64.b64decode(audio_part.inlineData.data)
        audio_segment = AudioSegment(
            data=audio_data,
            sample_width=2,
            frame_rate=24000,
            channels=1
        )
        audio_stream = io.BytesIO()
        audio_segment.export(audio_stream, format="wav")
        audio_stream.seek(0)
        return audio_stream
    except Exception as e:
        logger.error(f"❌ TTS error: {e}")
        return None

# -----------------------------
# توليد الصور
# -----------------------------
async def _generate_and_send_image(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str):
    if not prompt:
        await update.message.reply_text("🤔 من فضلك أرسل وصفًا للصورة.")
        return
    try:
        await update.message.reply_text("⏳ جاري إنشاء الصورة...")
        full_prompt = f"generate a creative and imaginative image: {prompt}"
        image_response = await asyncio.to_thread(
            image_model.generate_content,
            contents=[{"parts": [{"text": full_prompt}]}],
            response_modalities=["IMAGE", "TEXT"]
        )
        if not image_response.candidates:
            await update.message.reply_text("❌ لم أستطع توليد الصورة.")
            return

        image_part = next((p for p in image_response.candidates[0].content.parts if "inlineData" in p), None)
        if not image_part:
            await update.message.reply_text("❌ لم أستطع استخراج بيانات الصورة.")
            return
        
        image_data = base64.b64decode(image_part.inlineData.data)
        await update.message.reply_photo(photo=io.BytesIO(image_data), caption="✅ تم إنشاء الصورة!")
    except Exception as e:
        logger.error(f"❌ Image generation error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء توليد الصورة.")

async def handle_image_generation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    await _generate_and_send_image(update, context, prompt)

# -----------------------------
# معالجة النصوص
# -----------------------------
async def process_text_and_respond(update: Update, context: ContextTypes.DEFAULT_TYPE, user_text: str):
    try:
        # Initialize chat_history if it doesn't exist
        if 'chat_history' not in context.user_data:
            context.user_data['chat_history'] = [{"role": "user", "parts": [{"text": PROFESSIONAL_PROMPT}]}]
        
        chat_history = context.user_data['chat_history']
        
        # Start a new chat session with the current history
        chat_session = text_model.start_chat(history=chat_history)
        
        # Send the user's message to the model
        text_response = await asyncio.to_thread(chat_session.send_message, user_text)
        
        if text_response.candidates and text_response.candidates[0].content.parts:
            bot_reply = text_response.candidates[0].content.parts[0].text
            # Append the user and model messages to the history for context
            chat_history.append({"role": "user", "parts": [{"text": user_text}]})
            chat_history.append({"role": "model", "parts": [{"text": bot_reply}]})
        else:
            bot_reply = "🤖 لم أستطع توليد رد مناسب."

        await update.message.reply_text(bot_reply)
        audio_stream = await convert_text_to_wav(bot_reply)
        if audio_stream:
            await update.message.reply_voice(voice=audio_stream)
    except Exception as e:
        logger.error(f"❌ Text processing error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء معالجة النص.")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    image_keywords = ["انشئ صورة", "ارسم", "صورة", "توليد صورة", "انشاء صورة"]
    for keyword in image_keywords:
        if keyword in user_message:
            prompt = user_message.replace(keyword, "", 1).strip()
            await _generate_and_send_image(update, context, prompt)
            return
    await process_text_and_respond(update, context, user_message)

# -----------------------------
# معالجة الرسائل الصوتية
# -----------------------------
async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        processing_message = await update.message.reply_text("⏳ جاري تحويل الرسالة الصوتية إلى نص...")
        
        file_id = update.message.voice.file_id
        voice_file = await context.bot.get_file(file_id)
        voice_data = await voice_file.download_as_bytearray()
        voice_stream = io.BytesIO(voice_data)
        
        audio_segment = AudioSegment.from_file(voice_stream, format="ogg")
        wav_stream = io.BytesIO()
        audio_segment.export(wav_stream, format="wav")
        wav_stream.seek(0)
        
        audio_part = {
            "mime_type": "audio/wav",
            "data": base64.b64encode(wav_stream.read()).decode('utf-8')
        }
        
        transcription_prompt = [{"audio": audio_part}]
        transcription_response = await asyncio.to_thread(transcription_model.generate_content, transcription_prompt)
        
        if transcription_response.candidates and transcription_response.candidates[0].content.parts:
            transcribed_text = transcription_response.candidates[0].content.parts[0].text
            logger.info(f"✅ Transcribed text: {transcribed_text}")
            
            await context.bot.edit_message_text(
                chat_id=processing_message.chat_id,
                message_id=processing_message.message_id,
                text=f"✅ تم تحويل الصوت إلى نص: {transcribed_text}"
            )
            
            await process_text_and_respond(update, context, transcribed_text)
        else:
            await context.bot.edit_message_text(
                chat_id=processing_message.chat_id,
                message_id=processing_message.message_id,
                text="❌ لم أستطع فهم الرسالة الصوتية."
            )
            
    except Exception as e:
        logger.error(f"❌ Voice processing error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء معالجة الرسالة الصوتية.")

# -----------------------------
# تشغيل البوت
# -----------------------------
def main():
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("clear", clear_command))
        app.add_handler(CommandHandler("image", handle_image_generation))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
        logger.info("✅ البوت يعمل الآن ...")
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ Bot startup error: {e}")

if __name__ == "__main__":
    main()