import React from "react";
import "./topsisFormPage.css";

function TopsisFormPage() {
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
                    <button className="button-addition">Adicionar +</button>
                </div>
                
            </fieldset>
            
            <fieldset> 
                <label>Critérios</label>
                <div className="input-box">
                    <input type="text" className="input-addition" placeholder="Preencha e adicione critérios"></input>
                    <button className="button-addition">Adicionar +</button>
                </div>
                
            </fieldset>
        </div>
     
      
    </div>
  );
}

export default TopsisFormPage;
