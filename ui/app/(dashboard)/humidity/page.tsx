import Chart from "@/app/components/chart";
import Typography from "@mui/material/Typography";

export default function HumidityPage() {
  return (
    <>
      <Typography>Humidity</Typography>

      <Chart height={600} display="Humidity" />
    </>
  );
}
