const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Rota de teste
app.get('/api/projetos', (req, res) => {
  res.json({ 
    message: "Servidor rodando paezão",
    projetos: [] 
  });
});

app.listen(PORT, () => {
  console.log(`Servidor rodando aqui: ${PORT}`);
});