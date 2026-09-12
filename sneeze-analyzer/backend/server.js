import express from 'express';
import cors from 'cors';
import multer from 'multer';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import OpenAI from 'openai';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Set up multer for audio upload
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => cb(null, `sneeze-${Date.now()}.wav`)
});
const upload = multer({ storage });

// const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY }); // Uncomment when you add the key

app.post('/upload-sneeze', upload.single('audio'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No audio file uploaded.' });
  }

  const audioPath = req.file.path;

  // Run the Python analysis script
  const pythonProcess = spawn('python', ['analyze_sneeze.py', audioPath]);

  let pythonOutput = '';
  pythonProcess.stdout.on('data', (data) => {
    pythonOutput += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
  });

  pythonProcess.on('close', async (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Failed to analyze audio.' });
    }

    try {
      const stats = JSON.parse(pythonOutput);
      
      // Calculate scores (mock logic based on stats)
      const power = Math.min(10, (stats.peak * 10)).toFixed(1);
      const volume = Math.min(10, (stats.volume * 100)).toFixed(1);
      const suspense = Math.min(10, (stats.duration * 2)).toFixed(1);
      const style = (Math.random() * (10 - 5) + 5).toFixed(1); // random 5-10

      // Assign Achievement
      let achievement = "Beginner Sneezer";
      if (power > 9) achievement = "Earth Shaker";
      else if (volume > 8) achievement = "Wake The Neighbors";
      else if (stats.duration > 4) achievement = "The Build-Up";

      // Assign Animal
      let animal = "Mouse";
      if (power > 8) animal = "Rhino";
      else if (volume > 8) animal = "Lion";
      else if (style > 9) animal = "Eagle";

      /* // OPENAI INTEGRATION (Mocked for now)
      const prompt = `You are a professional sneeze commentator. Power: ${power}, Volume: ${volume}, Style: ${style}. Generate a funny sports commentary (max 2 sentences).`;
      
      const completion = await openai.chat.completions.create({
        messages: [{ role: "system", content: prompt }],
        model: "gpt-3.5-turbo",
      });
      const commentary = completion.choices[0].message.content;
      */
      
      const commentary = "An explosive opening sneeze with championship-level projection. Slightly chaotic landing, but the crowd loved it.";

      res.json({
        power: parseFloat(power),
        volume: parseFloat(volume),
        suspense: parseFloat(suspense),
        style: parseFloat(style),
        achievement,
        animal,
        commentary
      });

    } catch (e) {
      console.error(e);
      res.status(500).json({ error: 'Error parsing analysis results.' });
    } finally {
      // Clean up uploaded file
      fs.unlink(audioPath, (err) => {
        if (err) console.error('Failed to delete file:', err);
      });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
