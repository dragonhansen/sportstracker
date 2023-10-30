import "./App.css";
import DataContainer from "./components/DataContainer";

function App() {
  return (
    <>
      <title>dragonhansen's Sports Tracker</title>
      <div className="title-container">
        <h1>dragonhansen's Sports Tracker</h1>
      </div>
      <div className="outer-container">
        <div className="stats-container">
          <DataContainer className="data-container" endpoint="get-data-cycling" datatype="cycling">
            Cycling races and results
          </DataContainer>
        </div>
        <div className="stats-container">
          <DataContainer className="data-container" endpoint="get-data-f1" datatype="f1">
            F1 GP's and results
          </DataContainer>
        </div>
      </div>
    </>
  );
}

export default App;
