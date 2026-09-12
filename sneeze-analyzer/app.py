import http.server
import socketserver
import json
import base64
import io
import math
import os
import random
import sys
import time

try:
    import soundfile as sf
    import numpy as np
    import librosa
    HAS_AUDIO_LIBS = True
except Exception as e:
    HAS_AUDIO_LIBS = False
    print(f"Warning: Audio processing libs missing, fallback to simulation mode: {e}")

PORT = 8000
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")

# Initialize default leaderboard if missing
if not os.path.exists(LEADERBOARD_FILE):
    default_leaderboard = [
        {"name": "GigaSneezer_99", "score": 98.4, "power": 9.9, "volume": 9.8, "animal": "T-Rex", "achievement": "Earth Shaker", "date": "2026-09-10"},
        {"name": "Dad_At_Sunday_BBQ", "score": 96.7, "power": 9.7, "volume": 9.9, "animal": "Rhino", "achievement": "Wake The Neighbors", "date": "2026-09-10"},
        {"name": "SneezingBeauty", "score": 92.1, "power": 8.8, "volume": 8.5, "animal": "Eagle", "achievement": "Sonic Boom", "date": "2026-09-11"},
        {"name": "AllergyKing", "score": 88.5, "power": 8.2, "volume": 7.9, "animal": "Lion", "achievement": "Scared The Cat", "date": "2026-09-11"},
        {"name": "MouseWhisperer", "score": 42.0, "power": 3.1, "volume": 2.8, "animal": "Hamster", "achievement": "Muffled Mouse", "date": "2026-09-11"}
    ]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(default_leaderboard, f, indent=2)

CELEBRITY_BENCHMARKS = [
    {"name": "Dwayne 'The Rock' Johnson", "score": 89.2, "quote": "Can you smell what the sneeze is cooking?!"},
    {"name": "Gordon Ramsay", "score": 93.4, "quote": "Finally, some good explosive pressure!"},
    {"name": "Taylor Swift", "score": 86.8, "quote": "I knew you were trouble when you sneezed."},
    {"name": "Darth Vader", "score": 95.1, "quote": "The force is violently strong with this one."},
    {"name": "Morgan Freeman", "score": 91.5, "quote": "And so it was, that the room fell completely silent."}
]

HOROSCOPES = [
    "Today's sneeze predicts unexpected snacks in your near future.",
    "The alignment of your nostrils indicates incoming good fortune and mild dust.",
    "A sneeze of this caliber warns against wearing white shirts around soup.",
    "Cosmic sneeze reading: Someone was talking about you, and they were intimidated.",
    "Ancient texts suggest this sneeze will ward off awkward conversations for 48 hours."
]

COMMENTARIES = [
    "An explosive opening sneeze with championship-level projection. Chaotic landing, but the crowd is on their feet!",
    "Incredible atmospheric displacement! Windows were rattling two blocks away. Pure Olympic caliber.",
    "A textbook pre-sneeze buildup followed by a thunderous acoustic blast. Nearby cats have officially filed complaints.",
    "Tremendous wind speed recorded at the epicenter. That wasn't just a sneeze; that was a weather event!",
    "Graceful nasal cadence transitioning into a seismic rupture. Judges award 10s across the board for pure audacity."
]

def analyze_audio_features(raw_bytes):
    """Analyze raw audio bytes using soundfile/librosa or heuristic fallback."""
    duration = 2.4
    volume_val = 0.08
    peak_val = 0.85
    spectral_centroid = 2200.0

    if HAS_AUDIO_LIBS:
        try:
            buf = io.BytesIO(raw_bytes)
            audio, sr = sf.read(buf)
            if audio.ndim > 1:
                audio = audio.mean(axis=1) # convert to mono
            audio = audio.astype(np.float32)
            
            if len(audio) > 0:
                duration = float(len(audio) / sr)
                peak_val = float(np.max(np.abs(audio)))
                volume_val = float(np.mean(np.abs(audio)))
                
                # Spectral feature
                try:
                    cent = librosa.feature.spectral_centroid(y=audio, sr=sr)
                    spectral_centroid = float(np.mean(cent))
                except Exception:
                    spectral_centroid = 2000.0
        except Exception as err:
            print(f"Error parsing with librosa/soundfile: {err}, using heuristic fallback.")
            # Heuristic calculation from byte dynamics
            duration = max(0.8, min(8.0, len(raw_bytes) / 32000.0))
            peak_val = random.uniform(0.75, 0.98)
            volume_val = random.uniform(0.05, 0.15)

    # Calculate normalized scores (0 - 10)
    power = round(min(10.0, max(1.0, peak_val * 10.2)), 1)
    volume_score = round(min(10.0, max(1.0, volume_val * 85.0 + random.uniform(0.5, 1.5))), 1)
    suspense = round(min(10.0, max(1.0, duration * 2.2 + random.uniform(0.2, 1.2))), 1)
    
    # Style based on spectral complexity + randomness
    style = round(min(10.0, max(3.0, (spectral_centroid / 500.0) + random.uniform(2.0, 4.5))), 1)

    # Total overall score out of 100
    overall = round(((power * 0.35) + (volume_score * 0.35) + (style * 0.15) + (suspense * 0.15)) * 10, 1)

    # Animal Classification
    if power >= 9.0 and volume_score >= 8.5:
        animal = "T-Rex"
        animal_desc = "Apex predator sneeze. Nearby car alarms were likely activated."
    elif power >= 8.5:
        animal = "Rhino"
        animal_desc = "Raw battering-ram energy. Structural integrity severely tested."
    elif volume_score >= 8.5:
        animal = "Lion"
        animal_desc = "Majestic, reverberant, territorial roar masquerading as a sneeze."
    elif style >= 8.5:
        animal = "Eagle"
        animal_desc = "Soaring acoustics and sharp aerodynamic pitch."
    elif suspense >= 8.0:
        animal = "Prowling Leopard"
        animal_desc = "The agonizing delay had everyone holding their breath."
    elif overall < 55.0:
        animal = "Hamster"
        animal_desc = "Adorably ineffective squeak. Mild breeze detected."
    else:
        animal = "Honey Badger"
        animal_desc = "Unapologetic, chaotic, and takes no prisoners."

    # Achievements
    achievements = []
    if power >= 9.0:
        achievements.append("Earth Shaker")
    if volume_score >= 8.5:
        achievements.append("Wake The Neighbors")
    if suspense >= 7.5:
        achievements.append("The Build-Up")
    if overall >= 90.0:
        achievements.append("Dad Sneeze Supreme")
    if style >= 8.8:
        achievements.append("Sonic Boom")
    if not achievements:
        achievements.append("Subtle Breezer")

    # Celebrity matchup
    celeb = random.choice(CELEBRITY_BENCHMARKS)
    diff = round(overall - celeb["score"], 1)
    if diff > 0:
        celeb_result = f"You OUT-SNEEZED {celeb['name']} by +{diff} pts! {celeb['quote']}"
    else:
        celeb_result = f"{celeb['name']} edged you out by {abs(diff)} pts! {celeb['quote']}"

    commentary = random.choice(COMMENTARIES)
    horoscope = random.choice(HOROSCOPES)

    return {
        "overall": overall,
        "power": power,
        "volume": volume_score,
        "style": style,
        "suspense": suspense,
        "duration": round(duration, 2),
        "animal": animal,
        "animal_desc": animal_desc,
        "achievement": achievements[0],
        "all_achievements": achievements,
        "commentary": commentary,
        "celebrity": {
            "name": celeb["name"],
            "score": celeb["score"],
            "result": celeb_result
        },
        "horoscope": horoscope,
        "certificate_id": f"SNZ-{random.randint(1000, 9999)}-{int(overall)}"
    }

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sneeze Analyzer: The Competitive Sneeze Rating Engine</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @keyframes pulse-glow {
      0%, 100% { box-shadow: 0 0 25px rgba(239, 68, 68, 0.4); }
      50% { box-shadow: 0 0 50px rgba(239, 68, 68, 0.8); }
    }
    .recording-pulse { animation: pulse-glow 1.5s infinite; }
    .glass-card { background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .gold-gradient { background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706); }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans selection:bg-rose-500 selection:text-white">

  <!-- TOP NAV -->
  <header class="border-b border-slate-800 bg-slate-900/60 sticky top-0 z-50 backdrop-blur-md">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3 cursor-pointer" onclick="showTab('record')">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-500 to-amber-500 flex items-center justify-center text-xl shadow-lg shadow-rose-500/30">
          <i class="fa-solid fa-head-side-cough text-white"></i>
        </div>
        <div>
          <span class="text-xl font-black tracking-tight bg-gradient-to-r from-rose-400 via-amber-300 to-emerald-400 bg-clip-text text-transparent">
            SNEEZE ANALYZER
          </span>
          <span class="block text-[10px] uppercase font-bold tracking-widest text-slate-400">Acoustic Rating Engine</span>
        </div>
      </div>
      <nav class="flex space-x-1 sm:space-x-2">
        <button onclick="showTab('record')" id="tab-record" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition bg-rose-500 text-white flex items-center space-x-2">
          <i class="fa-solid fa-microphone"></i> <span>Record</span>
        </button>
        <button onclick="showTab('battle')" id="tab-battle" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition hover:bg-slate-800 text-slate-300 flex items-center space-x-2">
          <i class="fa-solid fa-swords"></i> <span>Battle Mode</span>
        </button>
        <button onclick="showTab('leaderboard')" id="tab-leaderboard" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition hover:bg-slate-800 text-slate-300 flex items-center space-x-2">
          <i class="fa-solid fa-trophy"></i> <span>Leaderboard</span>
        </button>
      </nav>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 py-8">

    <!-- TAB 1: RECORD SNEEZE -->
    <section id="view-record" class="space-y-8">
      <div class="text-center max-w-2xl mx-auto space-y-3">
        <h1 class="text-4xl sm:text-5xl font-black text-white tracking-tight">
          Unleash Your <span class="bg-gradient-to-r from-rose-400 to-amber-400 bg-clip-text text-transparent">Acoustic Fury</span>
        </h1>
        <p class="text-slate-400 text-sm sm:text-base">
          Our AI acoustic model evaluates decibel intensity, duration suspense, spectral richness, and blast trajectory.
        </p>
      </div>

      <!-- MAIN RECORDER CARD -->
      <div class="max-w-xl mx-auto glass-card rounded-3xl p-6 sm:p-8 text-center relative overflow-hidden shadow-2xl">
        
        <!-- Mode Switcher -->
        <div class="flex items-center justify-center space-x-2 mb-5">
          <button id="modeMicBtn" onclick="setRecordingMode('mic')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-rose-500 text-white flex items-center space-x-1.5 shadow">
            <i class="fa-solid fa-microphone"></i> <span>Physical Mic</span>
          </button>
          <button id="modeSimBtn" onclick="setRecordingMode('sim')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center space-x-1.5">
            <i class="fa-solid fa-wand-magic-sparkles text-amber-400"></i> <span>Sneeze Simulator</span>
          </button>
        </div>

        <!-- In-Page Permission / Diagnostic Banner -->
        <div id="micNoticeBanner" class="hidden mb-5 p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-left">
          <div class="flex items-start space-x-3">
            <i class="fa-solid fa-triangle-exclamation text-amber-400 text-lg mt-0.5"></i>
            <div class="text-xs space-y-1.5 flex-1">
              <div class="font-bold text-amber-300" id="micNoticeTitle">Microphone Permission Needed</div>
              <div class="text-slate-300 leading-relaxed" id="micNoticeDesc">
                Click the 🔒 icon in your browser address bar and set <b>Microphone</b> to <b>Allow</b>. Or click below to record using the <b>Sneeze Simulator</b>!
              </div>
              <div class="pt-2 flex flex-wrap gap-2">
                <button onclick="retryMicPermission()" class="px-3 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold text-[11px] hover:bg-amber-400 transition">
                  <i class="fa-solid fa-rotate-right mr-1"></i> Grant / Retry Mic
                </button>
                <button onclick="setRecordingMode('sim'); toggleRecording();" class="px-3 py-1 rounded-lg bg-slate-800 text-amber-300 border border-amber-500/40 font-bold text-[11px] hover:bg-slate-700 transition">
                  <i class="fa-solid fa-bolt mr-1"></i> Auto-Sneeze Simulator
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Waveform Canvas -->
        <div class="w-full h-28 bg-slate-900/90 rounded-2xl mb-6 overflow-hidden border border-slate-800 relative flex items-center justify-center">
          <canvas id="waveformCanvas" class="w-full h-full"></canvas>
          <div id="micPromptText" class="absolute text-xs text-slate-500 uppercase tracking-widest font-bold">
            Mic Standby • Waveform Active
          </div>
        </div>

        <!-- Big Record Button -->
        <div class="my-6">
          <button id="recordBtn" onclick="toggleRecording()" class="w-32 h-32 rounded-full bg-gradient-to-tr from-rose-600 to-red-500 text-white flex flex-col items-center justify-center mx-auto shadow-xl hover:scale-105 active:scale-95 transition-all duration-300">
            <i id="recordIcon" class="fa-solid fa-microphone text-3xl mb-1"></i>
            <span id="recordLabel" class="text-xs font-black uppercase tracking-wider">Start Sneeze</span>
          </button>
          <div id="recordTimer" class="mt-3 text-sm font-mono font-bold text-slate-400 hidden">00:00</div>
          <div id="simModeBadge" class="mt-2 text-[11px] text-amber-400 font-semibold hidden">
            <i class="fa-solid fa-wand-magic-sparkles mr-1"></i> Acoustic Simulation Mode Active
          </div>
        </div>

        <div class="flex items-center justify-center space-x-3 text-slate-400 text-xs my-4">
          <span class="h-px w-12 bg-slate-800"></span>
          <span>OR UPLOAD AUDIO</span>
          <span class="h-px w-12 bg-slate-800"></span>
        </div>

        <!-- Upload File Option -->
        <div class="flex justify-center">
          <label class="cursor-pointer px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center space-x-2 transition border border-slate-700">
            <i class="fa-solid fa-upload"></i>
            <span>Upload .wav / .mp3</span>
            <input type="file" id="audioFileInput" accept="audio/*" class="hidden" onchange="handleFileUpload(event)">
          </label>
        </div>

        <!-- Sample Sneeze Demo Button -->
        <div class="mt-4">
          <button onclick="triggerDemoAnalysis()" class="text-xs text-amber-400 hover:underline font-semibold">
            <i class="fa-solid fa-bolt mr-1"></i> Instant 1-Click Sample Analysis
          </button>
        </div>

        <!-- Analyzing Spinner Overlay -->
        <div id="analyzingOverlay" class="absolute inset-0 bg-slate-950/90 backdrop-blur-md flex flex-col items-center justify-center space-y-4 hidden">
          <div class="w-16 h-16 border-4 border-rose-500/30 border-t-rose-500 rounded-full animate-spin"></div>
          <p class="text-base font-bold text-rose-400 animate-pulse">Running Librosa Acoustic Engine...</p>
          <p class="text-xs text-slate-500">Calculating peak amplitude & spectral roll-off</p>
        </div>
      </div>

      <!-- RESULTS DASHBOARD (Hidden until analysis completes) -->
      <div id="resultsSection" class="hidden space-y-8 max-w-4xl mx-auto transition-all duration-500">
        
        <!-- Score Banner -->
        <div class="glass-card rounded-3xl p-6 sm:p-8 flex flex-col sm:flex-row items-center justify-between border border-rose-500/30 bg-gradient-to-r from-rose-950/30 via-slate-900 to-amber-950/30">
          <div>
            <span class="px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider bg-rose-500/20 text-rose-400 border border-rose-500/30">
              Analysis Certified
            </span>
            <h2 class="text-3xl font-black text-white mt-2">Overall Blast Rating</h2>
            <p id="resAnimalDesc" class="text-sm text-slate-400 mt-1"></p>
          </div>
          <div class="text-center mt-4 sm:mt-0">
            <div id="resOverallScore" class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-rose-400 to-red-500">
              --
            </div>
            <div class="text-xs font-bold uppercase tracking-widest text-slate-400 mt-1">out of 100</div>
          </div>
        </div>

        <!-- Two Columns: Metrics & Radar Chart -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Metrics Breakdown -->
          <div class="glass-card rounded-3xl p-6 space-y-5">
            <h3 class="text-lg font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-chart-simple text-rose-400"></i>
              <span>Acoustic Metrics</span>
            </h3>

            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-xs font-bold mb-1">
                  <span class="text-slate-300"><i class="fa-solid fa-bomb text-red-400 mr-2"></i>Power (Peak Impact)</span>
                  <span id="valPower" class="text-red-400">-- / 10</span>
                </div>
                <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                  <div id="barPower" class="bg-red-500 h-full rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs font-bold mb-1">
                  <span class="text-slate-300"><i class="fa-solid fa-volume-high text-blue-400 mr-2"></i>Volume (Decibels)</span>
                  <span id="valVolume" class="text-blue-400">-- / 10</span>
                </div>
                <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                  <div id="barVolume" class="bg-blue-500 h-full rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs font-bold mb-1">
                  <span class="text-slate-300"><i class="fa-solid fa-wand-magic-sparkles text-purple-400 mr-2"></i>Style (Harmonics)</span>
                  <span id="valStyle" class="text-purple-400">-- / 10</span>
                </div>
                <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                  <div id="barStyle" class="bg-purple-500 h-full rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs font-bold mb-1">
                  <span class="text-slate-300"><i class="fa-solid fa-hourglass-half text-amber-400 mr-2"></i>Suspense (Build-up)</span>
                  <span id="valSuspense" class="text-amber-400">-- / 10</span>
                </div>
                <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                  <div id="barSuspense" class="bg-amber-500 h-full rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Radar Chart -->
          <div class="glass-card rounded-3xl p-6 flex flex-col items-center justify-center">
            <h3 class="text-lg font-bold text-white mb-2 self-start flex items-center space-x-2">
              <i class="fa-solid fa-radar text-emerald-400"></i>
              <span>Sneeze Resonance Radar</span>
            </h3>
            <div class="w-full max-w-[280px] h-[260px]">
              <canvas id="radarChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Badges & Highlights Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          
          <!-- Animal Classification Card -->
          <div class="glass-card rounded-3xl p-6 border-l-4 border-amber-500">
            <div class="text-xs uppercase font-bold text-amber-400 tracking-wider mb-1">Animal Classifier</div>
            <div id="resAnimal" class="text-2xl font-black text-white flex items-center space-x-3">
              <span id="resAnimalIcon" class="text-3xl">🦏</span>
              <span id="resAnimalTitle">The Rhino</span>
            </div>
            <p id="resAnimalDetail" class="text-xs text-slate-400 mt-2">Battering-ram energy detected.</p>
          </div>

          <!-- Achievement Card -->
          <div class="glass-card rounded-3xl p-6 border-l-4 border-emerald-500">
            <div class="text-xs uppercase font-bold text-emerald-400 tracking-wider mb-1">Achievement Unlocked</div>
            <div id="resAchievement" class="text-2xl font-black text-white flex items-center space-x-3">
              <span class="text-3xl">🏆</span>
              <span id="resAchievementTitle">Earth Shaker</span>
            </div>
            <div id="resAchievementsList" class="flex flex-wrap gap-1 mt-2"></div>
          </div>
        </div>

        <!-- AI Commentary Box -->
        <div class="glass-card rounded-3xl p-6 border border-blue-500/30 bg-blue-950/20 relative">
          <div class="flex items-center space-x-2 text-blue-400 font-bold text-xs uppercase tracking-wider mb-2">
            <i class="fa-solid fa-bullhorn"></i>
            <span>AI Sports Commentary</span>
          </div>
          <p id="resCommentary" class="text-base sm:text-lg italic text-slate-200 font-medium leading-relaxed">
            "..."
          </p>
        </div>

        <!-- Celebrity Comparison & Horoscope -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <!-- Celebrity Comparison -->
          <div class="glass-card rounded-3xl p-6">
            <div class="text-xs uppercase font-bold text-rose-400 tracking-wider mb-2 flex items-center space-x-2">
              <i class="fa-solid fa-star"></i>
              <span>Celebrity Sneeze-Off</span>
            </div>
            <p id="resCelebrityResult" class="text-sm font-semibold text-slate-200"></p>
          </div>

          <!-- Sneeze Horoscope -->
          <div class="glass-card rounded-3xl p-6">
            <div class="text-xs uppercase font-bold text-purple-400 tracking-wider mb-2 flex items-center space-x-2">
              <i class="fa-solid fa-crystal-ball"></i>
              <span>Daily Sneeze Horoscope</span>
            </div>
            <p id="resHoroscope" class="text-sm italic text-slate-300"></p>
          </div>
        </div>

        <!-- Sneeze Certificate / NFT Card & Leaderboard Submission -->
        <div class="glass-card rounded-3xl p-6 sm:p-8 text-center space-y-4 border border-amber-500/30">
          <h4 class="text-xl font-black text-white">Claim Your Sneeze Certificate</h4>
          <p class="text-xs text-slate-400 max-w-md mx-auto">
            Save your result to the Global Leaderboard and stamp your official Sneeze NFT ID.
          </p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-3 max-w-md mx-auto">
            <input type="text" id="leaderboardNameInput" placeholder="Enter your Sneezer Name" class="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-rose-500">
            <button onclick="submitToLeaderboard()" class="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-white font-bold text-sm shadow-lg hover:opacity-90 transition whitespace-nowrap">
              Submit Score
            </button>
          </div>
          <div id="submitStatus" class="text-xs text-emerald-400 font-semibold hidden"></div>
        </div>

      </div>
    </section>

    <!-- TAB 2: SNEEZE BATTLE MODE -->
    <section id="view-battle" class="space-y-8 hidden">
      <div class="text-center max-w-2xl mx-auto space-y-3">
        <h1 class="text-4xl sm:text-5xl font-black text-white tracking-tight">
          Sneeze <span class="bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">Battle Arena</span>
        </h1>
        <p class="text-slate-400 text-sm">Two warriors enter. Only the superior nasal blast survives.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <!-- Player 1 -->
        <div class="glass-card rounded-3xl p-6 text-center space-y-4 border border-cyan-500/30">
          <div class="w-12 h-12 rounded-2xl bg-cyan-500/20 text-cyan-400 mx-auto flex items-center justify-center text-xl font-black">P1</div>
          <h3 class="text-xl font-bold text-white">Challenger 1</h3>
          <button onclick="recordBattle(1)" id="battleBtn1" class="px-6 py-3 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-sm transition w-full">
            <i class="fa-solid fa-microphone mr-2"></i> Record P1 Sneeze
          </button>
          <div id="battleP1Status" class="text-xs text-slate-400">Status: Waiting for sneeze</div>
          <div id="battleP1Score" class="text-3xl font-black text-cyan-400 hidden">--</div>
        </div>

        <!-- Player 2 -->
        <div class="glass-card rounded-3xl p-6 text-center space-y-4 border border-pink-500/30">
          <div class="w-12 h-12 rounded-2xl bg-pink-500/20 text-pink-400 mx-auto flex items-center justify-center text-xl font-black">P2</div>
          <h3 class="text-xl font-bold text-white">Challenger 2</h3>
          <button onclick="recordBattle(2)" id="battleBtn2" class="px-6 py-3 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-bold text-sm transition w-full">
            <i class="fa-solid fa-microphone mr-2"></i> Record P2 Sneeze
          </button>
          <div id="battleP2Status" class="text-xs text-slate-400">Status: Waiting for sneeze</div>
          <div id="battleP2Score" class="text-3xl font-black text-pink-400 hidden">--</div>
        </div>
      </div>

      <!-- Battle Result Card -->
      <div id="battleResultCard" class="max-w-xl mx-auto glass-card rounded-3xl p-8 text-center space-y-4 border border-amber-500/40 hidden">
        <span class="px-3 py-1 rounded-full text-xs font-black uppercase bg-amber-500/20 text-amber-400">Decisive Victory</span>
        <h2 id="battleWinnerText" class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-rose-400"></h2>
        <p id="battleWinnerSub" class="text-sm text-slate-300"></p>
      </div>
    </section>

    <!-- TAB 3: LEADERBOARD -->
    <section id="view-leaderboard" class="space-y-8 hidden">
      <div class="text-center max-w-2xl mx-auto space-y-3">
        <h1 class="text-4xl sm:text-5xl font-black text-white tracking-tight">
          Global <span class="bg-gradient-to-r from-amber-400 to-yellow-500 bg-clip-text text-transparent">Hall of Fame</span>
        </h1>
        <p class="text-slate-400 text-sm">The most explosive nasal sonic blasts recorded in human history.</p>
      </div>

      <div class="max-w-3xl mx-auto glass-card rounded-3xl overflow-hidden shadow-2xl border border-slate-800">
        <div class="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/40">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Top Sneezers</span>
          <button onclick="loadLeaderboard()" class="text-xs text-rose-400 hover:underline flex items-center space-x-1">
            <i class="fa-solid fa-rotate-right"></i> <span>Refresh</span>
          </button>
        </div>
        <div id="leaderboardList" class="divide-y divide-slate-800/60">
          <div class="p-8 text-center text-slate-500">Loading rankings...</div>
        </div>
      </div>
    </section>

  </main>

  <footer class="border-t border-slate-900 py-6 text-center text-xs text-slate-600">
    Sneeze Analyzer • Powered by Python Librosa & Web Audio API
  </footer>

  <script>
    let isRecording = false;
    let mediaRecorder = null;
    let audioChunks = [];
    let audioContext = null;
    let analyser = null;
    let animFrameId = null;
    let currentResultData = null;
    let radarChartInstance = null;
    let recordStartTime = 0;
    let timerInterval = null;

    // Tabs
    function showTab(tab) {
      ['record', 'battle', 'leaderboard'].forEach(t => {
        document.getElementById('view-' + t).classList.toggle('hidden', t !== tab);
        const btn = document.getElementById('tab-' + t);
        if (t === tab) {
          btn.className = 'tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition bg-rose-500 text-white flex items-center space-x-2';
        } else {
          btn.className = 'tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition hover:bg-slate-800 text-slate-300 flex items-center space-x-2';
        }
      });
      if (tab === 'leaderboard') loadLeaderboard();
    }

    // Audio Canvas visualizer setup
    const canvas = document.getElementById('waveformCanvas');
    const ctx = canvas.getContext('2d');

    function drawIdleWaveform() {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 2;
      ctx.beginPath();
      const mid = canvas.height / 2;
      ctx.moveTo(0, mid);
      ctx.lineTo(canvas.width, mid);
      ctx.stroke();
    }
    window.addEventListener('resize', drawIdleWaveform);
    drawIdleWaveform();

    function visualizeStream(stream) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioContext.createMediaStreamSource(stream);
      analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      function render() {
        animFrameId = requestAnimationFrame(render);
        analyser.getByteTimeDomainData(dataArray);

        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.lineWidth = 3;
        ctx.strokeStyle = isRecording ? '#f43f5e' : '#38bdf8';
        ctx.beginPath();

        const sliceWidth = canvas.width / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          const v = dataArray[i] / 128.0;
          const y = (v * canvas.height) / 2;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
          x += sliceWidth;
        }

        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
      }
      render();
    }

    let currentMode = 'mic'; // 'mic' or 'sim'
    let simAnimId = null;

    function setRecordingMode(mode) {
      currentMode = mode;
      const micBtn = document.getElementById('modeMicBtn');
      const simBtn = document.getElementById('modeSimBtn');
      const badge = document.getElementById('simModeBadge');

      if (mode === 'mic') {
        micBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition bg-rose-500 text-white flex items-center space-x-1.5 shadow';
        simBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center space-x-1.5';
        badge.classList.add('hidden');
        document.getElementById('micPromptText').innerText = 'Mic Standby • Waveform Active';
      } else {
        simBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition bg-amber-500 text-slate-950 flex items-center space-x-1.5 shadow';
        micBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center space-x-1.5';
        badge.classList.remove('hidden');
        document.getElementById('micPromptText').innerText = 'Simulator Ready • Click Start Sneeze';
      }
    }

    async function retryMicPermission() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(t => t.stop());
        document.getElementById('micNoticeBanner').classList.add('hidden');
        setRecordingMode('mic');
        toggleRecording();
      } catch (err) {
        showMicWarning(err);
      }
    }

    function showMicWarning(err) {
      const banner = document.getElementById('micNoticeBanner');
      const title = document.getElementById('micNoticeTitle');
      const desc = document.getElementById('micNoticeDesc');
      banner.classList.remove('hidden');

      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        title.innerText = 'Microphone Access Was Blocked in Browser';
        desc.innerHTML = 'Click the 🔒 icon in the browser address bar (top left of this page) and toggle <b>Microphone</b> to <b>Allow</b>, then click "Grant / Retry Mic". Or use the <b>Auto-Sneeze Simulator</b> right now!';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        title.innerText = 'No Hardware Microphone Detected';
        desc.innerHTML = 'Your system does not report an active microphone. We have activated <b>Acoustic Sneeze Simulator Mode</b> so you can still record and analyze realistic sneezes!';
      } else {
        title.innerText = 'Microphone Notice: ' + (err.name || 'Unavailable');
        desc.innerText = (err.message || 'Microphone could not be started.') + ' You can continue seamlessly using the Sneeze Simulator!';
      }
    }

    // Dual-Mode Recording (Physical Mic + Virtual Sneeze Simulator)
    async function toggleRecording() {
      if (!isRecording) {
        // If already in simulator mode or if no getUserMedia available
        if (currentMode === 'sim' || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          startSimulatedRecording();
          return;
        }

        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          audioChunks = [];
          document.getElementById('micNoticeBanner').classList.add('hidden');
          visualizeStream(stream);

          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = e => { if (e.data.size > 0) audioChunks.push(e.data); };
          mediaRecorder.onstop = () => {
            const blob = new Blob(audioChunks, { type: 'audio/wav' });
            stream.getTracks().forEach(t => t.stop());
            if (animFrameId) cancelAnimationFrame(animFrameId);
            drawIdleWaveform();
            sendAudioToBackend(blob);
          };

          mediaRecorder.start();
          isRecording = true;
          document.getElementById('recordBtn').classList.add('recording-pulse', 'from-red-600', 'to-rose-700');
          document.getElementById('recordIcon').className = 'fa-solid fa-stop text-3xl mb-1';
          document.getElementById('recordLabel').innerText = 'Stop Sneeze';
          document.getElementById('micPromptText').innerText = 'RECORDING NOW • SNEEZE PROUDLY!';
          
          recordStartTime = Date.now();
          document.getElementById('recordTimer').classList.remove('hidden');
          timerInterval = setInterval(() => {
            const sec = Math.floor((Date.now() - recordStartTime) / 1000);
            document.getElementById('recordTimer').innerText = `00:0${sec}`.slice(-5);
          }, 500);

        } catch (err) {
          console.warn("Microphone access failed:", err);
          showMicWarning(err);
          // Graceful auto-fallback: switch to simulator so user is not blocked!
          setRecordingMode('sim');
          startSimulatedRecording();
        }
      } else {
        if (currentMode === 'sim') {
          stopSimulatedRecording();
        } else {
          if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
          }
          isRecording = false;
          clearInterval(timerInterval);
          document.getElementById('recordBtn').classList.remove('recording-pulse');
          document.getElementById('recordIcon').className = 'fa-solid fa-microphone text-3xl mb-1';
          document.getElementById('recordLabel').innerText = 'Start Sneeze';
          document.getElementById('micPromptText').innerText = 'Mic Standby • Waveform Active';
        }
      }
    }

    // Simulated Acoustic Sneeze Recording
    function startSimulatedRecording() {
      isRecording = true;
      document.getElementById('recordBtn').classList.add('recording-pulse', 'from-amber-600', 'to-orange-600');
      document.getElementById('recordIcon').className = 'fa-solid fa-stop text-3xl mb-1';
      document.getElementById('recordLabel').innerText = 'Stop Sneeze';
      document.getElementById('micPromptText').innerText = 'SIMULATING SNEEZE BLAST • SNEEZE READY!';

      recordStartTime = Date.now();
      document.getElementById('recordTimer').classList.remove('hidden');
      timerInterval = setInterval(() => {
        const sec = Math.floor((Date.now() - recordStartTime) / 1000);
        document.getElementById('recordTimer').innerText = `00:0${sec}`.slice(-5);
      }, 500);

      // Animate simulated waveform on canvas
      function drawSimWaveform() {
        if (!isRecording) return;
        simAnimId = requestAnimationFrame(drawSimWaveform);

        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const elapsed = (Date.now() - recordStartTime) / 1000.0;
        const mid = canvas.height / 2;
        ctx.lineWidth = 3;
        ctx.strokeStyle = elapsed > 1.2 && elapsed < 2.0 ? '#ef4444' : '#f59e0b';
        ctx.beginPath();

        const points = 64;
        const sliceWidth = canvas.width / points;

        for (let i = 0; i <= points; i++) {
          const x = i * sliceWidth;
          // Inhalation phase (0-1.2s), Explosive blast spike (1.2-2.0s), Decay (>2.0s)
          let amp = 6;
          if (elapsed > 1.2 && elapsed < 2.0) {
            amp = (canvas.height * 0.42) * (Math.random() * 0.8 + 0.2); // massive burst
          } else if (elapsed <= 1.2) {
            amp = 8 + (elapsed / 1.2) * 20 * (Math.random() * 0.5 + 0.5);
          } else {
            amp = 10 * Math.random();
          }
          const y = mid + Math.sin(i * 0.4 + elapsed * 10) * amp;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      drawSimWaveform();

      // Auto-finish after 2.4s of realistic sneeze duration if not manually stopped
      setTimeout(() => {
        if (isRecording && currentMode === 'sim') {
          stopSimulatedRecording();
        }
      }, 2500);
    }

    function stopSimulatedRecording() {
      isRecording = false;
      clearInterval(timerInterval);
      if (simAnimId) cancelAnimationFrame(simAnimId);
      drawIdleWaveform();

      document.getElementById('recordBtn').classList.remove('recording-pulse');
      document.getElementById('recordIcon').className = 'fa-solid fa-microphone text-3xl mb-1';
      document.getElementById('recordLabel').innerText = 'Start Sneeze';
      document.getElementById('micPromptText').innerText = 'Simulator Ready • Sneeze Captured';

      // Synthesize realistic acoustic audio WAV buffer
      const audioBlob = generateAcousticSneezeBlob();
      sendAudioToBackend(audioBlob);
    }

    // Generate real acoustic 16-bit PCM WAV
    function generateAcousticSneezeBlob() {
      const sampleRate = 22050;
      const duration = 2.2 + Math.random() * 0.6; // ~2.5s duration
      const totalSamples = Math.floor(sampleRate * duration);
      const buffer = new Float32Array(totalSamples);

      const inhaleEnd = Math.floor(totalSamples * 0.40);
      const blastEnd = Math.floor(totalSamples * 0.75);

      for (let i = 0; i < totalSamples; i++) {
        const t = i / sampleRate;
        let sample = 0;
        if (i < inhaleEnd) {
          // Inhale: rising soft noise + harmonic flutter
          const progress = i / inhaleEnd;
          const noise = (Math.random() * 2 - 1) * 0.18 * Math.pow(progress, 2);
          const tone = Math.sin(2 * Math.PI * (220 + progress * 280) * t) * 0.12 * progress;
          sample = noise + tone;
        } else if (i < blastEnd) {
          // Explosive Sneeze Blast: extreme amplitude burst + low end acoustic pressure
          const blastProgress = (i - inhaleEnd) / (blastEnd - inhaleEnd);
          const envelope = Math.exp(-blastProgress * 3.8);
          const noise = (Math.random() * 2 - 1) * 0.98 * envelope;
          const rumble = Math.sin(2 * Math.PI * 90 * t) * 0.45 * envelope;
          const pop = Math.sin(2 * Math.PI * 1800 * t) * 0.25 * envelope;
          sample = noise + rumble + pop;
        } else {
          // Dissipation tail
          const tailProgress = (i - blastEnd) / (totalSamples - blastEnd);
          const envelope = Math.max(0, 1 - tailProgress) * 0.12;
          sample = (Math.random() * 2 - 1) * envelope;
        }
        buffer[i] = Math.max(-1, Math.min(1, sample));
      }

      return encodeWav(buffer, sampleRate);
    }

    function encodeWav(samples, sampleRate) {
      const buffer = new ArrayBuffer(44 + samples.length * 2);
      const view = new DataView(buffer);

      function writeStr(offset, str) {
        for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
      }

      writeStr(0, 'RIFF');
      view.setUint32(4, 36 + samples.length * 2, true);
      writeStr(8, 'WAVE');
      writeStr(12, 'fmt ');
      view.setUint32(16, 16, true);
      view.setUint16(20, 1, true); // PCM
      view.setUint16(22, 1, true); // Mono
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * 2, true);
      view.setUint16(32, 2, true);
      view.setUint16(34, 16, true);
      writeStr(36, 'data');
      view.setUint32(40, samples.length * 2, true);

      let offset = 44;
      for (let i = 0; i < samples.length; i++, offset += 2) {
        const s = Math.max(-1, Math.min(1, samples[i]));
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
      }

      return new Blob([view], { type: 'audio/wav' });
    }

    // File upload
    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        sendAudioToBackend(file);
      }
    }

    // Instant demo trigger
    function triggerDemoAnalysis() {
      // Create a dummy audio blob with a chirp / burst
      sendAudioToBackend(null, true);
    }

    // Send to Backend
    async function sendAudioToBackend(blob, isDemo = false) {
      document.getElementById('analyzingOverlay').classList.remove('hidden');

      let payload = { is_demo: isDemo };
      if (blob && !isDemo) {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = async () => {
          payload.audio_base64 = reader.result;
          executeUpload(payload);
        };
      } else {
        executeUpload(payload);
      }
    }

    async function executeUpload(payload) {
      try {
        const res = await fetch('/api/upload-sneeze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        document.getElementById('analyzingOverlay').classList.add('hidden');
        displayResults(data);
      } catch (err) {
        document.getElementById('analyzingOverlay').classList.add('hidden');
        alert("Server error processing audio: " + err.message);
      }
    }

    // Display Results
    function displayResults(data) {
      currentResultData = data;
      document.getElementById('resultsSection').classList.remove('hidden');

      // Scroll to results
      document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });

      // Confetti burst!
      confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });

      document.getElementById('resOverallScore').innerText = data.overall;
      document.getElementById('resAnimalDesc').innerText = data.animal_desc;

      // Metrics
      document.getElementById('valPower').innerText = `${data.power} / 10`;
      document.getElementById('barPower').style.width = `${data.power * 10}%`;

      document.getElementById('valVolume').innerText = `${data.volume} / 10`;
      document.getElementById('barVolume').style.width = `${data.volume * 10}%`;

      document.getElementById('valStyle').innerText = `${data.style} / 10`;
      document.getElementById('barStyle').style.width = `${data.style * 10}%`;

      document.getElementById('valSuspense').innerText = `${data.suspense} / 10`;
      document.getElementById('barSuspense').style.width = `${data.suspense * 10}%`;

      // Animal
      const animalIcons = { 'T-Rex': '🦖', 'Rhino': '🦏', 'Lion': '🦁', 'Eagle': '🦅', 'Prowling Leopard': '🐆', 'Hamster': '🐹', 'Honey Badger': '🦡' };
      document.getElementById('resAnimalIcon').innerText = animalIcons[data.animal] || '🦏';
      document.getElementById('resAnimalTitle').innerText = 'The ' + data.animal;
      document.getElementById('resAnimalDetail').innerText = data.animal_desc;

      // Achievement
      document.getElementById('resAchievementTitle').innerText = data.achievement;
      const achContainer = document.getElementById('resAchievementsList');
      achContainer.innerHTML = '';
      data.all_achievements.forEach(ach => {
        const badge = document.createElement('span');
        badge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        badge.innerText = '⚡ ' + ach;
        achContainer.appendChild(badge);
      });

      // Commentary & Extras
      document.getElementById('resCommentary').innerText = `"${data.commentary}"`;
      document.getElementById('resCelebrityResult').innerText = data.celebrity.result;
      document.getElementById('resHoroscope').innerText = `"${data.horoscope}"`;

      // Radar Chart
      renderRadarChart(data);
    }

    function renderRadarChart(data) {
      const ctx = document.getElementById('radarChart').getContext('2d');
      if (radarChartInstance) radarChartInstance.destroy();

      radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['Power', 'Volume', 'Style', 'Suspense'],
          datasets: [{
            label: 'Resonance Profile',
            data: [data.power, data.volume, data.style, data.suspense],
            backgroundColor: 'rgba(244, 63, 94, 0.25)',
            borderColor: '#f43f5e',
            borderWidth: 2,
            pointBackgroundColor: '#fbbf24',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#fbbf24'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              pointLabels: { color: '#94a3b8', font: { size: 11, weight: 'bold' } },
              ticks: { display: false, min: 0, max: 10 }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }

    // Leaderboard
    async function submitToLeaderboard() {
      if (!currentResultData) return;
      const name = document.getElementById('leaderboardNameInput').value.trim() || 'Anonymous Sneezer';
      const statusEl = document.getElementById('submitStatus');

      try {
        const res = await fetch('/api/leaderboard', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: name,
            score: currentResultData.overall,
            power: currentResultData.power,
            volume: currentResultData.volume,
            animal: currentResultData.animal,
            achievement: currentResultData.achievement
          })
        });
        const saved = await res.json();
        statusEl.innerText = `✓ Stamped on Leaderboard! Certificate: ${currentResultData.certificate_id}`;
        statusEl.classList.remove('hidden');
      } catch (e) {
        alert("Failed to submit score: " + e.message);
      }
    }

    async function loadLeaderboard() {
      const container = document.getElementById('leaderboardList');
      container.innerHTML = '<div class="p-8 text-center text-slate-500">Fetching rankings...</div>';
      try {
        const res = await fetch('/api/leaderboard');
        const list = await res.json();
        container.innerHTML = '';
        list.forEach((item, index) => {
          const row = document.createElement('div');
          row.className = 'p-4 flex items-center justify-between hover:bg-slate-900/40 transition';
          const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index + 1}`;
          row.innerHTML = `
            <div class="flex items-center space-x-4">
              <span class="text-lg font-black text-amber-400 w-8 text-center">${medal}</span>
              <div>
                <div class="font-bold text-white text-sm">${item.name}</div>
                <div class="text-[11px] text-slate-400 flex items-center space-x-2 mt-0.5">
                  <span class="px-1.5 py-0.2 rounded bg-slate-800 text-slate-300">${item.animal || 'Animal'}</span>
                  <span>•</span>
                  <span>${item.achievement || 'Achievement'}</span>
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-xl font-black text-rose-400">${item.score}</div>
              <div class="text-[10px] uppercase font-bold text-slate-500">Points</div>
            </div>
          `;
          container.appendChild(row);
        });
      } catch (err) {
        container.innerHTML = `<div class="p-8 text-center text-red-400">Failed to load leaderboard.</div>`;
      }
    }

    // Battle Mode Simulation
    let battleScores = { 1: null, 2: null };
    function recordBattle(playerNum) {
      const statusEl = document.getElementById(`battleP${playerNum}Status`);
      const scoreEl = document.getElementById(`battleP${playerNum}Score`);
      const btn = document.getElementById(`battleBtn${playerNum}`);

      btn.disabled = true;
      statusEl.innerText = "Analyzing battle sneeze...";
      
      setTimeout(() => {
        const score = parseFloat((Math.random() * (98.5 - 65.0) + 65.0).toFixed(1));
        battleScores[playerNum] = score;
        scoreEl.innerText = score + " pts";
        scoreEl.classList.remove('hidden');
        statusEl.innerText = "Sneeze Recorded!";
        btn.disabled = false;

        if (battleScores[1] !== null && battleScores[2] !== null) {
          evaluateBattle();
        }
      }, 1500);
    }

    function evaluateBattle() {
      const card = document.getElementById('battleResultCard');
      const title = document.getElementById('battleWinnerText');
      const sub = document.getElementById('battleWinnerSub');
      card.classList.remove('hidden');
      card.scrollIntoView({ behavior: 'smooth' });

      confetti({ particleCount: 150, spread: 80, origin: { y: 0.7 } });

      if (battleScores[1] > battleScores[2]) {
        title.innerText = "PLAYER 1 WINS THE SNEEZE BATTLE!";
        sub.innerText = `P1 crushed with ${battleScores[1]} pts over P2's ${battleScores[2]} pts. Pure sonic dominance.`;
      } else if (battleScores[2] > battleScores[1]) {
        title.innerText = "PLAYER 2 WINS THE SNEEZE BATTLE!";
        sub.innerText = `P2 obliterated with ${battleScores[2]} pts over P1's ${battleScores[1]} pts. Unstoppable pressure.`;
      } else {
        title.innerText = "IT'S A DEAD TIE!";
        sub.innerText = "Synchronized nasal blast of equal magnitude!";
      }
    }
  </script>
</body>
</html>
"""

class SneezeRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean logging
        sys.stdout.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}\n")
        sys.stdout.flush()

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/leaderboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            try:
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Sort descending by score
                data.sort(key=lambda x: x.get("score", 0), reverse=True)
                self.wfile.write(json.dumps(data).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps([]).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/upload-sneeze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            
            raw_audio_bytes = b""
            try:
                payload = json.loads(body.decode("utf-8"))
                if "audio_base64" in payload and payload["audio_base64"]:
                    b64_str = payload["audio_base64"]
                    if "," in b64_str:
                        b64_str = b64_str.split(",")[1]
                    raw_audio_bytes = base64.b64decode(b64_str)
            except Exception:
                raw_audio_bytes = body

            result = analyze_audio_features(raw_audio_bytes)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        elif self.path == "/api/leaderboard":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                new_entry = json.loads(body.decode("utf-8"))
                new_entry["date"] = time.strftime("%Y-%m-%d")
                
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data.append(new_entry)
                data.sort(key=lambda x: x.get("score", 0), reverse=True)
                data = data[:50] # Keep top 50
                with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), SneezeRequestHandler) as httpd:
        print("===============================================================")
        print(f"[*] SNEEZE ANALYZER SERVER RUNNING at http://localhost:{PORT}")
        print(f"[*] Audio Engine: {'Librosa + SoundFile (Active)' if HAS_AUDIO_LIBS else 'Simulation Mode'}")
        print("===============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
