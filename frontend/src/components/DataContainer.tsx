import { useState, useEffect } from "react";

interface Props {
  children: string;
  endpoint: string;
}

function DataContainer({ children, endpoint }: Props) {
  const [data, setData] = useState([]);

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

  const upcomingRace = data.map((item) => {
    if (!item.Winner) {
      return (
        <>
          <h1>Upcoming race</h1>
          <tbody>
            <tr>
              <th>Date</th>
              <th>Race</th>
            </tr>
            <tr>
              <td>{item.Date}</td>
              <td>{item.Race}</td>
            </tr>
          </tbody>
        </>
      );
    }
    return "";
  });

  const previousRaces = (
    <>
      <h1>Previous races</h1>
      <tbody>
        <tr>
          {endpoint == 'get-data-cycling' ? <th>Date</th> : null}
          <th>Race</th>
          <th>Winner</th>
        </tr>
        {data.map((item, index) => {
          if (!item.Winner) {
            return "";
          } else {
            return (
              <tr key={index}>
                {item.Date ? <td>{item.Date}</td> : null}
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
    <div>
      <h1>{children}</h1>
      {upcomingRace}
      {previousRaces}
    </div>
  );
}

export default DataContainer;
