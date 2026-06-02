from flask import Flask, jsonify, request
import requests
import hashlib
import json

def stringToMD5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    md5_digest = md5.hexdigest()
    return md5_digest

app = Flask(__name__)

@app.route('/chapters/phigros', methods=['GET'])
def _chaptersPhigros():
    try:
        chartsInfoJSON = requests.get("https://raw.githubusercontent.com/RhythmActions/PhigrosActions/refs/heads/main/GameInformation/Modified_Gameinfo.json").json()
        allSongs = chartsInfoJSON["allSongs"]
        processedSongsInfo = []
        for song in allSongs:
            songInfo = chartsInfoJSON["regularSongs"][song]
            songName = songInfo["songsName"]
            songComposer = songInfo["composer"]
            songIllustrator = songInfo["illustrator"]
            songLevels = songInfo["chartDetail"]["level_list"]
            songBPM = 0
            songID = 'r'+stringToMD5(song.split('.0')[0])
            processedChartsInfo = []
            for chartLevel in songLevels:
                difficulty = songInfo["chartDetail"][chartLevel]["rating"]
                try:
                    difficulty = int(float(difficulty))
                except:
                    pass
                chartInfo = {
                    "id": f"{songID}{chartLevel}",
                    "song": songID,
                    "charter": songInfo["chartDetail"][chartLevel]["charter"],
                    "chart": f"https://raw.githubusercontent.com/7aGiven/Phigros_Resource/refs/heads/chart/{song}/{chartLevel}.json",
                    "level": chartLevel,
                    "difficulty": difficulty,
                    "ranked": False,
                    "notes": songInfo["chartDetail"][chartLevel]["numOfNotes"]
                }
                processedChartsInfo.append(chartInfo)
            processedSongInfo = {
                "id": songID,
                "charts": processedChartsInfo,
                "composer": songComposer,
                "illustrator": songIllustrator,
                "name": songName,
                "song": "https://raw.githubusercontent.com/7aGiven/Phigros_Resource/refs/heads/music/"+song.split('.0')[0]+".ogg",
                "edition": "Phigros Official Charts",
                "illustration": "https://raw.githubusercontent.com/7aGiven/Phigros_Resource/refs/heads/illustrationLowRes/"+song.split('.0')[0]+".png",
                "bpm": songBPM,
                "duration": "",
                "preview_start": "00:00:00"
            }
            processedSongsInfo.append(processedSongInfo)
        chapterInfo = {
            "count": len(processedSongsInfo),
            "next": None,
            "previous": None,
            "results": processedSongsInfo
        }
        return jsonify(chapterInfo)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v', methods=['GET'])
def _ver():
    return requests.get("https://raw.githubusercontent.com/RhythmActions/PhigrosActions/refs/heads/main/status.json").json()['version']

