import * as React from "react";
import Typography from "@mui/material/Typography";
import Chart from "@/app/components/chart";

export default function TemperaturePage() {
  return (
    <>
      <Typography>Temperature</Typography>

      <Chart height={600} display="Temperature" />
    </>
  );
}
