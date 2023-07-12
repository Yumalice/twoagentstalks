# coding: utf-8

import time
import tvml
import pydub
from pydub import AudioSegment
from gtts import gTTS 

wavPath   = 'C:/Users/thevo/Documents/TVML関係/TVML/Datafiles/Sound/'

#-------------------------------------------------
# mkVoice
#-------------------------------------------------
def mkVoice(inText):
	gTTS(text=inText, lang='en', slow=False).save("C:/Users/thevo/Documents/TVML関係/TVML/Datafiles/Sound/inText.mp3")
	time.sleep(0.5)

	sound = pydub.AudioSegment.from_mp3("C:/Users/thevo/Documents/TVML関係/TVML/Datafiles/Sound/inText.mp3")
	sound = sound.set_frame_rate(44100)
	sound.export(wavPath+"output.wav", format="wav")
	time.sleep(0.5)

#-------------------------------------------------
# main
#-------------------------------------------------
def main():

	#----------------------------------
	# TVIF経由でAnimeViewerに接続
	#----------------------------------
	if tvml.connectAnimeViewerByTvif( ) == False:
		print('error:tvifConnect')
		exit()
	else:
		print('success:tvifConnect')

	#----------------------------------
	# AnimeViewerのWindowサイズ設定
	#----------------------------------
	if tvml.sendSetWindowSize( 820 , 640 ) == False:
		print('error:tvifSetWindowSize')
	else:
		print('success:tvifSetWindowSize')
	time.sleep(0.5)

	#----------------------------------
	# リセットコマンドの送信
	#----------------------------------
	if tvml.sendSetCommand( tvml.TVP_RESET, 100, ) == False:
		print('error:tvifReset')
		tvml.disconnectAnimeViewerByTvif();
		exit()
	else:
		print('success:tvmlReset')

	#----------------------------------
	# ファイルの内容をAnimeViewerに送信
	#----------------------------------
	sf = 'setting2.tvml'
	if tvml.sendScriptFileByTvif( sf ) == False:
		print('error:sendScriptFileByTvif')
	else:
		print('success:sendScriptFileByTvif')

	#----------------------------------
	# 自己紹介
	#----------------------------------
	time.sleep(1.0)
	sc = 'character: talk( name=CharacterA, text="こんにちは、ナビゲーターのマイです。", emotion=normal )'
	tvml.sendScriptByTvif( sc )

	#----------------------------------
	# 目的を説明する
	#----------------------------------
	sc = 'character: talk( name=CharacterA, text="今日は、英語音声の再生を行ないたいと思います。", emotion=normal )'
	tvml.sendScriptByTvif( sc )
	time.sleep(1.0)

	sc = 'character: talk( name=CharacterA, text="それでは再生します。", emotion=normal )'
	tvml.sendScriptByTvif( sc )

	#----------------------------------
	# 音声再生
	#----------------------------------
	text = "I'm kinuta.I'm so happy to meet you today."
	mkVoice(text)

	sc = 'character: talkfile( name=CharacterB, filename="C:/Users/thevo/Documents/TVML関係/TVML/Datafiles/Sound/output.wav", emotion=excite)'
	tvml.sendScriptByTvif( sc )

	time.sleep(4.0)

	#----------------------------------
	# 終了の挨拶
	#----------------------------------
	time.sleep(1.0)
	sc = 'character: talk( name=CharacterA, text="よい発音でしたね。", emotion=normal )'
	tvml.sendScriptByTvif( sc )

	sc = 'character: talk( name=CharacterA, text="またお会いしましょう。", emotion=normal )'
	tvml.sendScriptByTvif( sc )

	sc = 'character: byebye( name=CharacterA, hand=right, wait=no, speed=1.2)'
	tvml.sendScriptByTvif( sc )
	sc = 'character: byebye( name=CharacterB, hand=right, wait=no, speed=1.2)'
	tvml.sendScriptByTvif( sc )

	sc = 'super: off()'
	tvml.sendScriptByTvif( sc )

	#----------------------------------
	# TVIF経由でのAnimeViewer接続を解除
	#----------------------------------
	tvml.disconnectAnimeViewerByTvif()

#-----------------------------------------------------------------------------
# Start up
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
