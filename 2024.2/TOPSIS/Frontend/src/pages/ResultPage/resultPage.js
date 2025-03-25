import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./resultPage.css";

function ResultPage() {
  const location = useLocation();
  const { inputData } = location.state || {};
  const [result, setResult] = useState("");
  const [pyodide, setPyodide] = useState(null);

  useEffect(() => {
    async function loadAndRunPyodide() {
      // if (!inputData) return;

      // 1. Carregar Pyodide dinamicamente
      if (!window.loadPyodide) {
        console.error("Pyodide não foi carregado corretamente.");
        return;
      }

      const pyodideInstance = await window.loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.0/full/",
      });

      setPyodide(pyodideInstance);

       // 2. Instalar o numpy
       try {
        await pyodideInstance.loadPackage("numpy");
      } catch (error) {
        console.error("Erro ao carregar o pacote numpy:", error);
        setResult("Erro ao carregar o pacote numpy.");
        return;
      }

      // 3. Buscar e carregar o conteúdo do `main.py`
      try {
        const response = await fetch("/main.py"); // Certifique-se de que o arquivo está acessível na pasta `public`
        const pythonCode = await response.text();
    
        const input = {
          "method": "TOPSIS",
          "parameters": {
            "alternatives": ["A1", "A2", "A3"],
            "criteria": ["C1", "C2", "C3"],
            "performance_matrix": {
              "A1": [0.7, 0.5, 0.8],
              "A2": [0.6, 0.7, 0.6],
              "A3": [0.8, 0.6, 0.7]
            },
            "criteria_types": {
              "C1": "max",
              "C2": "min",
              "C3": "max"
            },
            "weights": {
              "C1": 0.4,
              "C2": 0.3,
              "C3": 0.3
            },
            "distance_metric": 2
          }
        }


        // 4. Passar os dados do formulário como JSON para o Pyodide
        pyodideInstance.globals.set("input_data", JSON.stringify(inputData));

        // 5. Executar o código Python e capturar o resultado
        const output = await pyodideInstance.runPythonAsync(pythonCode);

        // 6. Chamar a função get_input_data exposta pelo Pyodide
        const resultProxy = pyodideInstance.globals.get("get_input_data")(JSON.stringify(inputData));

        // 7. Converter o resultado de Proxy para JavaScript
        const result = resultProxy.toJs(); // Converte o proxy para um objeto JavaScript

        setResult(result);
      } catch (error) {
        console.error("Erro ao carregar ou executar o Python:", error);
        setResult("Erro ao executar o código Python.");
      }
    }

    loadAndRunPyodide();
  }, [inputData]);

  // Função para renderizar o conteúdo do resultado
  const renderResult = (result) => {
    if (!result) return <div className="loader-container"><span className="loader"></span> Carregando...</div>;
    if (result.error) return <p>Erro: {result.error}</p>;
  
    const results = result.get("results")

    return (
      <div className="result-list-container">
        <div className="box-1">
          {/* Ranking */}
          <div className="result-box ranking">
              <h4>Ranking das Alternativas</h4>
              <ol>
                {results.get("ranking").map((alternative, index) => (
                  <li key={alternative}>
                    <strong>{index + 1} º</strong> {alternative}
                  </li>
                ))}
              </ol>
            </div>
            {/* Scores TOPSIS */}
            <div className="result-box score">
              <h4>Scores TOPSIS</h4>
              <ul>
                {Array.from(results.get("topsis_score").entries()).map(([alternative, value]) => (
                  <li key={alternative}>
                    <strong>{alternative}</strong> {value.toFixed(4)}
                  </li>
                ))}
              </ul>
            </div>
        </div>

        <div className="box-1">

            {/* Solução Ideal Positiva */}
            <div className="result-box small-list">
              <h4>Solução Ideal Positiva</h4>
              <ul>
                {Array.from(results.get("positive_ideal_solution").entries()).map(([criterion, value]) => (
                  <li key={criterion}>
                    <strong>{criterion}:</strong> {value.toFixed(4)}
                  </li>
                ))}
              </ul>
            </div>
        
            {/* Solução Ideal Negativa */}
            <div className="result-box  small-list">
              <h4>Solução Ideal Negativa</h4>
              <ul>
                {Array.from(results.get("negative_ideal_solution").entries()).map(([criterion, value]) => (
                  <li key={criterion}>
                    <strong>{criterion}</strong>: {value.toFixed(4)}
                  </li>
                ))}
              </ul>
            </div>
        
            {/* Distância para a Solução Ideal Positiva */}
            <div className="result-box  small-list">
              <h4>Distância para a Solução Ideal Positiva</h4>
              <ul>
                {Array.from(results.get("distance_to_pis").entries()).map(([alternative, value]) => (
                  <li key={alternative}>
                    <strong>{alternative}</strong>: {value.toFixed(4)}
                  </li>
                ))}
              </ul>
            </div>
        
            {/* Distância para a Solução Ideal Negativa */}
            <div className="result-box  small-list">
              <h4>Distância para a Solução Ideal Negativa</h4>
              <ul>
                {Array.from(results.get("distance_to_nis").entries()).map(([alternative, value]) => (
                  <li key={alternative}>
                    <strong>{alternative}</strong>: {value.toFixed(4)}
                  </li>
                ))}
              </ul>
            </div>   

        </div>
        
        
       
      </div>
    );
  };

  return (
    <div className="result-page-container">
      <h1>Resultado TOPSIS</h1>
      {renderResult(result)}
    </div>
  );
}

export default ResultPage;
