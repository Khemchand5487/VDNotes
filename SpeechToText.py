import json
from ibm_watson import SpeechToTextV1, ApiException
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment # pip install pydub
from pydub.silence import split_on_silence
import os


# Insert API Key in place of
# 'YOUR UNIQUE API KEY'
authenticator = IAMAuthenticator('VDaPOy8P4vkWgXHiWLJqOLEqkSHprTcDL2iny_uIw1Uf')
service = SpeechToTextV1(authenticator=authenticator)

# Insert URL in place of 'API_URL'
service.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/ba00ae65-b873-412e-9d22-a3624856b06f')


 

# a function that splits the audio file into chunks 
# and applies speech recognition 
def silence_based_conversion(path = r"E:\My Projects\COVID-19 Video to Text\data\audio.wav"): 

	# open the audio file stored in 
	# the local system as a wav file. 
	voice = AudioSegment.from_wav(path) 

	# open a file where we will concatenate 
	# and store the recognized text 
	fh = open("recognized.txt", "w+") 
		
	# split track where silence is 0.5 seconds 
	# or more and get chunks 
	chunks = split_on_silence(voice,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = voice.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    ) 

	# create a directory to store the audio chunks. 
	try: 
		os.mkdir('audio_chunks') 
	except(FileExistsError): 
		pass

	# move into the directory to 
	# store the audio files. 
	os.chdir('audio_chunks') 

	i = 0
	# process each chunk 
	for chunk in chunks: 
			
		# Create 0.5 seconds silence chunk 
		chunk_silent = AudioSegment.silent(duration = 10) 

		# add 0.5 sec silence to beginning and 
		# end of audio chunk. This is done so that 
		# it doesn't seem abruptly sliced. 
		audio_chunk = chunk_silent + chunk + chunk_silent 

		# export audio chunk and save it in 
		# the current directory. 
		print("saving chunk{0}.wav".format(i)) 
		# specify the bitrate to be 192 k 
		audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 

		# the name of the newly created chunk 
		filename = 'chunk'+str(i)+'.wav'

		print("Processing chunk "+str(i)) 

		# get the name of the newly created chunk 
		# in the AUDIO_FILE variable for later use. 
		file = filename 
		# try converting it to text 
		rec = audio_to_text(file)
		if rec == "Error5487":
			return "Error5487E"
		# write the output to the file. 
		fh.write(rec+" ")

		os.remove(filename)
		i += 1
	fh.close()
	os.chdir('..') 




# Insert local mp3 file path in
# place of 'LOCAL FILE PATH'
def audio_to_text(file_path):
	with open(os.path.join(os.path.dirname('__file__'), file_path),'rb') as audio_file:
		try:
		    dic = json.loads(
		        json.dumps(
		            service.recognize(
			                audio=audio_file,
			                content_type='audio/wav',
			                model='en-US_BroadbandModel',
			                continuous=True,
			                smart_formatting=True).get_result(), indent=2))
		except ApiException as ex:
			raise ValueError("There is an error!")
	try:
		return dic["results"][0]["alternatives"][0]["transcript"]
	except: return ""



# import speech_recognition as sr

# r = sr.Recognizer()
# mic = sr.Microphone()

# print('Recording...')
# with mic as source:
#     audio = r.listen(source)

# with open("audio_file.wav", "wb") as file:
#     file.write(audio.get_wav_data())
# #silence_based_conversion()