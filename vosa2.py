# coding: utf-8

import time
import tvml
import pydub
from pydub import AudioSegment
from gtts import gTTS 

import win32com.client

sapi = win32com.client.Dispatch("SAPI.SpVoice")
cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft David"]

wavPath = 'C:/Users/thevo/Documents/TVML関係/TVML/Datafiles/Sound/'
#wavPath = 'C:\Users\thevo\Documents\TVML関係\TVML\Datafiles\Sound\'


#-------------------------------------------------
# mkVoice
#-------------------------------------------------
def mkVoice(inText):
	if v:
		fs = win32com.client.Dispatch("SAPI.SpFileStream")
		fs.Open(wavPath+"output.wav", 3)
		sapi.AudioOutputStream = fs
		oldv = sapi.Voice
		sapi.Rate = -2
		sapi.Voice = v[0]
		sapi.Speak(inText)
		sapi.Voice = oldv
		fs.Close()

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
	if tvml.sendSetWindowSize( 920, 640 ) == False:
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
	# sf = 'setting.tvml' 今回は２名のAgent
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
	text = "I'm David."
	mkVoice(text)

	sc = 'character: talkfile( name=CharacterB, filename="Sound/output.wav", emotion=excite)'
	tvml.sendScriptByTvif( sc )
	time.sleep(3.0)

	text = "I'm so happy to meet you today."
	mkVoice(text)

	sc = 'character: talkfile( name=CharacterB, filename="Sound/output.wav", emotion=excite)'
	tvml.sendScriptByTvif( sc )
	time.sleep(3.0)

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
