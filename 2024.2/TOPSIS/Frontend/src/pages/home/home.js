import { Link } from "react-router-dom";
import "./home.css"; // Estilos opcionais

const Home = () => {
  return (
    <div className="home-container">

        <header className="header-container">
            <div className="header-informations-container">
                <h1>Bem-vindo ao Método TOPSIS</h1>
                <p>
                    O <strong>Técnica para Ordem de Preferência por Similaridade com a Solução Ideal</strong> 
                    (TOPSIS) é um método de tomada de decisão multicritério amplamente utilizado para 
                    escolher a melhor alternativa entre várias opções, considerando diferentes critérios de 
                    avaliação.
                </p>
            </div>

            <figure className="figure">
                <img src="assets/tela-inicial.svg" alt="Logo" />
            </figure>
        </header>

        <section className="section-container">
            <h2>📌 Para que serve o TOPSIS?</h2>
            <ul>
                <li>Ajuda a tomar decisões complexas considerando múltiplos critérios.</li>
                <li>É amplamente usado em áreas como gestão, engenharia e economia.</li>
                <li>Permite comparar alternativas e ranqueá-las de forma objetiva.</li>
            </ul>
        </section>
      

  

      

      <h2>⚙️ Como funciona?</h2>
      <p>
        O método calcula a alternativa que está mais próxima da solução ideal (melhor opção) 
        e mais distante da solução anti-ideal (pior opção). Para isso, utiliza uma matriz de 
        desempenho ponderada e métricas de distância.
      </p>

      <h2>📊 Exemplo prático</h2>
      <p>
        Imagine que você precisa escolher um novo fornecedor para sua empresa com base 
        em critérios como <strong>custo, qualidade e prazo de entrega</strong>. O TOPSIS ajudaria a 
        encontrar a melhor opção comparando todas as alternativas de forma estruturada.
      </p>

      <h2>🚀 Vamos começar?</h2>
      <p>
        Você pode testar o método inserindo seus próprios dados na ferramenta.
      </p>
      <Link to="/topsis">
        <button className="start-button">Ir para o cálculo TOPSIS</button>
      </Link>
    </div>
  );
};

export default Home;
