from pydub import AudioSegment
from pydub.playback import play

# Plays sound to attract the user's attention in case he is not looking at the console.
def sound_alarm():
    song = AudioSegment.from_wav(os.path.dirname(os.path.abspath(__file__))+"/firePagerAlert.wav")
    first_second = song[:1000]
    play(first_second-30)
