import * as React from "react";
import Typography from "@mui/material/Typography";
import Link from "next/link";
import Chart from "../components/chart";
import { PageContainer } from "@toolpad/core/PageContainer";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid2";

export default function HomePage() {
  return (
    <>
      <Grid container spacing={0}>
        <Grid size={6}>
          <Paper className="m-5 rounded-lg">
            <Chart height={300} display="Temperature" />
          </Paper>
        </Grid>
        <Grid size={6}>
          <Paper className="m-5 rounded-lg">
            <Chart height={300} display="Humidity" />
          </Paper>
        </Grid>
        <Grid size={6}>
          <Paper className="m-5 rounded-lg">
            <Chart height={300} display="Brightness" />
          </Paper>
        </Grid>
      </Grid>
      {/* <div className="underline">Hi, Charlie</div> */}
    </>
  );
}
