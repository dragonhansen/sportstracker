import './App.css'
import DataContainer from './components/DataContainer'

function App() {

  return (
    <>
      <title>dragonhansen's Sports Tracker</title>
      <div className='title-container'>
      <h1 id="website-title">dragonhansen's Sports Tracker</h1>
      <button>Update using JS fetch</button>
      </div>
      <div className='outer-container'>
        <div className='stats-container'>
        <DataContainer endpoint='get-data-cycling'>Cycling races and results</DataContainer>
        </div>
        <div className='stats-container'>
         <DataContainer endpoint='get-data-f1'>F1 GP's and results</DataContainer>
        </div>
      </div>
    </>
  )
}

export default App
