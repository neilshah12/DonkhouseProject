import React from "react";
import { Line } from "react-chartjs-2";
import 'chart.js/auto';

function LineGraph({ data, labels }) {
  return (
    <div>
      <Line
        data={{
          // x-axis label values
          labels: labels,
          datasets: [
            {
              label: "Cumulative Net",
              // y-axis data plotting values
              data: data,
              fill: false,
              borderWidth:4,
              backgroundColor: "rgb(255, 99, 132)",
              borderColor:'black',
              responsive:true
            },
          ],
        }}
      />
    </div>
  );
}

export default LineGraph;