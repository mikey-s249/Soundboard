from pydub import AudioSegment
from pydub.playback import play, _play_with_pyaudio, _play_with_simpleaudio
from pydub.utils import ratio_to_db
import csv
import threading
import pyaudio
from math import ceil
# song = AudioSegment.from_mp3("Sounds/Grant.mp3")

# backwards = song.reverse
# play(backwards)

FIELD_NAMES = ["id", "file", "name", "volume", "reversed", "splice1", "splice2"]

USE_SPECIAL_PLAY = False

class Soundboard():
    def __init__(self):
        self.sounds = []
        for i in range(25):
            self.sounds.append(None)

    def loadChanges(self):
        # Read CSV and load each change into sound object
        with open("SoundData.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    AudioSegment.from_mp3(row["file"])
                    sound = Sound(row["id"], row["file"], row["name"], row["volume"], row["reversed"]== "True", row["splice1"], row["splice2"])
                    self.sounds[int(row["id"])] = sound
                except:
                    print("invalid file")

    def saveChanges(self):
        array = []
        for i in self.sounds:
            if i != None:
                dict = {}
                dict["id"] = i.id
                dict["file"] = i.path
                dict["name"] = i.name
                dict["volume"] = i.volume
                dict["reversed"] = str(i.reversed)
                dict["splice1"] = i.splice1
                dict["splice2"] = i.splice2 
                array.append(dict)

        with open("SoundData.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(array)

    def addSound(self, id, path, name, volume, reversed):
        
        self.sounds[id] = Sound(id, path, name, volume, reversed)
        if not self.sounds[id].valid:
            self.sounds[id] = None



# Provides methods for playing and changing sounds
class Sound():
    def __init__(self, id, path, name, volume=False, reversed=False, splice1=0, splice2=None):
        self.valid = True
        try:
            # Original unedited audio
            self.audio = AudioSegment.from_mp3(path)
            if splice2 != None:
                self.splice2 = int(splice2)
            else:
                self.splice2 = len(self.audio)
            self.edited = self.audio
        except:
            print("Invalid File")
            self.valid = False
            self.splice2 = None
        # Edited audio
        self.reversed = reversed
        self.volume =  int(volume)
        self.splice1 = int(splice1)
        self.name = name
        self.id = id
        self.path = path




    def play(self):
        thread = threading.Thread(target=self.playThreaded, args=(self.edited,))
        thread.start()
    
    def playThreaded(self, sound):
        if USE_SPECIAL_PLAY:
            specialPlay(sound)
        else:
            _play_with_simpleaudio(sound)

    def setReverse(self, reversed):
        self.reversed = reversed

    def setVolume(self, volume):
        self.volume = volume

    def setSplice1(self, value):
        self.splice1 = value

    def setSplice2(self, value):
        self.splice2 = value

    def reset(self):
        self.edited = self.audio

    def makeChanges(self):
        self.edited = self.audio.apply_gain(ratio_to_db(self.volume / 100))
        self.edited = self.edited[self.splice1:self.splice2] 
        if self.reversed:
            self.edited = self.edited.reverse()

    def loadChanges(self):
        # read from file
        # edit using methods and data from file
        pass




def make_chunks(audio_segment, chunk_length):
    """
    Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
    long.
    if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    segments back (except the last one, which can be shorter)
    """
    number_of_chunks = ceil(len(audio_segment) / float(chunk_length))
    return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
            for i in range(int(number_of_chunks))]



def specialPlay(seg):
    p = pyaudio.PyAudio()
    # index = 0
    # for i in range(p.get_device_count()):
    #     device = p.get_device_info_by_index(i)
    #     if device["name"] == "my-combined-sink Audio/Sink sink":
    #         index = i
    # print(index)
    index = 26
    if index != 0:
            stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True, output_device_index=index)
    # else:
    # stream = p.open(format=p.get_format_from_width(seg.sample_width),
    #                 channels=seg.channels,
    #                 rate=seg.frame_rate,
    #                 output=True)
    print("1")
    # Just in case there were any exceptions/interrupts, we release the resource
    # So as not to raise OSError: Device Unavailable should play() be used again
    try:
        # break audio into half-second chunks (to allows keyboard interrupts)
        print("2")
        for chunk in make_chunks(seg, 500):
            stream.write(chunk._data)
    finally:
        print("3")
        stream.stop_stream()
        stream.close()

        p.terminate()




if __name__ == "__main__":

    soundboard = Soundboard()
    # soundboard.addSound("Sounds/boom.mp3", 0,"Vine Boom", 1, True)
    # soundboard.addSound("Sounds/get_out.mp3", 1, "Get Out", 1, True)
    soundboard.loadChanges()
    soundboard.sounds[0].play()
    soundboard.sounds[1].play()
    # soundboard.saveChanges()