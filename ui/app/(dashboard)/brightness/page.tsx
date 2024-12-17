import Chart from "@/app/components/chart";
import Typography from "@mui/material/Typography";

export default function BrightnessPage() {
  return (
    <>
      <Typography>Brightness</Typography>
      <Chart height={600} display="Brightness" />
    </>
  );
}
