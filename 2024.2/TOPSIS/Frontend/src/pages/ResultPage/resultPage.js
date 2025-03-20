import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { loadPyodide } from "pyodide";

function ResultPage() {
  const location = useLocation();
  const { inputData } = location.state || {};
  const [result, setResult] = useState("");

  useEffect(() => {
    async function runPython() {
        if (!inputData) return;
  
        // 1. Carregar Pyodide
        const pyodide = await loadPyodide();
  
        // 2. Buscar e carregar o conteúdo do `main.py`
        const response = await fetch("../../../../main.py"); 
        const pythonCode = await response.text();
  
        // 3. Passar os dados do formulário como JSON para o Pyodide
        pyodide.globals.set("input_data", JSON.stringify(inputData));
  
        // 4. Executar o código Python e capturar o resultado
        try {
          const output = await pyodide.runPythonAsync(pythonCode);
          setResult(output);
        } catch (error) {
          setResult("Erro ao executar o código Python.");
        }
      }
  
      runPython();
    }, [inputData]);


  return (
    <div>
      <h1>Resultado TOPSIS</h1>
      <p>{result}</p>
    </div>
  );
}

export default ResultPage;
