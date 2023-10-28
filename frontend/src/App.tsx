import './App.css'
import DataContainer from './components/DataContainer'

function App() {

  return (
    <>
      <title>dragonhansen's Sports Tracker</title>
      <h1 id="website-title">dragonhansen's Sports Tracker</h1>
      <button>Update using JS fetch</button>
      <DataContainer endpoint='get-data-cycling'>Cycling races and results</DataContainer>
      <DataContainer endpoint='get-data-f1'>F1 GP's and results</DataContainer>
    </>
  )
}

export default App
