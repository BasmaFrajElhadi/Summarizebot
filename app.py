import streamlit as st
from txtai.pipeline import Summary,Transcription
from PyPDF2 import PdfReader
import whisper

st.set_page_config(page_title="Summarize what you want", page_icon="🧊")
with open('main.css') as cssFile:
    st.markdown(f'<style>{cssFile.read()}</style>', unsafe_allow_html=True)
#to save audio and documents in folder
def saveResource(resource , path):
    with open(path, "wb") as f:
        f.write(resource.getbuffer()) 
    return path   

@st.cache_resource
def summerizeText(text):
    summery = Summary()
    text = (text)
    result = summery(text)
    return result

# extract text from the Pdf file using PyPDF2 
def extractTxtFromPdf(filePath):
    text = ""
    with open(filePath,'rb') as file:
        reader = PdfReader(file)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text += page.extract_text()
    return text

# extract text from the Audio file using whisper 
@st.cache_resource
def extractTxtFromAudio(audioPath):
    model = whisper.load_model("base")
    result = model.transcribe(audioPath)
    return result["text"]



sidebar = st.sidebar
choice = sidebar.selectbox("Select what you want to summarize",["Summerize Text","Summerize Documnet","Summerize Audio"])

st.subheader(f"Your Are {choice}")
if choice == "Summerize Text":
    inputText = st.text_area("Enter your text")
    if inputText is not None:
        if st.button("Summerize text"):
            col1,col2 = st.columns([1,1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(inputText)
            with col2:
                summaryResult = summerizeText(inputText)
                st.markdown("**Summerize Text**")
                st.success(summaryResult)
elif choice == "Summerize Documnet":
    inputDoc = st.file_uploader("Upload Your Document" , type=["pdf"])
    if inputDoc is not None:
        if st.button("Summerize document"):
            # save file in Document folder
            filePath = saveResource(inputDoc , './documents/' + inputDoc.name)
            extractText = extractTxtFromPdf(filePath)
            col1,col2 = st.columns([1,1])
            with col1:
                st.markdown("**Extracted Text**")
                st.info(extractText)
            with col2:
                summaryResult = summerizeText(extractText)
                st.markdown("**Summerize Text**")
                st.success(summaryResult)
elif choice == "Summerize Audio":
        inputAudio = st.file_uploader("Upload Your Audio" , type=["mp3","wav","wma"])
        if inputAudio is not None:
            if st.button("Summerize Audio"):
                # save file in Audios folder
                AudioPath = saveResource(inputAudio , './Audios/' + inputAudio.name)
                extractText = extractTxtFromAudio(AudioPath)
                col1,col2 = st.columns([1,1])
                with col1:
                    st.markdown("**Extracted Text**")
                    st.info(extractText)
                with col2:
                    summaryResult = summerizeText(extractText)
                    st.markdown("**Summerize Text**")
                    st.success(summaryResult)