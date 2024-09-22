import streamlit as st
import io
import chardet
import hashlib
import fitz # type: ignore

from datetime import datetime
from langdetect import detect, DetectorFactory
from google_gemini import google_gemini_translate
from deep_translator import GoogleTranslator
from docx import Document # type: ignore

# Ensure consistency in language detection
DetectorFactory.seed = 0

st.set_page_config(
    page_title="The Avengers - AI Translator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 The Avengers - AI Translator")

# Use CSS to position the small subtitle text
st.markdown("""
            
    <style>
    .subtitle {
        position: absolute;
        top: -.65rem; 
        left: 4.55rem; 
        font-size: 1rem;
        color: gray;
    }
    </style>
            
    <div class="subtitle">Capture semantic meaning!</div>
            
    """, unsafe_allow_html=True)

# Create navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📑 Documents", "🔤 Text", "🤖 ChatBot", "📖 Blog", "💡 About Us"])

# Tab 1: Document translation
with tab1:
    col1, col2 = st.columns(2)

    # Select output language
    with col1:
        output_languages_list = [
            'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Azerbaijani', 'Bengali',
            'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese Simplified',
            'Chinese Traditional', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English',
            'Finnish', 'French', 'Georgian', 'German', 'Greek', 'Gujarati', 'Hausa',
            'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Italian',
            'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Korean', 'Kurdish', 'Lao',
            'Latvian', 'Lithuanian', 'Malay', 'Malayalam', 'Marathi', 'Nepali', 'Pashto',
            'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Romanian', 'Russian', 'Serbian',
            'Sinhala', 'Slovak', 'Somali', 'Spanish', 'Swahili', 'Swedish', 'Tagalog',
            'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese',
            'Yoruba', 'Zulu'
        ]

        output_language_tab1 = st.selectbox(label="Output language", options=output_languages_list, key="output_language_tab1")

    # File uploader
    with col2:
        uploaded_file = st.file_uploader("Supported file types: .txt, .docx, .pdf", type=["txt", "docx", "pdf"])

    # Add HTML and CSS to change the content
    st.markdown(
        """
        <style>
            .e1b2p2ww11 .e1bju1570::before {
                content: "Please note: We only accept text up to 1000 characters long: .txt, .docx, .pdf";
                font-size: 12px;
                color: white;
                font-family: 'Source Sans Pro', sans-serif;
                letter-spacing: 1px;
            }

            .e1b2p2ww11 .e1bju1570 {
                font-size: 0;
            }
        </style>
        """, unsafe_allow_html=True
    )

    if uploaded_file:
        if st.button("Translate",  key="translate_button_tab1"):
            if uploaded_file.name.endswith('.txt'):
                # Read file as binary
                file_bytes = uploaded_file.read()
                
                # Detect file encoding
                result = chardet.detect(file_bytes)
                encoding = result['encoding']
                
                # Decode file content using detected encoding
                file_contents = file_bytes.decode(encoding)

                # Limit the number of characters
                if len(file_contents) > 1000:
                    st.warning("Limit is 1000 characters.")
                    st.stop()  # Stop the program
                else:        
                    source_language = detect(file_contents)
                    language_mapping = {
                        "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
                        "Azerbaijani": "az", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
                        "Burmese": "my", "Catalan": "ca", "Cebuano": "ceb", "Chinese Simplified": "zh-CN",
                        "Chinese Traditional": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
                        "Dutch": "nl", "English": "en", "Finnish": "fi", "French": "fr", "Georgian": "ka",
                        "German": "de", "Greek": "el", "Gujarati": "gu", "Hausa": "ha", "Hebrew": "he",
                        "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id",
                        "Italian": "it", "Japanese": "ja", "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk",
                        "Korean": "ko", "Kurdish": "ku", "Lao": "lo", "Latvian": "lv", "Lithuanian": "lt",
                        "Malay": "ms", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Pashto": "ps",
                        "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
                        "Russian": "ru", "Serbian": "sr", "Sinhala": "si", "Slovak": "sk", "Somali": "so",
                        "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl", "Tamil": "ta",
                        "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
                        "Uzbek": "uz", "Vietnamese": "vi", "Yoruba": "yo", "Zulu": "zu"
                    }
                    target_language_code = language_mapping.get(output_language_tab1)

                    if source_language == target_language_code:
                        st.warning(f"The content you provided already in {output_language_tab1}.")
                        st.stop()  # Stop the program
                    else:
                        translated_text = google_gemini_translate(file_contents, None, target_language_code)
                        st.session_state.translated_text_tab1 = translated_text
            elif uploaded_file.name.endswith('.docx'):
                doc = Document(uploaded_file)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                text = '\n'.join(full_text)

                # Limit the number of characters
                if len(text) > 1000:
                    st.warning("Limit is 1000 characters.")
                    st.stop()  # Stop the program
                else:
                    source_language = detect(text)
                    language_mapping = {
                        "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
                        "Azerbaijani": "az", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
                        "Burmese": "my", "Catalan": "ca", "Cebuano": "ceb", "Chinese Simplified": "zh-CN",
                        "Chinese Traditional": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
                        "Dutch": "nl", "English": "en", "Finnish": "fi", "French": "fr", "Georgian": "ka",
                        "German": "de", "Greek": "el", "Gujarati": "gu", "Hausa": "ha", "Hebrew": "he",
                        "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id",
                        "Italian": "it", "Japanese": "ja", "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk",
                        "Korean": "ko", "Kurdish": "ku", "Lao": "lo", "Latvian": "lv", "Lithuanian": "lt",
                        "Malay": "ms", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Pashto": "ps",
                        "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
                        "Russian": "ru", "Serbian": "sr", "Sinhala": "si", "Slovak": "sk", "Somali": "so",
                        "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl", "Tamil": "ta",
                        "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
                        "Uzbek": "uz", "Vietnamese": "vi", "Yoruba": "yo", "Zulu": "zu"
                    }
                    target_language_code = language_mapping.get(output_language_tab1)
                    
                    if source_language == target_language_code:
                        st.warning(f"The content you provided is already in {output_language_tab1}.")
                        st.stop()  # Stop the program
                    else:
                        input_language = language_mapping.get(source_language)
                        output_language = language_mapping.get(target_language_code)

                        # Translate text using Google Translate API
                        translator = GoogleTranslator(source=source_language, target=target_language_code)
                        translated_text = translator.translate(text)
                        st.session_state.translated_text_tab1 = translated_text
                        # st.session_state.uploaded_file_type = 'docx'
            
            elif uploaded_file.name.endswith('.pdf'):
                # Extract text from the PDF
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                doc = fitz.open("temp.pdf")
                full_text = ""
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    full_text += page.get_text()

                # Limit the number of characters
                if len(full_text) > 1000:
                    st.warning("Limit is 1000 characters.")
                    st.stop()  # Stop the program
                else:
                    source_language = detect(full_text)
                    language_mapping = {
                        "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
                        "Azerbaijani": "az", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
                        "Burmese": "my", "Catalan": "ca", "Cebuano": "ceb", "Chinese Simplified": "zh-CN",
                        "Chinese Traditional": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
                        "Dutch": "nl", "English": "en", "Finnish": "fi", "French": "fr", "Georgian": "ka",
                        "German": "de", "Greek": "el", "Gujarati": "gu", "Hausa": "ha", "Hebrew": "he",
                        "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id",
                        "Italian": "it", "Japanese": "ja", "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk",
                        "Korean": "ko", "Kurdish": "ku", "Lao": "lo", "Latvian": "lv", "Lithuanian": "lt",
                        "Malay": "ms", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Pashto": "ps",
                        "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
                        "Russian": "ru", "Serbian": "sr", "Sinhala": "si", "Slovak": "sk", "Somali": "so",
                        "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl", "Tamil": "ta",
                        "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
                        "Uzbek": "uz", "Vietnamese": "vi", "Yoruba": "yo", "Zulu": "zu"
                    }
                    target_language_code = language_mapping.get(output_language_tab1)

                    if source_language == target_language_code:
                        st.warning(f"The content you provided is already in {output_language_tab1}.")
                        st.stop()  # Stop the program
                    else:
                        input_language = language_mapping.get(source_language)
                        output_language = language_mapping.get(target_language_code)

                        translator = GoogleTranslator(source=source_language, target=target_language_code)
                        translated_text = translator.translate(full_text)
                        st.session_state.translated_text_tab1 = translated_text
                
            else:   
                st.error("Please upload a file with the extension .txt, .docx, .pdf")

    # Display translated result
    if "translated_text_tab1" in st.session_state:
        if uploaded_file.name.endswith('.txt'):
            st.write("Translated content")
            st.success(st.session_state.translated_text_tab1)

            # Create file name based on current time hashed with MD5
            current_time = datetime.now().isoformat()
            md5_hash = hashlib.md5(current_time.encode()).hexdigest()
            file_name = f"{md5_hash}.txt"

            # Create .txt file for translated content and provide download link
            translated_text = st.session_state.translated_text_tab1
            buffer = io.BytesIO()
            buffer.write(translated_text.encode('utf-8'))
            buffer.seek(0)
            
            st.download_button(
                label="Download translation",
                data=buffer,
                file_name=file_name,
                mime="text/plain"
            )
        elif uploaded_file.name.endswith('.docx'):
            st.write("Translated content")
            st.success(st.session_state.translated_text_tab1)
            buffer = io.BytesIO()
            current_time = datetime.now().isoformat()
            md5_hash = hashlib.md5(current_time.encode()).hexdigest()
            file_name = f"{md5_hash}.docx"
            translated_text = st.session_state.translated_text_tab1
            doc = Document()
            doc.add_paragraph(translated_text)
            doc.save(buffer)
            mime_type = "application/msword"

            buffer.seek(0)
            st.download_button(
                label="Download translation",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
        elif uploaded_file.name.endswith('.pdf'):
            st.write("Translated content")
            st.success(st.session_state.translated_text_tab1)

            buffer = io.BytesIO()
            current_time = datetime.now().isoformat()
            md5_hash = hashlib.md5(current_time.encode()).hexdigest()
            file_name = f"{md5_hash}.docx"
            translated_text = st.session_state.translated_text_tab1
            doc = Document()
            doc.add_paragraph(translated_text)
            doc.save(buffer)
            mime_type = "application/msword"

            buffer.seek(0)
            st.download_button(
                label="Download translation",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
        else:
            st.write("Error")
                
# Tab 2: Text translation
with tab2:
    col_1, col_2 = st.columns(2)

    # Column for selecting input language
    with col_1:
        input_languages_list = [
            'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Azerbaijani', 'Bengali',
            'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese Simplified',
            'Chinese Traditional', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English',
            'Finnish', 'French', 'Georgian', 'German', 'Greek', 'Gujarati', 'Hausa',
            'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Italian',
            'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Korean', 'Kurdish', 'Lao',
            'Latvian', 'Lithuanian', 'Malay', 'Malayalam', 'Marathi', 'Nepali', 'Pashto',
            'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Romanian', 'Russian', 'Serbian',
            'Sinhala', 'Slovak', 'Somali', 'Spanish', 'Swahili', 'Swedish', 'Tagalog',
            'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese',
            'Yoruba', 'Zulu'
        ]
        input_language_tab2 = st.selectbox(label="Input language", options=input_languages_list, key="input_language_tab2")

    # Column for selecting output language
    with col_2:
        output_languages_list = [x for x in input_languages_list if x != input_language_tab2]
        output_language_tab2 = st.selectbox(label="Output language", options=output_languages_list)

    input_text_tab2 = st.text_area("Enter text here (up to 1000 characters)", key="input_text_tab2")

    if st.button("Translate"):
        if input_text_tab2.strip():
            if len(input_text_tab2) > 1000:
                st.warning("Limit is 1000 characters.")
                st.stop()  # Stop the program
            else:
                language_mapping = {
                    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
                    "Azerbaijani": "az", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
                    "Burmese": "my", "Catalan": "ca", "Cebuano": "ceb", "Chinese Simplified": "zh-CN",
                    "Chinese Traditional": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
                    "Dutch": "nl", "English": "en", "Finnish": "fi", "French": "fr", "Georgian": "ka",
                    "German": "de", "Greek": "el", "Gujarati": "gu", "Hausa": "ha", "Hebrew": "he",
                    "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id",
                    "Italian": "it", "Japanese": "ja", "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk",
                    "Korean": "ko", "Kurdish": "ku", "Lao": "lo", "Latvian": "lv", "Lithuanian": "lt",
                    "Malay": "ms", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Pashto": "ps",
                    "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
                    "Russian": "ru", "Serbian": "sr", "Sinhala": "si", "Slovak": "sk", "Somali": "so",
                    "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl", "Tamil": "ta",
                    "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
                    "Uzbek": "uz", "Vietnamese": "vi", "Yoruba": "yo", "Zulu": "zu"
                }               
                input_language = language_mapping.get(input_language_tab2)
                output_language = language_mapping.get(output_language_tab2)

                # Translate text using Google Translate API
                translator = GoogleTranslator(source=input_language, target=output_language)
                translated_text = translator.translate(input_text_tab2)
                st.session_state.translated_text_tab2 = translated_text
        else:
            st.warning("Please enter the text to be translated.")

    # Display translated result
    if "translated_text_tab2" in st.session_state:
        st.success(st.session_state.translated_text_tab2)

# Tab 3: ChatBot
with tab3:
    # Function to translate roles between Gemini-Pro and Streamlit's terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = []

    # Display chat history (older messages at the top)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_session:
        role = translate_role_for_streamlit(message['role'])
        with st.chat_message(role):
            st.markdown(f'<div class="chat-message">{message["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input field for user's message (always at the bottom)
    user_prompt = st.chat_input("Enter your question here...")

    if user_prompt:
        # Add user's message to chat and display it
        st.session_state.chat_session.append({"role": "user", "text": user_prompt})
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Google Gemini API and get response
        gemini_response = google_gemini_translate(user_prompt)
        st.session_state.chat_session.append({"role": "assistant", "text": gemini_response})
        st.chat_message("assistant").markdown(gemini_response)

with tab4:
    st.title("Techwiz 5 - GeoSpeak - Developed by The Avengers")
    st.subheader("Leveraging Gen AI for Smart solution of Translation: Geo-Speak Application")

    st.markdown(
    """
        Link: [The Avengers - AI Translator · Streamlit](https://theavengers.streamlit.app/)
    """)

    st.image("img/z5855806767554_aef51eacda4c36fd65660ce9ee04af64.jpg", width=50, use_column_width=True)

    st.markdown(
    """
        **Team: The Avengers** \n
        **List of members:** \n
        - Nguyễn Quốc Anh \n
        - Dương Gia Thành \n
        - Phạm Hoàng Tiến \n
        - Nguyễn Quốc Bảo \n
        - Trần Mai Phương \n
        - Lâm Kim Khánh

        **What is going on with Translation?**

        <p style="text-align: justify;">In the fast pace of world, it is common that people are breathing the cosmopolitan atmosphere, even companies. What does it mean? People have engaged in using in diverse languages more than ever before in their workplaces. They utilize languages or linguistic skills in reading and writing documents, listening to foreigners and especially speaking in a manner of responding actively to any information that is not of their “mother tongue” they received. To this point, some may think of many conventional translation tools as a solution which automatically translate any text that they input. It is fair enough to agree, but, the main point is that those tools are just simply doing the job of translation.</p>

        <p style="text-align: justify;">Take a closer look at the problem mentioned there, the “job” those conventional translation tools do is transferring words people input into a targeted language form without any consideration of context. It is just like users search for a vocabulary in a thick dictionary book and then use it, but maybe they do not understand how the word can be effectively use in the context they mean. It is about the problem of word choices. Those conventional tools may translate text accurately; however, it would cause difficulties of understanding the text or even misunderstandings. When it turns into the business context in which accuracy is the priority, the problem starts to arise.  People may find it hard to read many technical documents or even communicate about technical problems with many foreign experts. The sufficient flow of information exchange can be a result afterwards. One of problems related to reading technical documents of computer science fields, it is obvious that the same word can have different meanings.</p>

        <p style="text-align: justify;">Given those problems, we, human-beings, starts to think of something smarter and more sophisticated in providing translation service with a good combination of contextual awareness and linguistic profession. Therefore, Gemini's Large language Model and Generative AI (Gen AI) are utilized in developing a translation solution, called Geo-Speak.</p>

        **What is Geo-Speak?**

        <p style="text-align: justify;">To tackle issues in the language use, an application, called Geo-Speak, is innovated, aiming to address the limitations of traditional translation methods and the increasing complexity of language usage across diverse domains. By applying Gemini's Large Language Models (LLMs) and Generative AI (Gen AI), Geo-Speak are likely to interpret and translate text in manners of combining the contextual factors and academic linguistics. This application is essential for diplomacy, global business, education, and so on, where precise communication can significantly affect the outcomes. Hence, users are able to overcome language barriers, facilitate cross-cultural understanding, and ensure the smooth flow of information exchanging regardless of personal background or linguistic profession.</p>
        
    """, unsafe_allow_html=True)
    
    st.image("img/z5855785979880_853b682305e933c24c9e8eae5c40f52e.jpg", width=50, use_column_width=True)

    st.markdown(
    """
        <p style="text-align: justify;">Geo-Speak is a sophisticated real-time web application providing translating services. It is worth to mention that its design is the utilization of cutting-edge AI technologies, particularly a cloud-based Large Language Model, to deliver effective and efficient communication across diverse languages. Not only it enables users overcome the language barriers, but also take contextual sensitiveness into consideration to ensure the flow of information exchanging. It is fair to say that Geo-Speak is a human-kind leap for a context in which people have to adapt to future expansion involved in multinational and multilingual working environments quickly. By leveraging Gemini’s models, which specializes in language comprehension and generation. This solution offers real-time translations that are more accurate and contextually sensitive compared to the conventional methods. Therefore, Geo-Speak can potentially enhance cross-language communication in diverse workplace settings, being indispensable in businesses. </p>

        **How the Geo-Speak Application works?**

        **There are two main phrases performed by the Geo-Speak application:**

        <p style="text-align: justify;">At first, users inputs text or text file (.txt, .docx, .pdf extension) in any language forms and choose the desired target language from a drop-down list provided in the web interface. The Embedding API accesses the input information. At this stage, the application use constraints, related to word limitations and extension of a file to check if the file or text is qualified enough to process the further steps. Particularly, in this project, my team set 1000 words as the limitation and “.txt, .docx, .pdf” extension for the standard of file format. Once verified, the input information will be decoded into a high-dimensional embedding vector that captures its semantic essence. This vector is then used to query a vector Database containing precomputed embeddings of parallel corporate or translation sample. The system extracts relevant documents that closely aligned with the source text embedding, comprising paired texts in both source and target languages to guide the translation process. </p>
    """, unsafe_allow_html=True)

    st.image("img/z5855786203327_f6ec2b25a2b6acbed2fdbaabd8c6de88.jpg", width=50, use_column_width=True)

    st.markdown(
    """
        <p style="text-align: justify;">In the second phrase, the application transfers those data to Google Gemini API for translating process. The translated text is sent back to the users afterwards in a text or text file which is available for reading or downloading.</p>

        **Technologies and Tools in building Geo-Speak**

        <p style="text-align: justify;">To build Geo-Speak application, we start from scratches that maybe most people find themselves common with terms.</p>
    """, unsafe_allow_html=True)

    st.image("img/z5855785794142_784584c673ba215f438c3d5329e4ed59.jpg", width=50, use_column_width=True)

    st.markdown(
    """
        <p style="text-align: justify;">For the use of Programming Languages, Python would be smart options. Python will do the jobs of backend development, data processing and integration with AI and natural language toolkit libraries. Meanwhile, HTML and CSS is used for jobs of front-end development, interactivity and user interface design. Relatively, Frameworks of Python can be used along with developing responsive and interactive user interfaces.</p>

        <p style="text-align: justify;">For User Interface Design, developers can use HTML and CSS for building responsive and visually appealing user interface of website.</p>

        <p style="text-align: justify;">For Translation APIs, we can utilize which already have before, such as Google Cloud Translation API, Google Gemini API, for integrating neural machine translation capabilities into the application.</p>

        **Real-world Applications of Geo-Speak in business communications**

        <p style="text-align: justify;">Above is all you need to know about Geo-Speak application, It is time to look at this tool from business aspects to have a comprehensive understanding of the reasons we may need it.</p>
    """, unsafe_allow_html=True)

    st.image("img/tumblr_d5dff37917648d2f077d1971bc3335ce_8c896f3e_500.jpg", width=50, use_column_width=True)

    st.markdown(
    """
        <p style="text-align: justify;">In E-commerce industry, Online retailers definitely want to expand their brand name and products across countries over the world. The presence of Geo-Speak is useful for providing multilingual customers with sophisticated supports, product descriptions, and also checkout processes. From there, it fosters the better shopping experience.</p>

        <p style="text-align: justify;">For Travel and tourism industry, it is not necessary to explain the role of language anymore. Travel agencies, local businesses, like accommodation, restaurants, or tour guide services need to be specialized in using languages naturally more than any industries. Geo-Speak would help in offering real-time language assistance throughout the customer journeys.</p>

        <p style="text-align: justify;">For Legal and Compliance areas, corporation have to deal with laws across borders. Speaking of this context, strict word choices and comprehensive understandings of words’ meanings would form language barriers for them when they want to expand oversea. Therefore, Geo-Speak with high level of translation accuracy can facilitate the process of conducting documents, contracts, and compliance materials effectively.</p>

        <p style="text-align: justify;">There are still many areas to be mentioned to demonstrate the usefulness of this sophisticated Application.</p>
    """, unsafe_allow_html=True)

# Tab 5: About Us
with tab5:
    col1, col2, col3 = st.columns(3)

    with col2:
        st.image("img/z5855663862790_aa6a77c21ae95ad7f83fb3eccb262482.jpg", width=50,  caption="The Avengers Team", use_column_width=True)

    st.write(
        """
        **ABOUT US** \n
        The Avengers - AI Translator is a text/file translation and chatbot support using GenAI technology.
        
        **THE AVENGERS - AI TRANSLATOR PROJECT MEMBERS**
        - Dương Gia Thành: Main Developer
        - Nguyễn Quốc Anh: Project Manager
        - Other members:
            - Nguyễn Quốc Bảo
            - Phạm Hoàng Tiến
            - Trần Mai Phương
            - Lâm Kim Khánh

        - Project website - [Visit here](https://theavengers.streamlit.app/)

        **CONTACT**
        - Dương Gia Thành: [duonggiathanh3819@gmail.com](mailto:duonggiathanh3819@gmail.com)
        - Nguyễn Quốc Anh: [anh.datascience@gmail.com](mailto:anh.datascience@gmail.com)
        """
    )

