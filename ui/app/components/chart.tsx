"use client";
import React, { useState, useMemo, useEffect } from "react";
import axios from "axios";
import { lightTheme, darkTheme, XYChartTheme } from "@visx/xychart";
import CustomChartBackground from "./customChartBackground";
import { curveLinear } from "@visx/curve";
const dateScaleConfig = { type: "band", paddingInner: 0.3 } as const;
const temperatureScaleConfig = { type: "linear" } as const;
import {
  AnimatedAreaSeries as AreaSeries,
  AnimatedAreaStack as AreaStack,
  AnimatedAxis as Axis,
  AnimatedGrid as Grid,
  Tooltip,
  XYChart,
} from "@visx/xychart";

const getTime = (d: Measurement) => {
  const dateObj = new Date(d.recorded_at);
  const hours = dateObj.getHours();
  const mins = dateObj.getMinutes();
  const formattedHours = hours < 10 ? "0" + hours : hours;
  const formattedMinutes = mins < 10 ? "0" + mins : mins;
  return `${formattedHours}:${formattedMinutes}`;
};
const getDate = (d: Measurement) => d.recorded_at;
const getMeasure = (d: Measurement) => d.measure;

export type ChartProps = {
  display: Display;
  height: number;
};

type Measurement = {
  device: string;
  host: string;
  inserted_at: string;
  measure: number;
  recorded_at: string;
  unit: string;
  url: string;
};

type Display = "Temperature" | "Humidity";

const displayUnitMapping = { Temperature: "°C", Humidity: "%" };

export default function Chart({ height, display }: ChartProps) {
  const [theme, setTheme] = useState<XYChartTheme>(darkTheme);
  const [tempData, setTempData] = useState<Measurement[]>([]);

  useEffect(() => {
    const getData = () => {
      axios
        .get(
          `http://192.168.1.70:1337/api/measurements/?unit=${display.toLowerCase()}&last-hours=12`
        )
        .then(({ data }) => {
          const dataset: Measurement[] = data;
          setTempData(dataset);
        });
    };
    getData();
    const intervalId = setInterval(
      () => {
        getData();
      },
      1000 * 60 * 1
    );
    return () => clearInterval(intervalId);
  }, []);

  const generateLabel = (): string => {
    return `${display} (${displayUnitMapping[display]})`;
  };

  const renderHorizontally = false;
  const animationTrajectory = "center";
  const showGridColumns = false;
  const showGridRows = false;
  const numTicks = 4;
  const showTooltip = true;
  const curve = curveLinear;
  const config = useMemo(
    () => ({
      x: dateScaleConfig,
      y: temperatureScaleConfig,
    }),
    []
  );
  const accessors = useMemo(
    () => ({
      date: getDate,
      time: getTime,
    }),
    []
  );

  return (
    <XYChart
      theme={theme}
      xScale={config.x}
      yScale={config.y}
      height={Math.min(400, height)}
    >
      <CustomChartBackground />
      <Grid
        key={`grid-${animationTrajectory}`} // force animate on update
        rows={showGridRows}
        columns={showGridColumns}
        animationTrajectory={animationTrajectory}
        numTicks={numTicks}
      />
      (
      <AreaStack curve={curve}>
        <AreaSeries
          dataKey="measure"
          data={tempData}
          xAccessor={getTime}
          yAccessor={getMeasure}
          fillOpacity={0.4}
          fill={display === "Temperature" ? "lightcoral" : "#3BC9DB"}
        />
        {/* <AreaSeries
          dataKey="New York"
          data={data}
          xAccessor={accessors.x["New York"]}
          yAccessor={accessors.y["New York"]}
          fillOpacity={0.4}
        />
        <AreaSeries
          dataKey="San Francisco"
          data={data}
          xAccessor={accessors.x["San Francisco"]}
          yAccessor={accessors.y["San Francisco"]}
          fillOpacity={0.4}
        /> */}
      </AreaStack>
      )
      <Axis
        key={`time-axis-${animationTrajectory}-${renderHorizontally}`}
        orientation={"bottom"}
        numTicks={12}
        animationTrajectory={animationTrajectory}
      />
      <Axis
        key={`temp-axis-${animationTrajectory}-${renderHorizontally}`}
        label={generateLabel()}
        orientation={"left"}
        numTicks={numTicks}
        animationTrajectory={animationTrajectory}
      />
      {showTooltip && (
        <Tooltip<Measurement>
          showHorizontalCrosshair={true}
          showVerticalCrosshair={true}
          renderTooltip={({ tooltipData, colorScale }) => (
            <div>
              {(tooltipData?.nearestDatum?.datum &&
                "Datetime: " +
                  accessors.date(tooltipData?.nearestDatum?.datum)) ||
                "No date"}
              <br />
              <br />
              {Object.keys(tooltipData?.datumByKey ?? {}).map((location) => {
                const displayUnit =
                  tooltipData?.nearestDatum?.datum &&
                  getMeasure(tooltipData?.nearestDatum?.datum);

                return (
                  <div key={location}>
                    <em
                      style={{
                        color: colorScale?.(location),
                        textDecoration:
                          tooltipData?.nearestDatum?.key === location
                            ? "underline"
                            : undefined,
                      }}
                    >
                      {displayUnit}
                    </em>{" "}
                    {displayUnit == null || Number.isNaN(displayUnit)
                      ? "–"
                      : displayUnitMapping[display]}
                  </div>
                );
              })}
            </div>
          )}
        />
      )}
    </XYChart>
  );
}
