import React, { useState } from 'react';
import AudioRecorder from './components/AudioRecorder';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  const [sneezeData, setSneezeData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAudioUpload = async (audioBlob) => {
    setIsAnalyzing(true);
    // Mocking an API call
    setTimeout(() => {
      setSneezeData({
        power: 9.2,
        volume: 8.7,
        style: 7.4,
        suspense: 8.9,
        animal: "Rhino",
        achievement: "Earth Shaker",
        commentary: "An explosive opening sneeze with championship-level projection. Slightly chaotic landing, but the crowd loved it."
      });
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center py-10">
      <header className="mb-10 text-center">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500 mb-2">
          Sneeze Analyzer
        </h1>
        <p className="text-gray-400 text-lg">Record your sneeze. Get rated. Become a legend.</p>
      </header>

      <main className="w-full max-w-4xl px-4 flex flex-col items-center">
        {!sneezeData && !isAnalyzing && (
          <AudioRecorder onUpload={handleAudioUpload} />
        )}

        {isAnalyzing && (
          <div className="flex flex-col items-center justify-center space-y-4 py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
            <p className="text-xl font-semibold text-blue-400 animate-pulse">Analyzing acoustic resonance...</p>
          </div>
        )}

        {sneezeData && !isAnalyzing && (
          <div className="w-full">
            <ResultsDashboard data={sneezeData} onReset={() => setSneezeData(null)} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
