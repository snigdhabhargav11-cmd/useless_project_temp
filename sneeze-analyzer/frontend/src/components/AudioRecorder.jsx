import React, { useState, useRef } from 'react';
import { Mic, Square, Upload } from 'lucide-react';

const AudioRecorder = ({ onUpload }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(blob);
        audioChunksRef.current = [];
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Please allow microphone access to record your sneeze.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      // Stop all tracks to release mic
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const handleUpload = () => {
    if (audioBlob) {
      onUpload(audioBlob);
    }
  };

  return (
    <div className="bg-slate-800 p-8 rounded-2xl shadow-2xl w-full max-w-md text-center border border-slate-700">
      <div className="mb-8">
        <div className={`mx-auto w-32 h-32 rounded-full flex items-center justify-center transition-all duration-300 ${isRecording ? 'bg-red-500/20 animate-pulse' : 'bg-slate-700'}`}>
          {isRecording ? (
            <Mic className="w-16 h-16 text-red-500 animate-bounce" />
          ) : (
            <Mic className="w-16 h-16 text-gray-400" />
          )}
        </div>
      </div>
      
      {!audioBlob || isRecording ? (
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`px-8 py-4 rounded-full font-bold text-lg w-full flex items-center justify-center space-x-2 transition-transform hover:scale-105 ${
            isRecording 
              ? 'bg-red-500 hover:bg-red-600 text-white' 
              : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white'
          }`}
        >
          {isRecording ? (
            <>
              <Square className="w-5 h-5 fill-current" />
              <span>Stop Recording</span>
            </>
          ) : (
            <>
              <Mic className="w-5 h-5" />
              <span>Record Sneeze</span>
            </>
          )}
        </button>
      ) : (
        <div className="space-y-4">
          <audio controls src={URL.createObjectURL(audioBlob)} className="w-full mb-4" />
          <div className="flex space-x-4">
            <button
              onClick={() => setAudioBlob(null)}
              className="flex-1 px-4 py-3 rounded-xl bg-slate-700 hover:bg-slate-600 font-semibold transition-colors"
            >
              Retake
            </button>
            <button
              onClick={handleUpload}
              className="flex-1 px-4 py-3 rounded-xl bg-green-500 hover:bg-green-600 font-bold flex items-center justify-center space-x-2 transition-transform hover:scale-105 shadow-lg shadow-green-500/30"
            >
              <Upload className="w-5 h-5" />
              <span>Analyze</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;
