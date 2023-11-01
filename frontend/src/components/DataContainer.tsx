import { useState, useEffect } from "react";

interface Props {
  children: string;
  endpoint: string;
  className?: string;
  datatype: string;
}

type RaceData = {
  Date: string;
  Race: string;
  Winner: string;
};

function DataContainer({ children, endpoint, datatype}: Props) {
  const [data, setData] = useState<RaceData[]>([]);

  const fetchData = () => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((actualData) => {
        setData(actualData);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Use different terminology for F1 and cycling
  const headers: {upcoming: string, previous: string, race: string} = (datatype === 'cycling') ? 
  {upcoming: 'Upcoming Race', previous: 'Previous Races', race: 'Race'} : {upcoming: "Upcoming GP's", previous: "Previous GP's", race: 'Grand Prix'};

  const upcomingRace = data.map((item) => {
    if (!item.Winner) {
      return (
        <>
          <thead>
          <h2>{headers.upcoming}</h2>
            <tr>
              <th>Date</th>
              <th>{headers.race}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{item.Date}</td>
              <td>{item.Race}</td>
            </tr>
          </tbody>
        </>
      );
    }
    return <></>;
  });

  const previousRaces = (
    <>
      <thead>
      <h2>{headers.previous}</h2>
        <tr>
          {datatype === 'cycling' ? <th>Date</th> : null}
          <th>{headers.race}</th>
          <th>Winner</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => {
          if (!item.Winner) {
            return <></>;
          } else {
            return (
              <tr key={index}>
                {datatype === 'cycling' ? <td>{item.Date}</td> : null}
                <td>{item.Race}</td>
                <td>{item.Winner}</td>
              </tr>
            );
          }
        })}
      </tbody>
    </>
  );

  return (
    <>
      <h1>{children}</h1>
      <table>
        {upcomingRace}
        {previousRaces}
      </table>
    </>
  );
}

export default DataContainer;
