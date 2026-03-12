from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from main.models import Assessment
from django.utils import timezone
import google.generativeai as genai
from django.conf import settings
from .models import ChatSession, ChatMessage

# Configure Gemini for speed
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
)





def chat_page(request):
    if 'chat_session_id' in request.session:
        del request.session['chat_session_id']
    return render(request, 'chatbot/chat.html', {'history': []})

def chat_health(request):
    print(">>> HEALTH CHECK HIT", flush=True)
    return JsonResponse({'status': 'ok', 'message': 'NEXO Server is Alive'})



@csrf_exempt
def chat_api(request):
    print(">>> CHAT API REQUEST RECEIVED", flush=True)
    if request.method == 'POST':
        try:
            try:
                data = json.loads(request.body)
                message = data.get('message', '')
            except json.JSONDecodeError:
                print(">>> JSON DECODE ERROR", flush=True)
                return JsonResponse({'reply': "Internal Error: Malformed JSON sent to server."}, status=400)
            
            print(f">>> Message content: {message[:50]}...", flush=True)
            if not message:
                return JsonResponse({'reply': "I didn't catch that. Could you repeat?"})



            # Get or Create Session
            session_id = request.session.get('chat_session_id')
            if session_id:
                try:
                    session = ChatSession.objects.get(id=session_id)
                except ChatSession.DoesNotExist:
                    session = ChatSession.objects.create(user=request.user if request.user.is_authenticated else None)
            else:
                session = ChatSession.objects.create(user=request.user if request.user.is_authenticated else None)
                request.session['chat_session_id'] = session.id

            # Save User Message
            ChatMessage.objects.create(session=session, role='user', content=message)
            
            # Fetch History for Context (Last 10 messages)
            history_objs = session.messages.all().order_by('-timestamp')[:10]
            history_objs = reversed(history_objs)
            history_text = "\n".join([f"{m.role.capitalize()}: {m.content}" for m in history_objs])

            # Context for Gemini
            upcoming = Assessment.objects.filter(deadline__gte=timezone.now()).order_by('deadline')[:5]
            assessments_context = "Upcoming Assessments: " + ", ".join([f"{a.title} (due {a.deadline.strftime('%b %d')})" for a in upcoming]) if upcoming else "No upcoming assessments."
            
            system_prompt = f"""
            You are 'NEXO Bot', the intelligent assistant for the NEXO Student-Teacher Management System.
            Your goal is to help students and teachers with their questions.
            
            Platform Context:
            - NEXO allows teachers to upload notes, post instructions, and create assessments.
            - Students can download notes, view instructions, and submit assessments.
            - {assessments_context}
            
            Conversation History:
            {history_text}
            
            Instructions:
            - Be professional, helpful, and concise.
            - Use emojis to keep the conversation friendly.
            - If asked about homework or exams, use the 'Platform Context' provided above.
            - Remember previous context from 'Conversation History'.
            """
            
            try:
                # Use Gemini for response
                print(">>> STARTING GEMINI GENERATION...", flush=True)
                response = model.generate_content([system_prompt, message])
                reply = response.text
                print(f">>> GEMINI SUCCESS. Response: {reply[:50]}...", flush=True)
                
                # Save Bot Message (Non-blocking ideally, but here simple)
                ChatMessage.objects.create(session=session, role='bot', content=reply)
            except Exception as gemini_err:
                print(f">>> GEMINI ERROR: {str(gemini_err)}", flush=True)

                # Fallback to simple logic if API fails or key is missing
                if 'homework' in message.lower() or 'assessment' in message.lower():
                    reply = f"I'm having trouble connecting to my brain, but I know you have these: {assessments_context} 🍀"
                else:
                    reply = "I'm NEXO Bot! I'm currently having some technical trouble reaching my AI core, but I'm here to help with your studies! 🤖"

            print(">>> SENDING JSON RESPONSE BACK TO FRONTEND")
            return JsonResponse({'reply': reply})

        except Exception as e:
            msg = f"Error processing request: {str(e)}"
            print(f">>> CRITICAL VIEW ERROR: {msg}")
            return JsonResponse({'reply': msg}, status=400)

    
    return JsonResponse({'reply': "Invalid request method."}, status=405)

def clear_chat_session(request):
    if 'chat_session_id' in request.session:
        del request.session['chat_session_id']
    return redirect('chatbot:chat_page')

