import pyttsx3
import PyPDF2
import pyaudio

book = open('sample.pdf','rb')
Reader = PyPDF2.PdfFileReader(book)
pages = Reader.numPages
print(pages)

speaker = pyttsx3.init()
print("playing...")
page = Reader.getPage(0)
text = page.extractText()
speaker.say(text)
speaker.runAndWait()