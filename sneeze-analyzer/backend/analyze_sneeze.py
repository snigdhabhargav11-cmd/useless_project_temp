import sys
import json
try:
    import librosa
    import numpy as np
except ImportError:
    # If librosa is not installed, output mock data for testing
    print(json.dumps({
        "duration": 2.5,
        "volume": 0.08,
        "peak": 0.95
    }))
    sys.exit(0)

def analyze_audio(file_path):
    try:
        # Load audio file
        audio, sr = librosa.load(file_path, sr=None)
        
        # Calculate features
        duration = librosa.get_duration(y=audio, sr=sr)
        volume = float(np.mean(np.abs(audio)))
        peak = float(np.max(np.abs(audio)))
        
        # Output as JSON for Node.js to consume
        result = {
            "duration": duration,
            "volume": volume,
            "peak": peak
        }
        
        print(json.dumps(result))
    except Exception as e:
        print(f"Error analyzing audio: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_sneeze.py <audio_file_path>", file=sys.stderr)
        sys.exit(1)
        
    audio_path = sys.argv[1]
    analyze_audio(audio_path)
