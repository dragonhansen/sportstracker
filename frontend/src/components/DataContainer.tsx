import { useState, useEffect } from "react";

interface Props {
  children: string;
  className?: string;
  endpoint: string;
  datatype: string;
  includeDate?: boolean;
}

type RaceData = {
  Date: string;
  Race: string;
  Winner: string;
};

function DataContainer({ children, endpoint, datatype, includeDate}: Props) {
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

  // If there is no data at all, something most likely went wrong so we bail out and notify the user
  if (data.length === 0) {return <h2>Error, no data was received</h2>}

  // Use different terminology for F1 and cycling
  const headers: {upcoming: string, previous: string, race: string} = (datatype === 'cycling') ? 
  {upcoming: 'Upcoming Race', previous: 'Previous Races', race: 'Race'} : {upcoming: "Upcoming GP's", previous: "Previous GP's", race: 'Grand Prix'};

  // Define some boolean values that decides if parts of the containers should be renderen - this is probably not an ideal solution
  let noPreviousRaces: boolean = true;
  let noUpcomingRaces: boolean = true;

  const upcomingRace = data.map((item) => {
    if (!item.Winner) {
      noUpcomingRaces = false;
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
          {includeDate ? <th>Date</th> : null}
          <th>{headers.race}</th>
          <th>Winner</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => {
          if (!item.Winner) {
            return <></>;
          } else {
            noPreviousRaces = false;
            return (
              <tr key={index} className="highlighted-row">
                {includeDate ? <td>{item.Date}</td> : null}
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
        {noUpcomingRaces ? <thead><h2>{headers.upcoming}</h2><tr>Season is over, very sad!</tr></thead> : upcomingRace}
        {noPreviousRaces ? null : previousRaces}
      </table>
    </>
  );
}

export default DataContainer;
