import React, { useState } from "react";
import "./topsisFormPage.css";

function TopsisFormPage() {

    const [alternativas, setAlternativas] = useState([]);
  const [criterios, setCriterios] = useState([]);
  const [matriz, setMatriz] = useState({});

  const adicionarAlternativa = (event) => {
    event.preventDefault();
    const input = event.target.previousSibling;
    const valor = input.value.trim();
    if (valor) {
      setAlternativas([...alternativas, valor]);
      input.value = '';
    }
  };

  const adicionarCriterio = (event) => {
    event.preventDefault();
    const input = event.target.previousSibling;
    const valor = input.value.trim();
    if (valor) {
      setCriterios([...criterios, valor]);
      input.value = '';
    }
  };

  const atualizarMatriz = (alt, crit, valor) => {
    setMatriz((prev) => ({
      ...prev,
      [alt]: {
        ...prev[alt],
        [crit]: valor
      }
    }));
  };

  const [tiposCriterio, setTiposCriterio] = useState({});

  const atualizarTipoCriterio = (crit, valor) => {
    setTiposCriterio((prev) => ({
      ...prev,
      [crit]: valor
    }));
  };

  const [pesosCriterio, setPesosCriterio] = useState({});

  const atualizarPesoCriterio = (crit, valor) => {
    setPesosCriterio((prev) => ({
      ...prev,
      [crit]: valor
    }));
  };

  return (
    <div className="topsis-form-page-container">

        <figure>
            <img src="assets/Forms.svg" alt="" />
        </figure>

        <div className="forms-container">
            <h1>Preencha os Inputs para o Método TOPSIS</h1>
            <p>
                Preencha as informações necessárias para calcular o método TOPSIS. 
                Insira alternativas, critérios, a matriz de performance, os tipos de critérios, os pesos e a métrica de distância desejada.
            </p>

            <fieldset> 
                <label>Alternativas</label>
                <div className="input-box">
                    <input type="text" className="input-addition" placeholder="Preencha e adicione alternativas"></input>
                    <button className="button-addition" onClick={adicionarAlternativa}>Adicionar +</button>
                </div>
                <ul className="filled-inputs-list">
                    {alternativas.map((alt, idx) => (<li key={idx}>{alt}</li>))}
                </ul>
            </fieldset>
            
            <fieldset> 
                <label>Critérios</label>
                <div className="input-box">
                    <input type="text" className="input-addition" placeholder="Preencha e adicione critérios"></input>
                    <button className="button-addition" onClick={adicionarCriterio}>Adicionar +</button>
                </div>
                <ul className="filled-inputs-list">
                    {criterios.map((alt, idx) => (<li key={idx}>{alt}</li>))}
                </ul>
            </fieldset>

            {criterios.length > 0 && (
                    <fieldset>
                    <label>Tipos de Critérios (Max/Min)</label>
                    <div className="list-types-criteria">
                        {criterios.map((crit, idx) => (

                        <div className="type-criteria" key={idx}>
                            <span>{crit}</span>
                            <select  onChange={(e) => atualizarTipoCriterio(crit, e.target.value)}>
                                <option value="max">Max</option>
                                <option value="min">Min</option>
                            </select>
                        </div>
                        ))}
                    </div>
                    </fieldset>
            )}

            {criterios.length > 0 && (
                <fieldset>
                    <label>Peso dos Critério</label>
                    <div className="list-types-criteria">
                        {criterios.map((crit, idx) => (
                        <div className="type-criteria" key={idx}>
                            <span>{crit}</span>
                            <input
                                type="number"
                                value="0"
                                onChange={(e) => atualizarPesoCriterio(crit, e.target.value)}
                            />
                      
                        </div>
                        ))}
                    </div>
                </fieldset>
            )}

            {alternativas.length > 0 && criterios.length > 0 && (
            <>
                <label>Matriz de Performance</label>

                {alternativas.map((alt, idx) => (
                <fieldset className="matrix-container" key={idx}> {/* key deve estar no fieldset */}
                    <span>Alternativa: {alt}</span> 
                    <div className="list-matrix">
                    {criterios.map((crit, cidx) => (
                        <div key={cidx} className="item-matrix">
                        <label>{crit}: </label>
                        <input
                            type="number"
                            step="0.01"
                            value="0"
                            onChange={(e) => atualizarMatriz(alt, crit, e.target.value)}
                        />
                        </div>
                    ))}
                    </div>
                </fieldset>
                ))}
            </>
            )}

            {(alternativas.length > 0 && criterios.length > 0 && 
                <fieldset> 
                    <label>Métrica de distância</label>
                    <div className="">
                        <input type="number" className="input" placeholder="Preencha a métrica de distância"></input>
                    </div>
                </fieldset>
            )}

           
        </div>
    </div>
  );
}

export default TopsisFormPage;
