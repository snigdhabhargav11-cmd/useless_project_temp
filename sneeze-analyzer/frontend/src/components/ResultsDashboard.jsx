import React from 'react';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { RotateCcw, Trophy, Activity, Wind, Volume2 } from 'lucide-react';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const ResultsDashboard = ({ data, onReset }) => {
  const chartData = {
    labels: ['Power', 'Volume', 'Style', 'Suspense'],
    datasets: [
      {
        label: 'Sneeze Profile',
        data: [data.power, data.volume, data.style, data.suspense],
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(99, 102, 241, 1)',
      },
    ],
  };

  const chartOptions = {
    scales: {
      r: {
        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
        pointLabels: { color: 'rgba(255, 255, 255, 0.7)', font: { size: 14 } },
        ticks: { display: false, min: 0, max: 10 },
      },
    },
    plugins: {
      legend: { display: false },
    },
  };

  const totalScore = ((data.power + data.volume + data.style + data.suspense) / 4).toFixed(1);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full bg-slate-800 rounded-3xl p-8 border border-slate-700 shadow-2xl"
    >
      <div className="flex justify-between items-center mb-8 border-b border-slate-700 pb-6">
        <div>
          <h2 className="text-3xl font-bold">Analysis Complete</h2>
          <p className="text-slate-400 mt-1">Your sneeze has been judged.</p>
        </div>
        <div className="text-right">
          <div className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">
            {totalScore}
          </div>
          <p className="text-sm text-yellow-500 font-bold tracking-widest uppercase mt-1">Overall Score</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div className="space-y-6">
          <ScoreBar icon={<Activity />} label="Power" score={data.power} color="bg-red-500" />
          <ScoreBar icon={<Volume2 />} label="Volume" score={data.volume} color="bg-blue-500" />
          <ScoreBar icon={<Wind />} label="Style" score={data.style} color="bg-purple-500" />
          <ScoreBar icon={<Trophy />} label="Suspense" score={data.suspense} color="bg-green-500" />
        </div>
        
        <div className="bg-slate-900 rounded-2xl p-4 flex items-center justify-center">
          <Radar data={chartData} options={chartOptions} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-indigo-900/50 border border-indigo-500/30 p-6 rounded-2xl text-center relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500"></div>
          <p className="text-indigo-300 text-sm font-bold uppercase tracking-wider mb-2">Animal Classification</p>
          <h3 className="text-4xl font-black text-white">The {data.animal}</h3>
        </motion.div>

        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="bg-green-900/50 border border-green-500/30 p-6 rounded-2xl text-center relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-500 to-emerald-500"></div>
          <p className="text-green-300 text-sm font-bold uppercase tracking-wider mb-2">Achievement Unlocked</p>
          <h3 className="text-3xl font-bold text-white">{data.achievement}</h3>
        </motion.div>
      </div>

      <motion.div 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.7 }}
        className="bg-slate-900 rounded-2xl p-6 border-l-4 border-blue-500 mb-8"
      >
        <p className="text-blue-400 text-sm font-bold uppercase mb-2">AI Commentary</p>
        <p className="text-xl italic text-gray-300">"{data.commentary}"</p>
      </motion.div>

      <div className="text-center">
        <button 
          onClick={onReset}
          className="inline-flex items-center space-x-2 px-6 py-3 rounded-full bg-slate-700 hover:bg-slate-600 transition-colors text-white font-semibold"
        >
          <RotateCcw className="w-5 h-5" />
          <span>Sneeze Again</span>
        </button>
      </div>
    </motion.div>
  );
};

const ScoreBar = ({ icon, label, score, color }) => (
  <div>
    <div className="flex justify-between items-center mb-2">
      <div className="flex items-center space-x-2 text-slate-300">
        {React.cloneElement(icon, { className: "w-5 h-5" })}
        <span className="font-semibold">{label}</span>
      </div>
      <span className="font-bold text-white">{score}/10</span>
    </div>
    <div className="w-full bg-slate-700 rounded-full h-3">
      <motion.div 
        initial={{ width: 0 }}
        animate={{ width: `${(score / 10) * 100}%` }}
        transition={{ duration: 1, ease: "easeOut" }}
        className={`h-3 rounded-full ${color}`} 
      />
    </div>
  </div>
);

export default ResultsDashboard;
